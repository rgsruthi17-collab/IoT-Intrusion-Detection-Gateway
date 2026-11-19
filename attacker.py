import socket
import time

HOST = '127.0.0.1'
PORT = 9090

print("[!] Launching TCP Connection Flood Attack...")
for i in range(15):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((HOST, PORT))
        s.sendall(b"MALICIOUS_FLOOD_PACKET")
        s.close()
        print(f"Attack packet {i+1} sent.")
    except Exception as e:
        print(f"Packet {i+1} BLOCKED by Gateway Firewall!")
    time.sleep(0.1)
