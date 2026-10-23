"""Local field dashboard. Run with python -m dashboard.app."""
import argparse
from contextlib import closing, contextmanager
import hmac
import math
import os
from pathlib import Path
import secrets
import sqlite3
import time

from flask import Flask, jsonify, render_template, request


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(DATABASE=os.environ.get('SENTINEL_DB', str(Path(__file__).parent / 'instance' / 'sentinel.sqlite3')),
                      TOKEN=os.environ.get('SENTINEL_TOKEN'), DEMO=False, MAX_CONTENT_LENGTH=16384)
    app.config.update(config or {})
    Path(app.config['DATABASE']).parent.mkdir(parents=True, exist_ok=True)
    if not app.config['TOKEN']:
        token_path = Path(app.config['DATABASE']).with_suffix('.token')
        if not token_path.exists():
            token_path.write_text(secrets.token_urlsafe(32), encoding='utf-8')
            token_path.chmod(0o600)
        app.config['TOKEN'] = token_path.read_text(encoding='utf-8').strip()

    @contextmanager
    def connect():
        db = sqlite3.connect(app.config['DATABASE'], timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    with connect() as db:
        db.executescript('''
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS nodes (
              id TEXT PRIMARY KEY, name TEXT NOT NULL, voltage REAL,
              battery REAL, latitude REAL, longitude REAL, last_seen REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS reports (
              id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT NOT NULL,
              message TEXT NOT NULL, priority TEXT NOT NULL,
              resolved INTEGER NOT NULL DEFAULT 0, created REAL NOT NULL,
              request_id TEXT UNIQUE);
        ''')

    @app.before_request
    def protect_writes():
        if request.method in ('POST', 'PATCH', 'DELETE', 'PUT'):
            supplied = request.headers.get('Authorization', '').removeprefix('Bearer ')
            if not hmac.compare_digest(supplied.encode('utf-8'), app.config['TOKEN'].encode('utf-8')):
                return jsonify(error='A valid access token is required.'), 401

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        if request.path.startswith('/api/'):
            response.headers['Cache-Control'] = 'no-store'
        return response

    @app.errorhandler(400)
    @app.errorhandler(413)
    @app.errorhandler(415)
    def bad_request(error):
        return jsonify(error='Send a valid JSON object (maximum 16 KB).'), error.code

    def payload():
        value = request.get_json()
        if not isinstance(value, dict):
            raise ValueError('Expected a JSON object.')
        return value

    def text_value(data, key, limit):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > limit:
            raise ValueError(f'{key} must contain 1–{limit} characters.')
        return value.strip()

    def number(data, key, low, high):
        value = data.get(key)
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not low <= value <= high or not math.isfinite(value):
            raise ValueError(f'{key} must be between {low} and {high}.')
        return value

    @app.errorhandler(ValueError)
    def validation(error):
        return jsonify(error=str(error)), 400

    @app.get('/')
    @app.get('/status')
    def home():
        return render_template('index.html')

    @app.get('/api/state')
    def state():
        now = time.time()
        with connect() as db:
            nodes = [dict(row) for row in db.execute('SELECT * FROM nodes ORDER BY name COLLATE NOCASE')]
            reports = [dict(row) for row in db.execute('SELECT * FROM reports ORDER BY created DESC, id DESC LIMIT 200')]
            open_count = db.execute('SELECT COUNT(*) FROM reports WHERE resolved=0').fetchone()[0]
        for node in nodes:
            node['age_seconds'] = max(0, int(now - node['last_seen']))
            node['status'] = 'online' if node['age_seconds'] < 120 else 'stale' if node['age_seconds'] < 600 else 'offline'
        return jsonify(nodes=nodes, reports=reports, open_reports=open_count, demo=app.config['DEMO'], server_time=now)

    @app.get('/api/health')
    def health():
        with connect() as db:
            db.execute('SELECT 1').fetchone()
        return jsonify(status='ok', demo=app.config['DEMO'])

    @app.post('/api/access')
    def access():
        return jsonify(status='authorized')

    @app.post('/api/nodes')
    def check_in():
        data = payload()
        node_id = text_value(data, 'id', 64)
        name = text_value(data, 'name', 80)
        voltage = number(data, 'voltage', 0, 100)
        battery = number(data, 'battery', 0, 100)
        lat = number(data, 'latitude', -90, 90)
        lon = number(data, 'longitude', -180, 180)
        if (lat is None) != (lon is None):
            raise ValueError('Provide both latitude and longitude, or neither.')
        with connect() as db:
            db.execute('''INSERT INTO nodes VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET
                name=excluded.name, voltage=excluded.voltage, battery=excluded.battery,
                latitude=excluded.latitude, longitude=excluded.longitude, last_seen=excluded.last_seen''',
                       (node_id, name, voltage, battery, lat, lon, time.time()))
        return jsonify(id=node_id), 200

    @app.post('/api/reports')
    def add_report():
        data = payload()
        author = text_value(data, 'author', 80)
        message = text_value(data, 'message', 2000)
        priority = data.get('priority', 'routine')
        if priority not in ('routine', 'important', 'urgent'):
            raise ValueError('Unknown priority.')
        request_id = text_value(data, 'request_id', 64)
        with connect() as db:
            result = db.execute('INSERT OR IGNORE INTO reports(author,message,priority,created,request_id) VALUES(?,?,?,?,?)',
                                (author, message, priority, time.time(), request_id))
            saved = db.execute('SELECT * FROM reports WHERE request_id=?', (request_id,)).fetchone()
            if (saved['author'], saved['message'], saved['priority']) != (author, message, priority):
                return jsonify(error='Request ID already belongs to a different report.'), 409
        return jsonify(id=saved['id']), 201 if result.rowcount else 200

    @app.patch('/api/reports/<int:report_id>')
    def resolve(report_id):
        data = payload()
        if type(data.get('resolved')) is not bool:
            raise ValueError('resolved must be true or false.')
        with connect() as db:
            result = db.execute('UPDATE reports SET resolved=? WHERE id=?', (data['resolved'], report_id))
        if not result.rowcount:
            return jsonify(error='Report not found.'), 404
        return jsonify(id=report_id, resolved=data['resolved'])

    return app


def seed_demo(app):
    with closing(sqlite3.connect(app.config['DATABASE'])) as db, db:
        if db.execute('SELECT COUNT(*) FROM nodes').fetchone()[0]:
            return
        now = time.time()
        db.executemany('INSERT INTO nodes VALUES(?,?,?,?,?,?,?)', [
            ('base', 'Base camp', 13.2, 86, 35.61, -82.55, now),
            ('ridge', 'Ridge relay', 12.6, 64, 35.63, -82.52, now - 40),
            ('trail', 'Trail team', None, 32, 35.59, -82.53, now - 240)])
        db.executemany('INSERT INTO reports(author,message,priority,created) VALUES(?,?,?,?)', [
            ('Base camp', 'Demo: local field network established. Check-in interval is 60 seconds.', 'routine', now - 900),
            ('Trail team', 'Demo: pausing at the trail junction. Next check-in overdue.', 'important', now - 240)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true', help='Use a separate database with sample data.')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    options = {'DEMO': args.demo}
    if args.demo:
        options['DATABASE'] = str(Path(__file__).parent / 'instance' / 'demo.sqlite3')
    application = create_app(options)
    if args.demo:
        seed_demo(application)
    print('Access token: set SENTINEL_TOKEN or read the .token file beside the database.', flush=True)
    print(f'Dashboard: http://{args.host}:{args.port}', flush=True)
    from waitress import serve
    serve(application, host=args.host, port=args.port)
