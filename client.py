import tkinter as tk

root = tk.Tk()
root.title("Collaborative Network File System")
root.geometry("800x600")

editor = tk.Text(root, wrap="word", font=("Consolas", 12))
editor.pack(fill="both", expand=True, padx=10, pady=10)

status = tk.Label(root, text="Disconnected")
status.pack()

root.mainloop()
