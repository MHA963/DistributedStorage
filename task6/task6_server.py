import socket
import sys
import os

HOST = "127.0.0.1"
PORT = 9000

# Protocol Definitions
MESSAGE_STRING   = 1
MESSAGE_DATA_1B  = 2  # 1-byte length (up to 255 B)
MESSAGE_DATA_2B  = 3  # 2-byte length (up to 64 kB)
MESSAGE_DATA_3B  = 4  # 3-byte length (up to 16 MB)
MESSAGE_DATA_4B  = 5  # 4-byte length (up to 4 GB)

HEADER_SIZE_MAP = {
    MESSAGE_DATA_1B: 1,
    MESSAGE_DATA_2B: 2,
    MESSAGE_DATA_3B: 3,
    MESSAGE_DATA_4B: 4,
}

def recv_exact(sock, num_bytes):
    """Reliably receives exactly num_bytes across TCP stream chunks."""
    buffer = bytearray()
    while len(buffer) < num_bytes:
        chunk = sock.recv(min(4096, num_bytes - len(buffer)))
        if not chunk:
            return None
        buffer.extend(chunk)
    return bytes(buffer)

def handle_client(conn, addr):
    print(f"[{addr[0]}] Connected. Ready for file transfers.")
    try:
        while True:

            # 1. Read message type header for filename / string
            type_byte = conn.recv(1)
            if not type_byte:
                break  # Client closed connection

            msg_type = int.from_bytes(type_byte, byteorder=sys.byteorder)

            # Check for termination command or normal filename
            if msg_type != MESSAGE_STRING:
                print(f"[{addr[0]}] Expected filename (Type 1), got {msg_type}.")
                break

            # Read filename (limit 4kB)
            filename_data = conn.recv(4096)
            if not filename_data:
                break

            raw_filename = filename_data.decode("utf-8", errors="replace").strip()
            if raw_filename == "QUIT":
                print(f"[{addr[0]}] Client requested session close.")
                break

            # Sanitize filename
            filename = os.path.basename(raw_filename)
            print(f"[{addr[0]}] Target file requested: '{filename}'")

            # Create file immediately on server (Extra Task 2)
            target_path = f"server_storage_{filename}"
            
            # Send handshake OK back to client
            conn.sendall(b"OK")

            # 2. Read next message type header (File data payload)
            type_byte = conn.recv(1)
            if not type_byte:
                break

            msg_type = int.from_bytes(type_byte, byteorder=sys.byteorder)
            if msg_type not in HEADER_SIZE_MAP:
                print(f"[{addr[0]}] Expected data message type (2-5), got {msg_type}.")
                break

            header_len = HEADER_SIZE_MAP[msg_type]
            size_bytes = recv_exact(conn, header_len)
            if not size_bytes:
                print(f"[{addr[0]}] Error reading file payload length.")
                break

            expected_size = int.from_bytes(size_bytes, byteorder=sys.byteorder)
            print(f"[{addr[0]}] Receiving '{filename}' ({expected_size} bytes, {header_len}B size header)...")

            # Extra Task 2: Stream incoming chunks directly into the file
            received_bytes = 0
            with open(target_path, "wb") as f:
                while received_bytes < expected_size:
                    chunk_size = min(4096, expected_size - received_bytes)
                    chunk = conn.recv(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    received_bytes += len(chunk)

            if received_bytes == expected_size:
                print(f"[{addr[0]}] Successfully saved '{target_path}'.\n")
            else:
                print(f"[{addr[0]}] Transfer incomplete ({received_bytes}/{expected_size} bytes).\n")

    except (ConnectionResetError, BrokenPipeError):
        print(f"[{addr[0]}] Connection abruptly dropped.")
    finally:
        conn.close()
        print(f"[{addr[0]}] Session terminated.\n")

def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    server_sock.settimeout(1.0)
    print(f"Server listening on {HOST}:{PORT}...")

    try:
        while True:
            try:
                conn, addr = server_sock.accept()
            except socket.timeout:
                continue
            handle_client(conn, addr)
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_server()