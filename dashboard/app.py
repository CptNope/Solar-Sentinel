# SolarSentinel - Flask Dashboard App

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/status')
def status():
    # Example status variables (replace with real data later)
    solar_voltage = 12.8
    battery_status = "OK"
    gps_fix = True
    return render_template('status.html', 
                           solar_voltage=solar_voltage, 
                           battery_status=battery_status, 
                           gps_fix=gps_fix)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
