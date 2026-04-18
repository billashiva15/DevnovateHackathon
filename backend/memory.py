"""
backend/memory.py

Purpose:
    This module handles interaction with Hindsight memory API.

What this file does:
    1. Creates a unique memory "bank" for each client
    2. Stores past interactions (message + response + objection)
    3. Retrieves relevant past memories based on a query
    4. Handles API errors and timeouts safely

Why this matters:
    Memory is what makes the AI agent "intelligent over time".
    Instead of responding statelessly, the agent can recall:
        - past objections
        - previous responses
        - client preferences

    This is the core of Hindsight-based learning in your system.
"""

import requests
from backend.config import HINDSIGHT_API_KEY


# -------------------------------------------------------------------
# API Configuration
# -------------------------------------------------------------------
# Base endpoint for Hindsight memory API
BASE_URL = "https://api.hindsight.vectorize.io"

# Common headers for all API requests
HEADERS = {
    "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
    "Content-Type": "application/json",
}


# -------------------------------------------------------------------
# Utility: Bank ID Generator
# -------------------------------------------------------------------

def get_bank_id(client_name: str) -> str:
    """
    Generate a unique memory bank ID for each client.

    Args:
        client_name (str): Name of the client/account.

    Returns:
        str: Normalized bank ID.

    Example:
        Input: "Acme Corp"
        Output: "dealmind_acme_corp"

    Why this matters:
        Each client gets a separate memory space, preventing
        cross-contamination of conversations.
    """
    return f"dealmind_{client_name.strip().lower().replace(' ', '_')}"


# -------------------------------------------------------------------
# Save Interaction to Memory
# -------------------------------------------------------------------

def save_interaction(
    client_name: str,
    message: str,
    response: str,
    objection: str
) -> bool:
    """
    Store a client interaction in Hindsight memory.

    Args:
        client_name (str): Name of the client.
        message (str): User input message.
        response (str): AI-generated response.
        objection (str): Detected objection type.

    Returns:
        bool: True if successfully saved, False otherwise.

    Optimization:
        The response is truncated to reduce storage pressure
        and API load.

    Stored format:
        Message: ...
        Response: ...
        Objection: ...

    Why this matters:
        These stored interactions are later used for semantic recall,
        helping the agent improve future responses.
    """
    bank_id = get_bank_id(client_name)

    # ------------------------------------------------------------
    # Reduce payload size by limiting response length
    # ------------------------------------------------------------
    compact_response = response[:300] if response else ""

    # Payload structure expected by Hindsight API
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
        # Send request to Hindsight API
        res = requests.post(
            f"{BASE_URL}/v1/default/banks/{bank_id}/memories",
            headers=HEADERS,
            json=payload,
            timeout=5,  # prevent hanging requests
        )

        # Success case
        if res.status_code in (200, 201):
            return True

        # Log API error
        print("Memory Save Error:", res.status_code, res.text)
        return False

    except requests.exceptions.Timeout:
        print("Memory Save Timeout")
        return False

    except Exception as e:
        print("Memory Save Exception:", e)
        return False


# -------------------------------------------------------------------
# Retrieve Relevant Memory
# -------------------------------------------------------------------

def get_relevant_memory(
    client_name: str,
    query: str,
    top_k: int = 5
) -> list:
    """
    Retrieve relevant past interactions for a client.

    Args:
        client_name (str): Name of the client.
        query (str): Search query (usually current message).
        top_k (int): Number of top results to return.

    Returns:
        list: List of memory results (dictionaries).

    Flow:
        1. Generate client-specific memory bank ID
        2. Send semantic search query to Hindsight API
        3. Retrieve top matching interactions

    Why this matters:
        Enables semantic recall:
        The agent doesn't just remember exact matches —
        it finds similar past situations.

    Example:
        Query: "too expensive"
        Retrieved memory:
            - Previous pricing objections
            - Past discount discussions
    """
    bank_id = get_bank_id(client_name)

    # Payload for recall API
    payload = {
        "query": query
    }

    try:
        # Send recall request
        res = requests.post(
            f"{BASE_URL}/v1/default/banks/{bank_id}/memories/recall",
            headers=HEADERS,
            json=payload,
            timeout=5,
        )

        # Success case
        if res.status_code == 200:
            return res.json().get("results", [])[:top_k]

        # Log API error
        print("Memory Search Error:", res.status_code, res.text)
        return []

    except requests.exceptions.Timeout:
        print("Memory Search Timeout")
        return []

    except Exception as e:
        print("Memory Fetch Exception:", e)
        return []