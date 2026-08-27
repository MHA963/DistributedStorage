import socket
import sys
import os

HOST = "127.0.0.1"
PORT = 9000

MESSAGE_TYPE_STRING = 1
MESSAGE_TYPE_BINARY = 2

def run_client():
    try:
        while True:
            choice = input("Select message type ([1] String, [2] Binary, [q] Quit): ").strip().lower()
            if choice == 'q':
                break

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            if choice == '1':
                text = input("Enter string to send: ")
                msg_bytes = text.encode("utf-8")[:4096]
                
                type_header = MESSAGE_TYPE_STRING.to_bytes(length=1, byteorder=sys.byteorder)
                sock.sendall(type_header + msg_bytes)
                print(f"Sent string message ({len(msg_bytes)} bytes).")

            elif choice == '2':
                size_str = input("Enter number of random bytes to send (default 5000): ").strip()
                byte_count = int(size_str) if size_str.isdigit() else 5000
                random_data = os.urandom(byte_count)

                type_header = MESSAGE_TYPE_BINARY.to_bytes(length=1, byteorder=sys.byteorder)
                sock.sendall(type_header + random_data)
                print(f"Sent binary payload ({byte_count} bytes).")

            else:
                print("Invalid choice, please select 1 or 2.")
                sock.close()
                continue

            sock.close()
            print("Connection closed.\n")

    except KeyboardInterrupt:
        print("\nClient exiting.")

if __name__ == "__main__":
    run_client()