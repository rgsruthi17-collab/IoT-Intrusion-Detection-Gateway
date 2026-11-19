# IoT Intrusion Detection & Traffic Monitoring Gateway

A lightweight, multi-threaded Network Security Gateway built in Python using raw TCP/IP sockets. Designed to protect IoT endpoints against Denial-of-Service (DoS) connection floods and malicious payload injections.

## Key Features
* **Raw TCP/IP Socket Server:** Handles concurrent IoT sensor connections using multi-threading (`socket` & `threading`) without relying on high-level web frameworks.
* **Rate-Limiting (DoS Prevention):** Tracks connection frequency per IP address and blocks traffic exceeding safe thresholds.
* **Deep Packet Inspection (DPI):** Scans incoming TCP payloads against known malicious signatures before processing sensor data.
* **Automated Firewall & Recovery:** Dynamically blocks malicious IPs and restores access automatically after a 15-second cooldown period.
* **Security Audit Logging:** Generates timestamped intrusion logs (`security_audit.log`) for forensic review.

## Project Structure
* `server.py` – Central IoT Gateway with integrated intrusion detection, rate-limiting, and firewall logic.
* `iot_device.py` – Simulates legitimate IoT temperature sensor telemetry over TCP.
* `attacker.py` – Simulates rapid TCP connection floods and malicious payload injection.

## How to Run
1. Start the Security Gateway first:
   ```bash
   python server.py
   ```
2. Start the IoT Sensor Simulator in a second terminal:
   ```bash
   python iot_device.py
   ```
3. Launch the Attack Simulator in a third terminal to test intrusion blocking:
   ```bash
   python attacker.py
   ```
