def sync_message(content, version, user_count):
    return {
        "type": "sync",
        "content": content,
        "version": version,
        "user_count": user_count
    }

def update_message(content, version, author):
    return {
        "type": "update",
        "content": content,
        "version": version,
        "author": author
    }

def conflict_message(content, version):
    return {
        "type": "conflict",
        "content": content,
        "server_version": version
    }
