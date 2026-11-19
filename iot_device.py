import socket
import time
import random

HOST = '127.0.0.1'
PORT = 9090

print("[*] Starting Normal IoT Temperature Sensor...")
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        temp = round(random.uniform(24.0, 30.0), 2)
        payload = f"DEVICE_ID:SENSOR_01 | TEMP:{temp}C"
        s.sendall(payload.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        print(f"Sent: {payload} -> Server replied: {response}")
        s.close()
    except Exception as e:
        print("[!] Connection refused or blocked by Gateway.")
    time.sleep(2)
