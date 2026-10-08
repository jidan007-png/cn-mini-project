import json

def encode(message):
    return (json.dumps(message) + "\n").encode("utf-8")

def decode(line):
    return json.loads(line)
