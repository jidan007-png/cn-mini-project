def try_update(document, base_version, new_content):
    with document.lock:
        if base_version != document.version:
            return False, document.content, document.version

        document.content = new_content
        document.version += 1
        document.save()
        return True, document.content, document.version
