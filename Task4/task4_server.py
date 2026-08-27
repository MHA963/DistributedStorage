import socket
import sys
import random
import string

HOST = "127.0.0.1"
PORT = 9000

MESSAGE_TYPE_STRING = 1
MESSAGE_TYPE_BINARY = 2

def write_file(data, filename=None):
    """Write the given data to a local file with the given filename
    :param data: A bytes object that stores the file contents
    :param filename: The file name. If not given, a random string is generated
    :return: The file name of the newly written file, or None if there was an error
    """
    if not filename:
        # Generate random filename
        filename_length = 8
        filename = ''.join([random.SystemRandom().choice(string.ascii_letters +
        string.digits) for n in range(filename_length)])
        # Add '.bin' extension
        filename += ".bin"
    try:
        # Open filename for writing binary content ('wb')
        # note: when a file is opened using the 'with' statement,
        # it is closed automatically when the scope ends
        with open('./'+filename, 'wb') as f:
            f.write(data)
    except EnvironmentError as e:
        print("Error writing file: {}".format(e))
        return None
    return filename
            


def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    server_sock.settimeout(1.0)
    print(f"Task 4 Server listening on {HOST}:{PORT}...")

    try:
        while True:
            try:
                conn, addr = server_sock.accept()
                # Read first byte for the message type
                type_byte = conn.recv(1)
                if not type_byte:
                    conn.close()
                    continue

                msg_type = int.from_bytes(type_byte, byteorder=sys.byteorder)
            except socket.timeout:
                continue

            if msg_type == MESSAGE_TYPE_STRING:
                data = conn.recv(4096)
                print(f"[{addr[0]}] String received: {data.decode('utf-8', errors='replace')}")

            elif msg_type == MESSAGE_TYPE_BINARY:
                # Read until connection closes (0 bytes received)
                chunks = []
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
                
                binary_data = b"".join(chunks)
                saved_name = write_file(binary_data)
                print(f"[{addr[0]}] Binary received ({len(binary_data)} bytes) and saved as '{saved_name}'.")

            else:
                print(f"[{addr[0]}] Unknown message type: {msg_type}")

            conn.close()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_server()