# import requests
# from backend.config import HINDSIGHT_API_KEY

# BASE_URL = "https://api.hindsight.vectorize.io"

# HEADERS = {
#     "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
#     "Content-Type": "application/json"
# }


# def get_collection(client_name):
#     return f"dealmind_{client_name.replace(' ', '_')}"


# # ---------------- SAVE ---------------- #
# def save_interaction(client_name, message, response, objection):
#     collection = get_collection(client_name)

#     data = {
#         "collection": collection,
#         "content": f"""
# Client: {message}
# Response: {response}
# Objection: {objection}
# """
#     }

#     try:
#         requests.post(
#             f"{BASE_URL}/memory",
#             headers=HEADERS,
#             json=data
#         )
#     except Exception as e:
#         print("Memory Save Error:", e)


# # ---------------- RETRIEVE ---------------- #
# def get_relevant_memory(client_name, query):
#     collection = get_collection(client_name)

#     data = {
#         "collection": collection,
#         "query": query,
#         "top_k": 5
#     }

#     try:
#         response = requests.post(
#             f"{BASE_URL}/search",
#             headers=HEADERS,
#             json=data
#         )

#         if response.status_code == 200:
#             return response.json().get("results", [])
#         else:
#             print("Search Error:", response.text)
#             return []

#     except Exception as e:
#         print("Memory Fetch Error:", e)
#         return []


# import requests
# from backend.config import HINDSIGHT_API_KEY

# BASE_URL = "https://api.hindsight.vectorize.io"

# HEADERS = {
#     "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
#     "Content-Type": "application/json",
# }


# def get_collection(client_name: str) -> str:
#     safe_name = client_name.strip().lower().replace(" ", "_")
#     return f"dealmind_{safe_name}"


# def save_interaction(client_name: str, message: str, response: str, objection: str) -> bool:
#     collection = get_collection(client_name)

#     data = {
#         "collection": collection,
#         "content": (
#             f"Client Name: {client_name}\n"
#             f"Client Message: {message}\n"
#             f"Agent Response: {response}\n"
#             f"Objection Type: {objection}"
#         ),
#     }

#     try:
#         res = requests.post(
#             f"{BASE_URL}/memory",
#             headers=HEADERS,
#             json=data,
#             timeout=10,
#         )

#         if res.status_code in [200, 201]:
#             return True

#         print("Memory Save Error:", res.status_code, res.text)
#         return False

#     except Exception as e:
#         print("Memory Save Exception:", e)
#         return False


# def get_relevant_memory(client_name: str, query: str, top_k: int = 5) -> list:
#     collection = get_collection(client_name)

#     data = {
#         "collection": collection,
#         "query": query,
#         "top_k": top_k,
#     }

#     try:
#         res = requests.post(
#             f"{BASE_URL}/search",
#             headers=HEADERS,
#             json=data,
#             timeout=10,
#         )

#         if res.status_code == 200:
#             return res.json().get("results", [])

#         print("Memory Search Error:", res.status_code, res.text)
#         return []

#     except Exception as e:
#         print("Memory Fetch Exception:", e)
#         return []

# import requests
# from backend.config import HINDSIGHT_API_KEY

# BASE_URL = "https://api.hindsight.vectorize.io"
# HEADERS = {
#     "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
#     "Content-Type": "application/json",
# }


# def get_bank_id(client_name: str) -> str:
#     return f"dealmind_{client_name.strip().lower().replace(' ', '_')}"


# def save_interaction(client_name: str, message: str, response: str, objection: str) -> bool:
#     bank_id = get_bank_id(client_name)

#     payload = {
#         "items": [
#             {
#                 "content": (
#                     f"Client Name: {client_name}\n"
#                     f"Client Message: {message}\n"
#                     f"Agent Response: {response}\n"
#                     f"Objection Type: {objection}"
#                 ),
#                 "tags": [f"client:{client_name.strip().lower().replace(' ', '_')}"]
#             }
#         ]
#     }

#     try:
#         res = requests.post(
#             f"{BASE_URL}/v1/default/banks/{bank_id}/memories",
#             headers=HEADERS,
#             json=payload,
#             timeout=15,
#         )

#         if res.status_code in (200, 201):
#             return True

#         print("Memory Save Error:", res.status_code, res.text)
#         return False

#     except Exception as e:
#         print("Memory Save Exception:", e)
#         return False


# def get_relevant_memory(client_name: str, query: str, top_k: int = 5) -> list:
#     bank_id = get_bank_id(client_name)

