import socket
import threading
import json

from document import Document
from core_update import try_update

HOST = "0.0.0.0"
PORT = 5000

document = Document("shared.txt")
document.load()

clients = {}
clients_lock = threading.Lock()


def send_json(conn, message):
    data = (json.dumps(message) + "\n").encode("utf-8")
    conn.sendall(data)


def broadcast(message, exclude=None):
    with clients_lock:
        connections = list(clients.keys())

    for conn in connections:
        if conn is exclude:
            continue
        try:
            send_json(conn, message)
        except OSError:
            remove_client(conn)


def remove_client(conn):
    with clients_lock:
        clients.pop(conn, None)


def handle_client(conn, address):
    print(f"Client connected: {address}")

    with clients_lock:
        clients[conn] = address
        user_count = len(clients)

    content, version = document.get_state()

    try:
        send_json(conn, {
            "type": "sync",
            "content": content,
            "version": version,
            "user_count": user_count
        })
        broadcast({"type": "user_count", "user_count": user_count})

        buffer = ""

        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue

                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    send_json(conn, {
                        "type": "error",
                        "message": "Invalid JSON message."
                    })
                    continue

                message_type = message.get("type")

                if message_type in ("request_sync", "connect"):
                    content, version = document.get_state()
                    with clients_lock:
                        count = len(clients)

                    send_json(conn, {
                        "type": "sync",
                        "content": content,
                        "version": version,
                        "user_count": count
                    })

                elif message_type in ("save", "edit"):
                    base_version = message.get("base_version")
                    new_content = message.get("content", "")

                    if not isinstance(base_version, int):
                        send_json(conn, {
                            "type": "error",
                            "message": "Missing or invalid base_version."
                        })
                        continue

                    accepted, current_content, current_version = try_update(
                        document, base_version, new_content
                    )

                    if not accepted:
                        send_json(conn, {
                            "type": "conflict",
                            "content": current_content,
                            "server_version": current_version
                        })
                        continue

                    send_json(conn, {
                        "type": "save_ack",
                        "version": current_version
                    })

                    broadcast({
                        "type": "update",
                        "content": current_content,
                        "version": current_version,
                        "author": str(address)
                    }, exclude=conn)

                else:
                    send_json(conn, {
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    })

    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        remove_client(conn)
        try:
            conn.close()
        except OSError:
            pass

        with clients_lock:
            user_count = len(clients)

        broadcast({"type": "user_count", "user_count": user_count})
        print(f"Client disconnected: {address}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(20)

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            conn, address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
