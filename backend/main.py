# from fastapi import FastAPI
# from pydantic import BaseModel
# from backend.agent import agent_pipeline

# app = FastAPI()

# class ChatRequest(BaseModel):
#     client_name: str
#     message: str

# @app.get("/")
# def home():
#     return {"message": "DealMind AI is running"}

# @app.post("/chat")
# def chat(req: ChatRequest):
#     response = agent_pipeline(req.client_name, req.message)
#     return {"response": response}


# from fastapi import FastAPI
# from pydantic import BaseModel
# from backend.agent import agent_pipeline
# from backend.memory import get_relevant_memory

# app = FastAPI(title="DealMind AI Backend")


# class ChatRequest(BaseModel):
#     client_name: str
#     message: str


# @app.get("/")
# def home():
#     return {"message": "DealMind AI Backend Running 🚀"}

# from fastapi import FastAPI
# from pydantic import BaseModel
# from backend.agent import agent_pipeline
# from backend.memory import get_relevant_memory

# app = FastAPI(title="DealMind AI Backend")


# class ChatRequest(BaseModel):
#     client_name: str
#     message: str


# @app.get("/")
# def home():
#     return {"message": "DealMind AI Backend Running 🚀"}


# @app.post("/chat")
# def chat(req: ChatRequest):
#     try:
#         result = agent_pipeline(req.client_name, req.message)
#         return result
#     except Exception as e:
#         print("CHAT ENDPOINT ERROR:", repr(e))
#         return {
#             "response": f"Backend error: {str(e)}",
#             "objection": "unknown",
#             "strategy": "fallback",
#             "deal_stage": "Unknown",
#             "deal_value": "Unknown",
#             "product": "Unknown",
#             "sales_agent": "Unknown",
#             "next_action": "Check backend logs",
#             "risk_flags": [],
#         }


# @app.get("/memory/{client_name}")
# def get_memory(client_name: str):
#     try:
#         results = get_relevant_memory(client_name, "summary", top_k=5)

#         formatted = []
#         for r in results:
#             if isinstance(r, dict) and "content" in r:
#                 formatted.append({"content": r["content"]})

#         return {"memory": formatted}
#     except Exception as e:
#         print("MEMORY ENDPOINT ERROR:", repr(e))
#         return {"memory": []}

from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent import agent_pipeline
from backend.memory import get_relevant_memory

app = FastAPI(title="DealMind AI Backend")


class ChatRequest(BaseModel):
    client_name: str
    message: str


@app.get("/")
def home():
    return {"message": "DealMind AI Backend Running 🚀"}


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = agent_pipeline(req.client_name, req.message)
        return result
    except Exception as e:
        print("CHAT ENDPOINT ERROR:", repr(e))
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


@app.get("/memory/{client_name}")
def get_memory(client_name: str):
    try:
        results = get_relevant_memory(client_name, "summary", top_k=5)

        formatted = []
        for r in results:
            if isinstance(r, dict) and "content" in r:
                formatted.append({"content": r["content"]})

        return {"memory": formatted}
    except Exception as e:
        print("MEMORY ENDPOINT ERROR:", repr(e))
        return {"memory": []}