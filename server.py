import socket

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, address = server.accept()
    print("Client connected:", address)
    conn.sendall(b"CONNECTED\n")
    conn.close()
