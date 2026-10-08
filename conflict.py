def accept_edit(current_version, base_version):
    return base_version == current_version

def conflict_message(current_version, base_version):
    return (
        f"Conflict: client version {base_version}; "
        f"server version {current_version}."
    )
