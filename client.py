import socket
import threading
import json
import tkinter as tk
from tkinter import messagebox

from client_controls import build_edit_payload
from client_sync import apply_server_update, ClientState


HOST = "127.0.0.1"
PORT = 5000

sock = None
receiver_thread = None
state = ClientState()
send_lock = threading.Lock()


def send_json(message):
    global sock

    if sock is None:
        raise OSError("Not connected to server.")

    data = (json.dumps(message) + "\n").encode("utf-8")

    with send_lock:
        sock.sendall(data)


def set_editor(content):
    editor.config(state="normal")
    editor.delete("1.0", "end")
    editor.insert("1.0", content)
    editor.edit_modified(False)


def update_status(extra=""):
    text = f"{'Connected' if state.connected else 'Disconnected'} | Version: {state.version}"
    if extra:
        text += f" | {extra}"
    status.config(text=text)


def connect():
    global sock, receiver_thread

    if state.connected:
        return

    try:
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.connect((HOST, PORT))
        sock = new_sock
        state.connected = True

        update_status("Connected")

        receiver_thread = threading.Thread(
            target=receive_messages,
            daemon=True
        )
        receiver_thread.start()

        send_json({"type": "request_sync"})

    except OSError as e:
        sock = None
        state.connected = False
        messagebox.showerror("Connection error", str(e))
        update_status()


def disconnect():
    global sock

    state.connected = False

    if sock is not None:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            sock.close()
        except OSError:
            pass

    sock = None
    update_status()


def save_document():
    if not state.connected:
        messagebox.showwarning("Not connected", "Connect to the server first.")
        return

    content = editor.get("1.0", "end-1c")

    try:
        send_json(build_edit_payload(editor, state.version))
        state.local_dirty = False
        update_status("Save sent")
    except OSError as e:
        messagebox.showerror("Save error", str(e))
        disconnect()


def reload_document():
    if not state.connected:
        messagebox.showwarning("Not connected", "Connect to the server first.")
        return

    try:
        send_json({"type": "request_sync"})
    except OSError as e:
        messagebox.showerror("Reload error", str(e))
        disconnect()


def receive_messages():
    global sock

    buffer = ""

    try:
        while state.connected and sock is not None:
            data = sock.recv(4096)

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
                    continue

                root.after(0, handle_message, message)

    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        if state.connected:
            root.after(0, handle_disconnect)


def handle_message(message):
    message_type = message.get("type")

    if message_type == "sync":
        content = message.get("content", "")
        version = message.get("version", 0)

        apply_server_update(editor, content)
        state.version = version
        state.local_dirty = False

        update_status(
            f"Synced | Clients: {message.get('user_count', '?')}"
        )

    elif message_type == "update":
        content = message.get("content", "")
        version = message.get("version", state.version)

        apply_server_update(editor, content)
        state.version = version
        state.local_dirty = False

        update_status("Updated from another client")

    elif message_type == "save_ack":
        state.version = message.get("version", state.version)
        state.local_dirty = False
        update_status("Saved successfully")

    elif message_type == "conflict":
        server_content = message.get("content", "")
        server_version = message.get("server_version", state.version)

        state.version = server_version

        choice = messagebox.askyesno(
            "Conflict detected",
            "Your edit was rejected because another client saved a newer "
            "version.\n\n"
            "Click Yes to load the latest server version."
        )

        if choice:
            apply_server_update(editor, server_content)
            state.local_dirty = False

        update_status("Conflict detected")

    elif message_type == "user_count":
        update_status(f"Clients: {message.get('user_count', 0)}")

    elif message_type == "error":
        messagebox.showerror(
            "Server error",
            message.get("message", "Unknown server error.")
        )


def handle_disconnect():
    state.connected = False
    update_status("Connection lost")


def on_editor_modified(event=None):
    if editor.edit_modified():
        state.local_dirty = True
        editor.edit_modified(False)
        update_status("Unsaved changes")


def on_close():
    disconnect()
    root.destroy()


root = tk.Tk()
root.title("Collaborative Network File System")
root.geometry("900x650")

toolbar = tk.Frame(root)
toolbar.pack(fill="x", padx=10, pady=10)

tk.Button(toolbar, text="Connect", command=connect).pack(side="left", padx=5)
tk.Button(toolbar, text="Disconnect", command=disconnect).pack(side="left", padx=5)
tk.Button(toolbar, text="Save", command=save_document).pack(side="left", padx=5)
tk.Button(toolbar, text="Reload", command=reload_document).pack(side="left", padx=5)

editor = tk.Text(
    root,
    wrap="word",
    font=("Consolas", 12),
    undo=True
)
editor.pack(fill="both", expand=True, padx=10, pady=10)
editor.bind("<<Modified>>", on_editor_modified)

status = tk.Label(
    root,
    text="Disconnected | Version: 0",
    anchor="w"
)
status.pack(fill="x", padx=10, pady=5)

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
