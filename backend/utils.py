
# import json
# from datetime import datetime


# def load_json(path: str):
#     try:
#         with open(path, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {}
#     except json.JSONDecodeError:
#         return {}


# def save_json(path: str, data):
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4)


# def get_timestamp() -> str:
#     return datetime.utcnow().isoformat()


"""
backend/utils.py

Purpose:
    This module provides common utility/helper functions used across the project.

What this file does:
    1. Safely loads JSON data from a file
    2. Saves data into JSON format
    3. Generates standardized timestamps

Why this matters:
    Utility functions reduce code duplication and keep the project clean.
    Instead of rewriting file-handling logic everywhere, we centralize it here.
"""

import json
from datetime import datetime


# -------------------------------------------------------------------
# JSON File Utilities
# -------------------------------------------------------------------

def load_json(path: str):
    """
    Load JSON data from a file safely.

    Args:
        path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
              Returns empty dictionary if file not found or invalid JSON.

    Error Handling:
        - FileNotFoundError → returns {}
        - JSONDecodeError → returns {}

    Why this matters:
        Prevents the application from crashing when:
        - file does not exist
        - file contains invalid JSON
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        # File does not exist
        return {}

    except json.JSONDecodeError:
        # File exists but JSON is invalid/corrupted
        return {}


def save_json(path: str, data):
    """
    Save data to a JSON file.

    Args:
        path (str): Path where the JSON file will be saved.
        data (Any): Data to be written into the file.

    Behavior:
        - Overwrites existing file if it already exists
        - Uses indentation for readability

    Why this matters:
        Ensures consistent JSON formatting across the project.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# -------------------------------------------------------------------
# Time Utility
# -------------------------------------------------------------------

def get_timestamp() -> str:
    """
    Generate a UTC timestamp in ISO format.

    Returns:
        str: Current UTC time in ISO 8601 format.

    Example:
        "2026-04-19T16:45:30.123456"

    Why this matters:
        Useful for:
        - logging events
        - tracking interactions
        - storing time-based records in memory systems
    """
    return datetime.utcnow().isoformat()