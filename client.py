import socket
import tkinter as tk
from tkinter import messagebox

HOST = "127.0.0.1"
PORT = 5000

def connect():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        status.config(text=sock.recv(1024).decode().strip())
        sock.close()
    except OSError as e:
        messagebox.showerror("Connection error", str(e))

root = tk.Tk()
root.title("Collaborative Network File System")
root.geometry("800x600")

tk.Button(root, text="Connect", command=connect).pack(pady=5)
editor = tk.Text(root, wrap="word", font=("Consolas", 12))
editor.pack(fill="both", expand=True, padx=10, pady=10)
status = tk.Label(root, text="Disconnected")
status.pack()

root.mainloop()
