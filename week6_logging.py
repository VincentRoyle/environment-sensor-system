"""
Week 6 — Reliability & Logging

- Retries failed DHT reads
- Logs readings to a CSV file on the Pico
- Includes a simple timestamp (seconds since boot)

Note: Pico typically has no real-time clock unless you add NTP/RTC.
"""

from machine import Pin
import dht
import time

# ---- Config ----
SENSOR_GPIO = 22          # change if needed (match your working pin)
THRESHOLD_C = 25.0        # keep from Week 5 if you like (optional use)
LOG_FILE = "dht_log.csv"
LOG_INTERVAL_S = 30       # 30s interval -> 10 mins gives ~20 entries
RETRY_COUNT = 3
RETRY_DELAY_S = 1

sensor = dht.DHT22(Pin(SENSOR_GPIO))
led = Pin("LED", Pin.OUT)

time.sleep(2)  # stabilise sensor


def read_dht_with_retry():
    """
    Returns (temp_c, hum) or (None, None) if all retries fail.
    """
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            sensor.measure()
            temp_c = sensor.temperature()
            hum = sensor.humidity()

            # Basic sanity checks (reject nonsense values)
            if temp_c is None or hum is None:
                raise ValueError("None reading")
            if hum < 0 or hum > 100:
                raise ValueError("Humidity out of range")
            if temp_c < -40 or temp_c > 80:
                raise ValueError("Temp out of range")

            return temp_c, hum

        except Exception as e:
            print(f"Read failed (attempt {attempt}/{RETRY_COUNT}): {repr(e)}")
            time.sleep(RETRY_DELAY_S)

    return None, None


def ensure_csv_header():
    """
    Create file with header if it doesn't exist.
    """
    try:
        with open(LOG_FILE, "r") as f:
            first_line = f.readline().strip()
            if first_line.startswith("ts_s,"):
                return
    except OSError:
        pass

    with open(LOG_FILE, "w") as f:
        f.write("ts_s,temp_c,hum_pct,led_state\n")


ensure_csv_header()

start_s = time.time()
entry_count = 0

print("Logging to:", LOG_FILE)
print("Interval:", LOG_INTERVAL_S, "seconds")

while True:
    ts_s = time.time() - start_s  # simple timestamp: seconds since program start
    temp_c, hum = read_dht_with_retry()

    if temp_c is None:
        led.value(0)  # fail safe
        print("All retries failed - no log entry written.")
    else:
        # Optional: keep threshold indicator from Week 5
        led_state = 1 if temp_c > THRESHOLD_C else 0
        led.value(led_state)

        line = f"{ts_s},{temp_c:.1f},{hum:.1f},{led_state}\n"
        try:
            with open(LOG_FILE, "a") as f:
                f.write(line)
            entry_count += 1
            print(f"OK #{entry_count}: ts={ts_s}s temp={temp_c:.1f}C hum={hum:.1f}% LED={led_state}")
        except OSError as e:
            led.value(0)
            print("File write failed:", repr(e))

    time.sleep(LOG_INTERVAL_S)
