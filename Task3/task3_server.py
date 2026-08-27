import socket

HOST = "127.0.0.1"
PORT = 9000

def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"Task 3 Server listening on {HOST}:{PORT}...")
    server_sock.settimeout(1.0)

    try:
        while True:
            try:
                conn, addr = server_sock.accept()
                print(f"Connected by: {addr}")
                conn.close()
            except socket.timeout:
                continue
            # Receive up to 4096 bytes
            data = conn.recv(4096)
        
            if data:
                message = data.decode("utf-8")
                print(f"[{addr[0]}] Received message: {message}")
                
                response = f"Message: {message}"
                conn.sendall(response.encode("utf-8"))
            conn.close()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_server()