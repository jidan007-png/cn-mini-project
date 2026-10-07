import threading

class Document:
    def __init__(self, path="shared.txt"):
        self.path = path
        self.content = ""
        self.version = 0
        self.lock = threading.Lock()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.content = f.read()
        except FileNotFoundError:
            self.content = "Welcome to the shared document!\n"
            self.save()
        self.version = 1

    def get_state(self):
        with self.lock:
            return self.content, self.version

    def update(self, content):
        with self.lock:
            self.content = content
            self.version += 1
            self.save()

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(self.content)
