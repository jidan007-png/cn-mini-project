import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

def handle_client(conn, address):
    print("Client connected:", address)
    try:
        conn.sendall(b"CONNECTED\n")
    finally:
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(20)

print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, address = server.accept()
    threading.Thread(
        target=handle_client,
        args=(conn, address),
        daemon=True
    ).start()
