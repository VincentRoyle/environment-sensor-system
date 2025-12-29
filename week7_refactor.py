"""
Week 7 — Refactor & Explain

Refactored the sensor/output script into small functions:
- read_sensor(): get temperature & humidity with retry logic
- format_data(): convert readings into a display-friendly string
- display_data(): output to serial and toggle LED threshold indicator
"""

from machine import Pin
import dht
import time

# --------------------
# Configuration
# --------------------
SENSOR_GPIO = 22
THRESHOLD_C = 25.0
READ_INTERVAL_S = 2

RETRY_COUNT = 3
RETRY_DELAY_S = 1

ENABLE_LOGGING = True
LOG_FILE = "dht_log.csv"
LOG_INTERVAL_S = 30  # only used if ENABLE_LOGGING is True


# --------------------
# Hardware setup
# --------------------
sensor = dht.DHT22(Pin(SENSOR_GPIO))
led = Pin("LED", Pin.OUT)


def read_sensor(retries: int = RETRY_COUNT, retry_delay_s: int = RETRY_DELAY_S):
    """
    Read temperature and humidity from the DHT sensor with retries.

    Inputs:
        retries (int): Number of attempts before giving up.
        retry_delay_s (int): Delay between attempts in seconds.

    Outputs:
        (temp_c, hum_pct) tuple of floats if successful, otherwise (None, None).
    """
    for attempt in range(1, retries + 1):
        try:
            sensor.measure()
            temp_c = sensor.temperature()
            hum_pct = sensor.humidity()

            # Basic sanity checks
            if temp_c is None or hum_pct is None:
                raise ValueError("None reading")
            if hum_pct < 0 or hum_pct > 100:
                raise ValueError("Humidity out of range")
            if temp_c < -40 or temp_c > 80:
                raise ValueError("Temp out of range")

            return temp_c, hum_pct

        except Exception as e:
            print(f"Sensor read failed (attempt {attempt}/{retries}): {repr(e)}")
            time.sleep(retry_delay_s)

    return None, None


def format_data(temp_c: float, hum_pct: float, threshold_c: float = THRESHOLD_C):
    """
    Convert sensor values into a human-readable string for output.

    Inputs:
        temp_c (float): Temperature in degrees Celsius.
        hum_pct (float): Humidity percentage.
        threshold_c (float): Threshold used for alert status text.

    Outputs:
        str: One-line formatted status string.
    """
    temp_f = temp_c * (9 / 5) + 32.0
    status = "ALERT" if temp_c > threshold_c else "OK"
    return (
        f"Temp: {temp_c:.1f} C / {temp_f:.1f} F | "
        f"Hum: {hum_pct:.1f} % | "
        f"Threshold: {threshold_c:.1f} C | {status}"
    )


def display_data(message: str, temp_c: float, threshold_c: float = THRESHOLD_C):
    """
    Present the formatted data and update any indicators.

    Inputs:
        message (str): Formatted data string to display.
        temp_c (float): Temperature value used for threshold check.
        threshold_c (float): Threshold which controls the LED indicator.

    Outputs:
        None
    """
    # Serial output
    print(message)

    # Threshold LED indicator
    led.value(1 if temp_c > threshold_c else 0)


def ensure_csv_header(filename: str):
    """
    Ensure the CSV log file exists and has a header row.

    Inputs:
        filename (str): Target CSV file name on Pico filesystem.

    Outputs:
        None
    """
    try:
        with open(filename, "r") as f:
            if f.readline().strip().startswith("ts_s,"):
                return
    except OSError:
        pass

    with open(filename, "w") as f:
        f.write("ts_s,temp_c,hum_pct\n")


def log_data(filename: str, ts_s: int, temp_c: float, hum_pct: float):
    """
    Append a single CSV row to the log file.

    Inputs:
        filename (str): CSV file name.
        ts_s (int): Timestamp in seconds since program start.
        temp_c (float): Temperature in Celsius.
        hum_pct (float): Humidity percentage.

    Outputs:
        None
    """
    with open(filename, "a") as f:
        f.write(f"{ts_s},{temp_c:.1f},{hum_pct:.1f}\n")


def main():
    """
    Main control loop:
    - Reads sensor
    - Formats data
    - Displays data
    - Optionally logs data at a slower interval
    """
    time.sleep(2)  # stabilise sensor after boot

    start_s = time.time()
    last_log_s = -LOG_INTERVAL_S

    if ENABLE_LOGGING:
        ensure_csv_header(LOG_FILE)

    while True:
        now_s = time.time() - start_s

        temp_c, hum_pct = read_sensor()

        if temp_c is None:
            led.value(0)  # fail safe
            print("All retries failed - skipping output/log this cycle.")
        else:
            msg = format_data(temp_c, hum_pct)
            display_data(msg, temp_c)

            if ENABLE_LOGGING and (now_s - last_log_s) >= LOG_INTERVAL_S:
                log_data(LOG_FILE, now_s, temp_c, hum_pct)
                last_log_s = now_s

        time.sleep(READ_INTERVAL_S)


# Run the program
main()
