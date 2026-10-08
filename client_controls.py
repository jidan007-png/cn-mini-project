def build_edit_payload(editor, version):
    return {
        "type": "edit",
        "base_version": version,
        "content": editor.get("1.0", "end-1c")
    }

def build_sync_request():
    return {"type": "request_sync"}

def set_status(status_label, version, connected=True):
    state = "Connected" if connected else "Disconnected"
    status_label.config(text=f"{state} | Version: {version}")
