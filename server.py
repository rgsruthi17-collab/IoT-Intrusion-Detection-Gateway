import socket
import threading
import time
from datetime import datetime

HOST = '127.0.0.1'
PORT = 9090

# Security tracking dictionaries
connection_counts = {}
blocked_ips = {}  # Stores {ip: unblock_timestamp}
THRESHOLD = 5     # Max allowed connections per 3 seconds
BAN_DURATION = 15 # Seconds to keep an IP blocked
MALICIOUS_SIGNATURES = ["DROP", "EXEC", "MALICIOUS", "SELECT *", "RM -RF"]

def log_security_event(event_type, ip, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{event_type}] IP: {ip} | {details}\n"
    with open("security_audit.log", "a") as log_file:
        log_file.write(log_entry)

def security_housekeeping():
    """Resets connection counters every 3s and removes expired IP bans."""
    while True:
        time.sleep(3)
        connection_counts.clear()
        
        now = time.time()
        expired = [ip for ip, expiry in blocked_ips.items() if now >= expiry]
        for ip in expired:
            del blocked_ips[ip]
            msg = f"Ban expired after {BAN_DURATION}s. IP restored."
            print(f"[INFO] {msg} -> {ip}")
            log_security_event("IP_UNBLOCKED", ip, msg)

def handle_client(conn, addr):
    ip = addr[0]
    
    # 1. Firewall Check: Drop active blocked IPs
    if ip in blocked_ips:
        conn.close()
        return

    # 2. Rate-Limiting Check (DoS Detection)
    connection_counts[ip] = connection_counts.get(ip, 0) + 1
    if connection_counts[ip] > THRESHOLD:
        msg = f"DoS Flood detected ({connection_counts[ip]} requests/3s). Blocked for {BAN_DURATION}s."
        print(f"\n[ALERT] {msg} -> {ip}")
        log_security_event("DOS_ATTACK", ip, msg)
        blocked_ips[ip] = time.time() + BAN_DURATION
        conn.close()
        return

    # 3. Deep Packet Inspection & Data Processing
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            if any(sig in data.upper() for sig in MALICIOUS_SIGNATURES):
                msg = f"Malicious payload signature detected: '{data}'. Blocked for {BAN_DURATION}s."
                print(f"\n[ALERT] {msg} from {ip}!")
                log_security_event("MALICIOUS_PAYLOAD", ip, msg)
                blocked_ips[ip] = time.time() + BAN_DURATION
                conn.sendall(b"ERR: Malicious Payload Blocked")
                return

            print(f"[DATA] Received from IoT Node ({ip}): {data}")
            conn.sendall(b"ACK: Data Logged")
            
    except Exception:
        pass
    finally:
        conn.close()

def start_server():
    threading.Thread(target=security_housekeeping, daemon=True).start()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"[*] IoT Security Gateway listening on {HOST}:{PORT}...")
    print("[*] Active Defenses: Rate-Limiting, Signature Inspection, Auto-Recovery, Audit Logs\n")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
