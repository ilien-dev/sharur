import json

cfg = json.loads('{"port": "8080"}')
print(cfg["port"] + 1)
