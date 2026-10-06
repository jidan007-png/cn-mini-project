class Document:
    def __init__(self, path="shared.txt"):
        self.path = path
        self.content = ""

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.content = f.read()
        except FileNotFoundError:
            self.content = "Welcome to the shared document!\n"
            self.save()

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(self.content)

    def get(self):
        return self.content

    def set(self, content):
        self.content = content
        self.save()
