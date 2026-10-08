def make_edit_message(content, version):
    return {
        "type": "edit",
        "base_version": version,
        "content": content
    }

def apply_server_update(editor, content):
    editor.delete("1.0", "end")
    editor.insert("1.0", content)

class ClientState:
    def __init__(self):
        self.version = 0
        self.connected = False
        self.local_dirty = False
