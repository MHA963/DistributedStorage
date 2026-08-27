import socket
import sys
import random
import string

HOST = "127.0.0.1"
PORT = 9000

# Protocol Definitions
MESSAGE_STRING   = 1
MESSAGE_DATA_1B  = 2  # 1 byte length (up to 255 B)
MESSAGE_DATA_2B  = 3  # 2 byte length (up to 64 kB)
MESSAGE_DATA_3B  = 4  # 3 byte length (up to 16 MB)
MESSAGE_DATA_4B  = 5  # 4 byte length (up to 4 GB)

# Map message types to their size header length
HEADER_SIZE_MAP = {
    MESSAGE_DATA_1B: 1,
    MESSAGE_DATA_2B: 2,
    MESSAGE_DATA_3B: 3,
    MESSAGE_DATA_4B: 4,
}

def recv_exact(sock, num_bytes):
    """Reliably receives exactly num_bytes across multiple TCP chunks."""
    buffer = bytearray()
    while len(buffer) < num_bytes:
        chunk = sock.recv(min(4096, num_bytes - len(buffer)))
        if not chunk:
            return None  # Premature EOF/disconnect
        buffer.extend(chunk)
    return bytes(buffer)

def write_file(data, filename=None):
    if filename is None:
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f"received_{random_suffix}.bin"
    with open(filename, "wb") as f:
        f.write(data)
    return filename

def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"Task 5 Server listening on {HOST}:{PORT}...")
    server_sock.settimeout(1.0)


    try:
        while True:
            try:
                conn, addr = server_sock.accept()
            except socket.timeout:
                continue
            
            # 1. Read the 1-byte message type identifier
            type_byte = conn.recv(1)
            if not type_byte:
                conn.close()
                continue

            msg_type = int.from_bytes(type_byte, byteorder=sys.byteorder)

            # Handle Type 1: String
            if msg_type == MESSAGE_STRING:
                data = conn.recv(4096)
                print(f"[{addr[0]}] String received: {data.decode('utf-8', errors='replace')}")

            # Handle Data Message Types: 2, 3, 4, 5
            elif msg_type in HEADER_SIZE_MAP:
                header_len = HEADER_SIZE_MAP[msg_type]
                size_bytes = recv_exact(conn, header_len)
                
                if not size_bytes:
                    print(f"[{addr[0]}] Error reading length header.")
                    conn.close()
                    continue

                expected_size = int.from_bytes(size_bytes, byteorder=sys.byteorder)
                print(f"[{addr[0]}] Type {msg_type}: Expecting {expected_size} bytes ({header_len}-byte header)...")

                # Receive exact payload
                binary_data = recv_exact(conn, expected_size)
                
                # Verify complete delivery before saving
                if binary_data is not None and len(binary_data) == expected_size:
                    saved_name = write_file(binary_data)
                    print(f"[{addr[0]}] Verified & saved {len(binary_data)} bytes as '{saved_name}'.")
                else:
                    print(f"[{addr[0]}] Incomplete transfer. Expected {expected_size} bytes, got {len(binary_data) if binary_data else 0} bytes.")

            else:
                print(f"[{addr[0]}] Unknown message type: {msg_type}")

            conn.close()

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_server()