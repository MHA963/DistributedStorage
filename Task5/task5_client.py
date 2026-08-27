import socket
import sys
import os

HOST = "127.0.0.1"
PORT = 9000

# Protocol Definitions
MESSAGE_STRING   = 1
MESSAGE_DATA_1B  = 2  # up to 255 B
MESSAGE_DATA_2B  = 3  # up to 65,535 B (64 kB)
MESSAGE_DATA_3B  = 4  # up to 16,777,215 B (16 MB)
MESSAGE_DATA_4B  = 5  # up to 4,294,967,295 B (4 GB)

def determine_msg_type_and_header_len(data_len):
    """Selects the smallest header size capable of encoding the payload size."""
    if data_len <= 255:
        return MESSAGE_DATA_1B, 1
    elif data_len <= 65535:
        return MESSAGE_DATA_2B, 2
    elif data_len <= 16777215:
        return MESSAGE_DATA_3B, 3
    elif data_len <= 4294967295:
        return MESSAGE_DATA_4B, 4
    else:
        raise ValueError("Data exceeds maximum 4 GB limit.")

def run_client():
    try:
        while True:
            choice = input("Select message type ([1] String, [2] Binary, [q] Quit): ").strip().lower()
            if choice == 'q':
                break

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            if choice == '1':
                text = input("Enter string: ")
                msg_bytes = text.encode("utf-8")[:4096]
                
                type_hdr = MESSAGE_STRING.to_bytes(1, byteorder=sys.byteorder)
                sock.sendall(type_hdr + msg_bytes)

            elif choice == '2':
                size_str = input("Enter payload size in bytes (e.g. 500, 70000): ").strip()
                byte_count = int(size_str) if size_str.isdigit() else 500
                random_data = os.urandom(byte_count)

                msg_type, header_len = determine_msg_type_and_header_len(byte_count)

                type_hdr = msg_type.to_bytes(1, byteorder=sys.byteorder)
                length_hdr = byte_count.to_bytes(header_len, byteorder=sys.byteorder)

                # Send Type (1B) + Size (1-4B) + Data
                sock.sendall(type_hdr + length_hdr + random_data)
                print(f"Sent Type {msg_type} (header: {header_len}B, payload: {byte_count}B).")

            else:
                print("Invalid selection.")
                sock.close()
                continue

            sock.close()
            print("Connection closed.\n")

    except KeyboardInterrupt:
        print("\nClient exiting.")

if __name__ == "__main__":
    run_client()