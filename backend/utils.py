# import json
# from datetime import datetime

# def load_json(path):
#     try:
#         with open(path, "r") as f:
#             return json.load(f)
#     except:
#         return {}

# def save_json(path, data):
#     with open(path, "w") as f:
#         json.dump(data, f, indent=4)

# def get_timestamp():
#     return datetime.utcnow().isoformat()

import json
from datetime import datetime


def load_json(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_timestamp() -> str:
    return datetime.utcnow().isoformat()