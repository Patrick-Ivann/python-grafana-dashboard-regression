import json

def log_json(data):
    print(json.dumps(data, indent=2))

def save_to_file(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
