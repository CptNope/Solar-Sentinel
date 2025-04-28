#!/usr/bin/env python3
# SolarSentinel - Solar Power Monitor Script

import time
import random  # Replace with real sensor reading logic later

def read_solar_data():
    # Placeholder values (simulate for now)
    voltage = round(random.uniform(11.8, 13.2), 2)
    current = round(random.uniform(0.5, 2.0), 2)
    return voltage, current

def main():
    while True:
        voltage, current = read_solar_data()
        print(f"Solar Voltage: {voltage} V | Solar Current: {current} A")
        time.sleep(10)  # Read every 10 seconds

if __name__ == "__main__":
    main()