#     payload = {
#         "query": query,
#         "tags": [f"client:{client_name.strip().lower().replace(' ', '_')}"],
#         "tags_match": "any"
#     }

#     try:
#         res = requests.post(
#             f"{BASE_URL}/v1/default/banks/{bank_id}/memories/recall",
#             headers=HEADERS,
#             json=payload,
#             timeout=15,
#         )

#         if res.status_code == 200:
#             return res.json().get("results", [])[:top_k]

#         print("Memory Search Error:", res.status_code, res.text)
#         return []

#     except Exception as e:
#         print("Memory Fetch Exception:", e)
#         return []


# import requests
# from backend.config import HINDSIGHT_API_KEY

# BASE_URL = "https://api.hindsight.vectorize.io"
# HEADERS = {
#     "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
#     "Content-Type": "application/json",
# }

# def get_bank_id(client_name: str) -> str:
#     return f"dealmind_{client_name.strip().lower().replace(' ', '_')}"

# def get_relevant_memory(client_name: str, query: str, top_k: int = 5) -> list:
#     bank_id = get_bank_id(client_name)

#     payload = {
#         "query": query
#     }

#     try:
#         res = requests.post(
#             f"{BASE_URL}/v1/default/banks/{bank_id}/memories/recall",
#             headers=HEADERS,
#             json=payload,
#             timeout=5,
#         )

#         if res.status_code == 200:
#             return res.json().get("results", [])[:top_k]

#         print("Memory Search Error:", res.status_code, res.text)
#         return []

#     except requests.exceptions.Timeout:
#         print("Memory Search Timeout")
#         return []
#     except Exception as e:
#         print("Memory Fetch Exception:", e)
#         return []

# def save_interaction(client_name: str, message: str, response: str, objection: str) -> bool:
#     bank_id = get_bank_id(client_name)

#     payload = {
#         "items": [
#             {
#                 "content": (
#                     f"Client Name: {client_name}\n"
#                     f"Client Message: {message}\n"
#                     f"Agent Response: {response}\n"
#                     f"Objection Type: {objection}"
#                 )
#             }
#         ]
#     }

#     try:
#         res = requests.post(
#             f"{BASE_URL}/v1/default/banks/{bank_id}/memories",
#             headers=HEADERS,
#             json=payload,
#             timeout=5,
#         )

#         if res.status_code in (200, 201):
#             return True

#         print("Memory Save Error:", res.status_code, res.text)
#         return False

#     except requests.exceptions.Timeout:
#         print("Memory Save Timeout")
#         return False
#     except Exception as e:
#         print("Memory Save Exception:", e)
#         return False

import requests
from backend.config import HINDSIGHT_API_KEY

BASE_URL = "https://api.hindsight.vectorize.io"
HEADERS = {
    "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
    "Content-Type": "application/json",
}


def get_bank_id(client_name: str) -> str:
    return f"dealmind_{client_name.strip().lower().replace(' ', '_')}"


def save_interaction(client_name: str, message: str, response: str, objection: str) -> bool:
    bank_id = get_bank_id(client_name)

    # Keep stored text compact to reduce pressure
    compact_response = response[:300] if response else ""

    payload = {
        "items": [
            {
                "content": (
                    f"Message: {message}\n"
                    f"Response: {compact_response}\n"
                    f"Objection: {objection}"
                )
            }
        ]
    }

    try:
        res = requests.post(
            f"{BASE_URL}/v1/default/banks/{bank_id}/memories",
            headers=HEADERS,
            json=payload,
            timeout=5,
        )

        if res.status_code in (200, 201):
            return True

        print("Memory Save Error:", res.status_code, res.text)
        return False

    except requests.exceptions.Timeout:
        print("Memory Save Timeout")
        return False
    except Exception as e:
        print("Memory Save Exception:", e)
        return False


def get_relevant_memory(client_name: str, query: str, top_k: int = 5) -> list:
    bank_id = get_bank_id(client_name)

    payload = {
        "query": query
    }

    try:
        res = requests.post(
            f"{BASE_URL}/v1/default/banks/{bank_id}/memories/recall",
            headers=HEADERS,
            json=payload,
            timeout=5,
        )

        if res.status_code == 200:
            return res.json().get("results", [])[:top_k]

        print("Memory Search Error:", res.status_code, res.text)
        return []

    except requests.exceptions.Timeout:
        print("Memory Search Timeout")
        return []
    except Exception as e:
        print("Memory Fetch Exception:", e)
        return []