import socket

HOST = "127.0.0.1"
PORT = 9000

def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Server listening on {HOST}:{PORT}...")

    try:
        while True:
            conn, addr = server_sock.accept()
            print(f"Connected by: {addr}")
            conn.close()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_server()
    