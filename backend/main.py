"""
backend/main.py

Purpose:
    This module defines the FastAPI backend for DealMind-AI.

What this file does:
    1. Creates the FastAPI application
    2. Defines request schema for chat input
    3. Exposes a health-check/home endpoint
    4. Exposes a /chat endpoint to interact with the sales agent
    5. Exposes a /memory/{client_name} endpoint to inspect recalled memory
    6. Handles backend errors safely

Why this matters:
    This file acts as the API layer of the project. It connects the
    frontend or any external client to the DealMind-AI agent pipeline.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from backend.agent import agent_pipeline
from backend.memory import get_relevant_memory


# -------------------------------------------------------------------
# FastAPI Application
# -------------------------------------------------------------------
# This creates the backend web application.
# The title appears in API docs (/docs).
app = FastAPI(title="DealMind AI Backend")


# -------------------------------------------------------------------
# Request Schema
# -------------------------------------------------------------------
# Pydantic model used to validate incoming chat requests.
# This ensures the API receives structured input.
class ChatRequest(BaseModel):
    """
    Request model for the /chat endpoint.

    Attributes:
        client_name (str): Name of the client/account.
        message (str): Incoming client message to be processed by the agent.
    """
    client_name: str
    message: str


# -------------------------------------------------------------------
# Root Endpoint
# -------------------------------------------------------------------
@app.get("/")
def home():
    """
    Health-check endpoint for the backend.

    Returns:
        dict: Simple success message showing that the backend is running.

    Why this is useful:
        - Confirms the API server is active
        - Useful for deployment testing
        - Helpful when checking browser/API connectivity
    """
    return {"message": "DealMind AI Backend Running 🚀"}


# -------------------------------------------------------------------
# Chat Endpoint
# -------------------------------------------------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    """
    Main API endpoint for generating AI sales responses.

    Args:
        req (ChatRequest): Request body containing:
            - client_name
            - message

    Returns:
        dict: Structured response from the agent pipeline including:
            - AI-generated reply
            - objection type
            - strategy
            - deal context
            - next best action
            - risk flags
            - client profile

    Flow:
        1. Receive structured request from frontend/client
        2. Pass client name and message to agent_pipeline()
        3. Return the enriched response

    Error handling:
        If any exception occurs, the endpoint returns a safe fallback
        response so the frontend does not break.
    """
    try:
        result = agent_pipeline(req.client_name, req.message)
        return result

    except Exception as e:
        # Log the backend error for debugging
        print("CHAT ENDPOINT ERROR:", repr(e))

        # Return a safe fallback response
        return {
            "response": f"Backend error: {str(e)}",
            "objection": "unknown",
            "strategy": "fallback",
            "deal_stage": "Unknown",
            "deal_value": "Unknown",
            "product": "Unknown",
            "sales_agent": "Unknown",
            "next_action": "Check backend logs",
            "risk_flags": [],
            "client_profile": {},
        }


# -------------------------------------------------------------------
# Memory Inspection Endpoint
# -------------------------------------------------------------------
@app.get("/memory/{client_name}")
def get_memory(client_name: str):
    """
    Retrieve recent relevant memory entries for a given client.

    Args:
        client_name (str): Name of the client/account.

    Returns:
        dict: Dictionary with a 'memory' key containing a list of
        recalled memory snippets.

    Flow:
        1. Query memory using the client name
        2. Request top 5 memory results
        3. Keep only the 'content' field for clean API output

    Why this is useful:
        - Helps debug memory retrieval
        - Lets developers inspect stored interactions
        - Makes the system more explainable during demos
    """
    try:
        # Retrieve memory results
        results = get_relevant_memory(client_name, "summary", top_k=5)

        # Keep only clean content for API response
        formatted = []
        for r in results:
            if isinstance(r, dict) and "content" in r:
                formatted.append({"content": r["content"]})

        return {"memory": formatted}

    except Exception as e:
        # Log memory endpoint error
        print("MEMORY ENDPOINT ERROR:", repr(e))

        # Return safe empty structure
        return {"memory": []}

