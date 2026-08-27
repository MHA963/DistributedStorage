import socket

HOST = "127.0.0.1"
PORT = 9000

def run_client():
    print("Press [Enter] to connect to server (Ctrl+C to quit)...")
    try:
        while True:
            input()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            print(f"Successfully connected to {HOST}:{PORT}")
            sock.close()
    except KeyboardInterrupt:
        print("\nExiting client.")

if __name__ == "__main__":
    run_client()