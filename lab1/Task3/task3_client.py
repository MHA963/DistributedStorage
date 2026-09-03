import socket

HOST = "127.0.0.1"
PORT = 9000

def run_client():
    try:
        while True:
            user_input = input("Enter a message to send (Ctrl+C to quit): ")
            # Limit string size to 4kB (4096 bytes)
            data_bytes = user_input.encode("utf-8")[:4096]
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            
            sock.sendall(data_bytes)
            
            response = sock.recv(4096)
            print(f"Server response: {response.decode('utf-8')}\n")
            
            sock.close()
    except KeyboardInterrupt:
        print("\nClient exiting.")

if __name__ == "__main__":
    run_client()