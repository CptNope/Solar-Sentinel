import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dashboard.app import create_app, seed_demo


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = {'TESTING': True, 'DATABASE': str(Path(self.temp.name) / 'test.db'), 'TOKEN': 'test-token'}
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.auth = {'Authorization': 'Bearer test-token'}

    def tearDown(self):
        self.temp.cleanup()

    def post(self, route, payload):
        return self.client.post(route, json=payload, headers=self.auth)

    def test_empty_state_never_claims_healthy_telemetry(self):
        data = self.client.get('/api/state').json
        self.assertEqual(data['nodes'], [])
        self.assertEqual(data['reports'], [])
        self.assertFalse(data['demo'])
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/status').status_code, 200)

    def test_writes_require_valid_token(self):
        for route in ['/api/access', '/api/nodes', '/api/reports']:
            self.assertEqual(self.client.post(route, json={}).status_code, 401)
            self.assertEqual(self.client.post(route, json={}, headers={'Authorization': 'Bearer é'}).status_code, 401)
        self.assertEqual(self.post('/api/access', {}).status_code, 200)
        self.assertEqual(self.client.patch('/api/reports/1', json={'resolved': True}).status_code, 401)

    def test_node_upsert_and_unknown_readings(self):
        self.assertEqual(self.post('/api/nodes', {'id': 'one', 'name': 'One', 'battery': 0, 'latitude': 0, 'longitude': 0}).status_code, 200)
        node = self.client.get('/api/state').json['nodes'][0]
        self.assertEqual(node['battery'], 0)
        self.assertEqual(node['latitude'], 0)
        self.assertIsNone(node['voltage'])
        self.post('/api/nodes', {'id': 'one', 'name': 'Updated'})
        nodes = self.client.get('/api/state').json['nodes']
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0]['name'], 'Updated')
        self.assertIsNone(nodes[0]['battery'])

    def test_freshness_boundaries(self):
        with patch('dashboard.app.time.time', return_value=1000):
            self.post('/api/nodes', {'id': 'one', 'name': 'One'})
        for current, expected in [(1119, 'online'), (1120, 'stale'), (1599, 'stale'), (1600, 'offline')]:
            with patch('dashboard.app.time.time', return_value=current):
                self.assertEqual(self.client.get('/api/state').json['nodes'][0]['status'], expected)

    def test_invalid_telemetry_and_json(self):
        for extra in [{'battery': -1}, {'battery': 101}, {'battery': True}, {'voltage': float('nan')},
                      {'voltage': float('inf')}, {'voltage': 10**1000}, {'latitude': 91, 'longitude': 0}, {'latitude': 1}, {'battery': '80'}]:
            with self.subTest(extra=extra):
                self.assertEqual(self.post('/api/nodes', {'id': 'one', 'name': 'One', **extra}).status_code, 400)
        self.assertEqual(self.post('/api/nodes', []).status_code, 400)
        self.assertEqual(self.post('/api/nodes', {'id': ' ', 'name': 'One'}).status_code, 400)
        self.assertEqual(self.client.post('/api/nodes', data='{', content_type='application/json', headers=self.auth).status_code, 400)
        self.assertEqual(self.client.post('/api/nodes', data='x' * 17000, content_type='application/json', headers=self.auth).status_code, 413)

    def test_report_retry_deduplication_and_conflict(self):
        payload = {'author': 'Team', 'message': 'Check-in complete', 'priority': 'urgent', 'request_id': 'unique'}
        first = self.post('/api/reports', payload)
        second = self.post('/api/reports', payload)
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json, second.json)
        self.assertEqual(self.post('/api/reports', {**payload, 'message': 'Different'}).status_code, 409)
        self.assertEqual(self.client.get('/api/state').json['open_reports'], 1)

    def test_resolution_and_restart_persistence(self):
        self.post('/api/nodes', {'id': 'one', 'name': 'One'})
        result = self.post('/api/reports', {'author': 'Team', 'message': '<script>alert(1)</script>', 'request_id': 'r1'})
        route = f"/api/reports/{result.json['id']}"
        self.assertEqual(self.client.patch(route, json={'resolved': 'yes'}, headers=self.auth).status_code, 400)
        self.assertEqual(self.client.patch(route, json={'resolved': True}, headers=self.auth).status_code, 200)
        restarted = create_app(self.config).test_client()
        data = restarted.get('/api/state').json
        self.assertEqual(data['open_reports'], 0)
        self.assertEqual(len(data['nodes']), 1)
        self.assertEqual(data['reports'][0]['message'], '<script>alert(1)</script>')
        self.assertEqual(self.client.patch('/api/reports/999', json={'resolved': True}, headers=self.auth).status_code, 404)

    def test_invalid_report_fields(self):
        base = {'author': 'Team', 'message': 'Hello', 'request_id': 'r1'}
        for extra in [{'author': ''}, {'message': 'x' * 2001}, {'priority': 'bad'}, {'priority': []}, {'request_id': ''}]:
            self.assertEqual(self.post('/api/reports', {**base, **extra}).status_code, 400)

    def test_demo_is_explicit_and_seed_is_idempotent(self):
        demo = create_app({**self.config, 'DATABASE': str(Path(self.temp.name) / 'demo.db'), 'DEMO': True})
        seed_demo(demo)
        seed_demo(demo)
        result = demo.test_client().get('/api/state').json
        self.assertTrue(result['demo'])
        self.assertEqual(len(result['nodes']), 3)
        self.assertEqual(len(result['reports']), 2)
        self.assertEqual(self.client.get('/api/state').json['nodes'], [])

    def test_security_headers(self):
        response = self.client.get('/api/state')
        self.assertEqual(response.headers['Cache-Control'], 'no-store')
        self.assertIn("frame-ancestors 'none'", response.headers['Content-Security-Policy'])
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')


if __name__ == '__main__':
    unittest.main()
