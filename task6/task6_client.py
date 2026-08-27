import socket
import sys
import os

HOST = "127.0.0.1"
PORT = 9000

# Protocol Definitions
MESSAGE_STRING   = 1
MESSAGE_DATA_1B  = 2  # up to 255 B
MESSAGE_DATA_2B  = 3  # up to 64 kB
MESSAGE_DATA_3B  = 4  # up to 16 MB
MESSAGE_DATA_4B  = 5  # up to 4 GB

def determine_msg_type_and_header_len(data_len):
    if data_len <= 255:
        return MESSAGE_DATA_1B, 1
    elif data_len <= 65535:
        return MESSAGE_DATA_2B, 2
    elif data_len <= 16777215:
        return MESSAGE_DATA_3B, 3
    elif data_len <= 4294967295:
        return MESSAGE_DATA_4B, 4
    else:
        raise ValueError("File exceeds 4 GB limit.")

def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}.")

        # Extra Task 1: Re-use the same socket for multiple uploads
        while True:
            user_input = input("Enter file name to upload (or 'q' to quit): ").strip()
            if user_input.lower() == 'q':
                # Notify server before terminating
                type_hdr = MESSAGE_STRING.to_bytes(1, byteorder=sys.byteorder)
                sock.sendall(type_hdr + b"QUIT")
                break

            if not os.path.isfile(user_input):
                print(f"Error: File '{user_input}' does not exist locally.")
                continue

            file_size = os.path.getsize(user_input)
            filename = os.path.basename(user_input)

            # Step 1: Send filename (Type 1 message)
            type_hdr = MESSAGE_STRING.to_bytes(1, byteorder=sys.byteorder)
            sock.sendall(type_hdr + filename.encode("utf-8")[:4096])

            # Wait for "OK" handshake response
            ack = sock.recv(1024)
            if ack != b"OK":
                print(f"Server rejected filename. Got response: {ack}")
                continue

            # Step 2: Send binary payload header (Type + Size)
            msg_type, header_len = determine_msg_type_and_header_len(file_size)
            type_hdr = msg_type.to_bytes(1, byteorder=sys.byteorder)
            size_hdr = file_size.to_bytes(header_len, byteorder=sys.byteorder)
            
            sock.sendall(type_hdr + size_hdr)

            # Stream the file contents in 4kB units over the open socket
            with open(user_input, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    sock.sendall(chunk)

            print(f"Successfully sent '{filename}' ({file_size} bytes).\n")

    except KeyboardInterrupt:
        print("\nClient terminated by user.")
    except (ConnectionResetError, BrokenPipeError):
        print("\nConnection lost with server.")
    finally:
        sock.close()
        print("Socket closed.")

if __name__ == "__main__":
    run_client()