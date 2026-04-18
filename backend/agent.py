# from backend.memory import get_client_memory, save_interaction
# from backend.llm import call_llm

# def detect_objection(text):
#     text = text.lower()
#     if "price" in text or "expensive" in text:
#         return "price"
#     elif "competitor" in text:
#         return "competitor"
#     return "general"


# def build_context(client_name, message, memory):
#     if memory:
#         past_summary = "\n".join(
#             [f"- {m['message']} (objection: {m['objection']})" for m in memory[-5:]]
#         )
#     else:
#         past_summary = "No previous interactions."

#     prompt = f"""
# You are an AI Sales Assistant.

# Client: {client_name}

# Current Message:
# {message}

# Past Interactions:
# {past_summary}

# Instructions:
# - Identify client concerns
# - Reference past objections if available
# - Suggest best response strategy
# - Be concise and actionable
# """

#     return prompt


# def agent_pipeline(client_name, message):
#     memory = get_client_memory(client_name)

#     objection = detect_objection(message)

#     prompt = build_context(client_name, message, memory)

#     response = call_llm(prompt)

#     save_interaction(client_name, message, response, objection)

#     return response



# from backend.memory import get_relevant_memory, save_interaction
# from backend.llm import call_llm


# def detect_objection(message: str) -> str:
#     msg = message.lower()

#     if any(word in msg for word in ["expensive", "cost", "price", "pricing", "budget", "overpriced"]):
#         return "pricing"
#     elif any(word in msg for word in ["not interested", "no need", "not now", "no thanks"]):
#         return "not_interested"
#     elif any(word in msg for word in ["later", "next month", "follow up later", "delay", "not today"]):
#         return "delay"
#     elif any(word in msg for word in ["competitor", "other vendor", "alternative", "another tool", "already using"]):
#         return "competition"
#     else:
#         return "general"


# def get_strategy(objection: str) -> str:
#     strategy_map = {
#         "pricing": "Emphasize ROI, efficiency gains, and long-term value over upfront cost.",
#         "not_interested": "Reconnect the solution to a relevant business pain point and spark curiosity.",
#         "delay": "Reduce commitment and suggest a simple next step with urgency.",
#         "competition": "Differentiate based on business outcomes, fit, and support quality.",
#         "general": "Be consultative, concise, and move the conversation toward the next action.",
#     }
#     return strategy_map.get(objection, "Be persuasive and helpful.")


# def build_memory_context(memories: list) -> str:
#     if not memories:
#         return "No past interactions found."

#     lines = []
#     for item in memories:
#         if isinstance(item, dict) and "content" in item:
#             lines.append(f"- {item['content']}")

#     return "\n".join(lines) if lines else "No past interactions found."


# def agent_pipeline(client_name: str, message: str) -> dict:
#     memories = get_relevant_memory(client_name, message)
#     memory_context = build_memory_context(memories)

#     objection = detect_objection(message)
#     strategy = get_strategy(objection)

#     prompt = f"""
# You are an expert enterprise sales closer.

# Client Name: {client_name}

# Relevant past interactions:
# {memory_context}

# Current client message:
# {message}

# Detected objection:
# {objection}

# Recommended sales strategy:
# {strategy}

# Write a persuasive reply in 2-3 lines only.
# Make it sound natural, professional, and action-oriented.
# Do not include reasoning, bullet points, labels, or thinking tags.
# """

#     response = call_llm(prompt)

#     save_interaction(
#         client_name=client_name,
#         message=message,
#         response=response,
#         objection=objection,
#     )

#     return {
#         "response": response,
#         "objection": objection,
#         "strategy": strategy,
#     }
# from backend.memory import get_relevant_memory, save_interaction
# from backend.llm import call_llm


# def detect_objection(message: str) -> str:
#     msg = message.lower()

#     if any(word in msg for word in ["expensive", "cost", "price", "pricing", "budget", "overpriced"]):
#         return "pricing"
#     elif any(word in msg for word in ["not interested", "no need", "not now", "no thanks"]):
#         return "not_interested"
#     elif any(word in msg for word in ["later", "next month", "follow up later", "delay", "not today"]):
#         return "delay"
#     elif any(word in msg for word in ["competitor", "other vendor", "alternative", "another tool", "already using"]):
#         return "competition"
#     else:
#         return "general"


# def get_strategy(objection: str) -> str:
#     strategy_map = {
#         "pricing": "Emphasize ROI, efficiency gains, and long-term value over upfront cost.",
#         "not_interested": "Reconnect the solution to a relevant business pain point and spark curiosity.",
#         "delay": "Reduce commitment and suggest a simple next step with urgency.",
#         "competition": "Differentiate based on business outcomes, fit, and support quality.",
#         "general": "Be consultative, concise, and move the conversation toward the next action.",
#     }
#     return strategy_map.get(objection, "Be persuasive and helpful.")


