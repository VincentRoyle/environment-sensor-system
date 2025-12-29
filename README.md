# Environment Sensor System

This project is an environment monitoring system built using a Raspberry Pi Pico W as part of a T Level IT Automation & Scripting assignment.

The system was developed incrementally, starting with development environment setup and board verification, followed by sensor integration. Display output was investigated as an extension and evaluated based on hardware limitations.

---

## Hardware Used
- Raspberry Pi Pico W
- DHT22 Temperature & Humidity Sensor
- Breadboard
- Jumper wires
- USB cable

## Software Used
- Thonny IDE
- MicroPython (Pico W firmware)

---

## Project Structure
- **Setup & Orientation** – development environment and board verification
- **Sensor Integration** – reading temperature and humidity data
- **Display Output (Experimental)** – OLED display investigation

---

## Week 1 — Setup & Orientation

### Ticket: Initial Environment & Board Verification

### Description
The aim of this stage was to set up the development environment and confirm that the Raspberry Pi Pico W could be programmed successfully.

### Tasks Completed
- Installed Thonny IDE and configured it for MicroPython development
- Flashed MicroPython firmware onto the Pico W
- Verified USB connection and serial REPL access
- Ran basic test scripts to confirm code execution on the board
- Created the project repository and initial README structure

### Evidence
- Pico W successfully recognised by the system as a serial device
- Code uploaded and executed via Thonny without errors
- REPL output confirmed successful flashing and communication

### Acceptance Criteria Review
- **Board successfully flashed and runs uploaded code:** Achieved
- **Development environment documented:** Achieved
- **Project structure created:** Achieved

### Learning Focus
This stage developed familiarity with the MicroPython flashing workflow, IDE usage, USB serial communication, and basic embedded scripting.

---

## Week 2 — Sensor Integration (DHT22)

### Ticket: Connect and Read Sensor Data

### Description
This stage focused on integrating a DHT22 sensor to capture temperature and humidity readings using the Raspberry Pi Pico W.

### Tasks Completed
- Wired the DHT22 sensor to the Pico W using a breadboard and jumper wires
- Connected sensor power to 3.3V and ground
- Connected the data pin to GPIO15
- Verified the MicroPython `dht` library was available
- Manually retyped and modified a sample script
- Added comments explaining each major step in the code
- Ran the script and captured live readings in the serial console

### Testing Evidence
- Serial console displayed valid temperature (°C) and humidity (%) values
- Readings updated repeatedly over time
- Sensor confirmed to work reliably when tested independently

### Acceptance Criteria Review
- **Console displays valid temperature and humidity values:** Achieved
- **Code is self-commented and saved to repository:** Achieved
- **Circuit wiring documented:** Achieved via annotated photo/diagram

### Learning Focus
This stage improved understanding of GPIO pin mapping, sensor libraries, digital timing requirements, and read–print loops in embedded systems.

---

## Display Output — OLED (Experimental)

### Description
An OLED display was investigated as an output method for sensor readings using the I²C protocol.

### Results
- The OLED device was detected on the I²C bus at address `0x3C`
- Basic I²C communication (address scan and minimal writes) was successful
- Full display initialisation and framebuffer updates were unreliable and resulted in timeout errors (`ETIMEDOUT`, `EIO`)
- The instability caused intermittent system resets and USB disconnections

### Evaluation
The OLED behaviour indicates insufficient I²C signal integrity under load. While the device acknowledges its address, large data transfers required by the display driver fail. This is consistent with weak or missing I²C pull-up resistors and breadboard signal limitations.

### Proposed Improvements
- Add 4.7kΩ–10kΩ pull-up resistors from SDA and SCL to 3.3V
- Shorten I²C wiring paths
- Use a display module with onboard pull-up resistors

Due to time and hardware constraints, serial output was used as the primary data display method.

---

## Conclusion

The Raspberry Pi Pico W environment sensor system successfully reads temperature and humidity data using a DHT22 sensor and outputs reliable results via the serial console.

The project demonstrates effective incremental development, hardware testing, and fault evaluation. While display output was not fully implemented, the issue was investigated, diagnosed, and documented with a clear proposed solution.

---

## Future Work
- Stabilise OLED output using proper I²C pull-up resistors
- Integrate display output with sensor readings
- Extend system with data logging or wireless transmission