# def build_memory_context(memories: list) -> str:
#     if not memories:
#         return "No past interactions found."

#     lines = []
#     for item in memories:
#         if isinstance(item, dict):
#             content = item.get("content")
#             if content:
#                 lines.append(f"- {content}")

#     return "\n".join(lines) if lines else "No past interactions found."


# def agent_pipeline(client_name: str, message: str) -> dict:
#     try:
#         memories = get_relevant_memory(client_name, message)
#     except Exception as e:
#         print("MEMORY RECALL ERROR:", repr(e))
#         memories = []

#     memory_context = build_memory_context(memories)
#     objection = detect_objection(message)
#     strategy = get_strategy(objection)

#     prompt = f"""
# You are an expert enterprise sales closer.

# Client Name: {client_name}

# Relevant past interactions:
# {memory_context}

# Current client message:
# {message}

# Detected objection:
# {objection}

# Recommended sales strategy:
# {strategy}

# Write a persuasive reply in 2-3 lines only.
# Make it sound natural, professional, and action-oriented.
# Do not include reasoning, bullet points, labels, or thinking tags.
# """

#     response = call_llm(prompt)

#     try:
#         save_interaction(
#             client_name=client_name,
#             message=message,
#             response=response,
#             objection=objection,
#         )
#     except Exception as e:
#         print("MEMORY SAVE ERROR:", repr(e))

#     return {
#         "response": response,
#         "objection": objection,
#         "strategy": strategy,
#     }

# from backend.memory import get_relevant_memory, save_interaction
# from backend.llm import call_llm
# from backend.deal_engine import build_deal_context, detect_risk_flags, suggest_next_best_action



# def detect_objection(message: str) -> str:
#     msg = message.lower()

#     if any(word in msg for word in ["expensive", "cost", "price", "pricing", "budget", "overpriced"]):
#         return "pricing"
#     elif any(word in msg for word in ["not interested", "no need", "not now", "no thanks"]):
#         return "not_interested"
#     elif any(word in msg for word in ["later", "next month", "follow up later", "delay", "not today"]):
#         return "delay"
#     elif any(word in msg for word in ["competitor", "other vendor", "alternative", "another tool", "already using"]):
#         return "competition"
#     else:
#         return "general"


# def get_strategy(objection: str) -> str:
#     strategy_map = {
#         "pricing": "Emphasize ROI, efficiency gains, and long-term value over upfront cost.",
#         "not_interested": "Reconnect the solution to a relevant business pain point and spark curiosity.",
#         "delay": "Reduce commitment and suggest a simple next step with urgency.",
#         "competition": "Differentiate based on business outcomes, fit, and support quality.",
#         "general": "Be consultative, concise, and move the conversation toward the next action.",
#     }
#     return strategy_map.get(objection, "Be persuasive and helpful.")


# def build_memory_context(memories: list) -> str:
#     if not memories:
#         return "No past interactions found."

#     lines = []
#     for item in memories:
#         if isinstance(item, dict):
#             content = item.get("content")
#             if content:
#                 lines.append(f"- {content}")

#     return "\n".join(lines) if lines else "No past interactions found."


# def agent_pipeline(client_name: str, message: str) -> dict:
#     try:
#         memories = get_relevant_memory(client_name, message)
#     except Exception:
#         memories = []

#     memory_context = build_memory_context(memories)

#     objection = detect_objection(message)
#     strategy = get_strategy(objection)

#     deal_context = build_deal_context(client_name)
#     risk_flags = detect_risk_flags(deal_context, objection)
#     next_action = suggest_next_best_action(deal_context.get("stage", "Unknown"), objection)

#     prompt = f"""
# You are an expert enterprise sales closer.

# Client Profile:
# - Account: {deal_context.get("account")}
# - Sector: {deal_context.get("sector")}
# - Location: {deal_context.get("office_location")}
# - Revenue: {deal_context.get("revenue")}
# - Employees: {deal_context.get("employees")}

# Current Deal Context:
# - Stage: {deal_context.get("stage")}
# - Product: {deal_context.get("product")}
# - Deal Value: {deal_context.get("deal_value")}
# - Sales Agent: {deal_context.get("sales_agent")}

# Relevant past interactions:
# {memory_context}

# Current client message:
# {message}

# Detected objection:
# {objection}

# Recommended strategy:
# {strategy}

# Suggested next action:
# {next_action}

# Write a persuasive reply in 2-3 lines only.
# Make it sound natural, professional, and action-oriented.
# Do not include reasoning, bullet points, labels, or thinking tags.
# """

#     response = call_llm(prompt)

#     try:
#         save_interaction(client_name, message, response, objection)
#     except Exception:
#         pass

#     return {
#         "response": response,
#         "objection": objection,
#         "strategy": strategy,
#         "deal_stage": deal_context.get("stage"),
#         "deal_value": deal_context.get("deal_value"),
#         "product": deal_context.get("product"),
#         "sales_agent": deal_context.get("sales_agent"),
#         "next_action": next_action,
#         "risk_flags": risk_flags,
#     }


from backend.memory import get_relevant_memory, save_interaction
from backend.llm import call_llm
from backend.deal_engine import (
    build_deal_context,
    detect_risk_flags,
    suggest_next_best_action,
)


def detect_objection(message: str) -> str:
    msg = message.lower()

    if any(word in msg for word in ["expensive", "cost", "price", "pricing", "budget", "overpriced"]):
        return "pricing"
    elif any(word in msg for word in ["not interested", "no need", "not now", "no thanks"]):
        return "not_interested"
    elif any(word in msg for word in ["later", "next month", "follow up later", "delay", "not today"]):
        return "delay"
    elif any(word in msg for word in ["competitor", "other vendor", "alternative", "another tool", "already using"]):
        return "competition"
    else:
        return "general"


def get_strategy(objection: str) -> str:
    strategy_map = {
        "pricing": "Emphasize ROI, efficiency gains, and long-term value over upfront cost.",
        "not_interested": "Reconnect the solution to a relevant business pain point and spark curiosity.",
        "delay": "Reduce commitment and suggest a simple next step with urgency.",
        "competition": "Differentiate based on business outcomes, fit, and support quality.",
        "general": "Be consultative, concise, and move the conversation toward the next action.",
    }
    return strategy_map.get(objection, "Be persuasive and helpful.")


def build_memory_context(memories: list) -> str:
    if not memories:
        return "No past interactions found."

    lines = []
    for item in memories:
        if isinstance(item, dict):
            content = item.get("content")
            if content:
                lines.append(f"- {content}")

    return "\n".join(lines) if lines else "No past interactions found."


def should_save_memory(objection: str, response: str) -> bool:
    """
    Reduce Hindsight load during demo/testing.
    Save only if response is valid and objection is meaningful.
    """
    if not response or response.startswith("LLM Error"):
        return False

    important_objections = {"pricing", "competition", "delay", "not_interested"}
    return objection in important_objections


def agent_pipeline(client_name: str, message: str) -> dict:
    # 1. Recall memory safely
    try:
        memories = get_relevant_memory(client_name, message)
    except Exception as e:
        print("MEMORY RECALL ERROR:", repr(e))
        memories = []

    memory_context = build_memory_context(memories)

    # 2. Detect objection and strategy
    objection = detect_objection(message)
    strategy = get_strategy(objection)

    # 3. Load real deal context from processed dataset
    deal_context = build_deal_context(client_name)

    # 4. Business insights
    risk_flags = detect_risk_flags(deal_context, objection)
    next_action = suggest_next_best_action(
        deal_context.get("stage", "Unknown"),
        objection
    )

    # 5. Build final prompt
    prompt = f"""
You are an expert enterprise sales closer.

Client Profile:
- Account: {deal_context.get("account")}
- Sector: {deal_context.get("sector")}
- Office Location: {deal_context.get("office_location")}
- Revenue: {deal_context.get("revenue")}
- Employees: {deal_context.get("employees")}

Current Deal Context:
- Stage: {deal_context.get("stage")}
- Product: {deal_context.get("product")}
- Deal Value: {deal_context.get("deal_value")}
- Sales Agent: {deal_context.get("sales_agent")}

Relevant past interactions:
{memory_context}

Current client message:
{message}

Detected objection:
{objection}

Recommended strategy:
{strategy}

Suggested next action:
{next_action}

Write a persuasive reply in 2-3 lines only.
Make it sound natural, professional, and action-oriented.
Do not include reasoning, bullet points, labels, or thinking tags.
"""

    # 6. Generate LLM response
    response = call_llm(prompt)

    # 7. Save memory safely and lightly
    if should_save_memory(objection, response):
        try:
            save_interaction(client_name, message, response, objection)
        except Exception as e:
            print("MEMORY SAVE WARNING:", repr(e))

    # 8. Return enriched response
    return {
        "response": response,
        "objection": objection,
        "strategy": strategy,
        "deal_stage": deal_context.get("stage"),
        "deal_value": deal_context.get("deal_value"),
        "product": deal_context.get("product"),
        "sales_agent": deal_context.get("sales_agent"),
        "next_action": next_action,
        "risk_flags": risk_flags,
        "client_profile": {
            "account": deal_context.get("account"),
            "sector": deal_context.get("sector"),
            "office_location": deal_context.get("office_location"),
            "revenue": deal_context.get("revenue"),
            "employees": deal_context.get("employees"),
        },
    }