
# from backend.memory import get_relevant_memory, save_interaction
# from backend.llm import call_llm
# from backend.deal_engine import (
#     build_deal_context,
#     detect_risk_flags,
#     suggest_next_best_action,
# )


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


# def should_save_memory(objection: str, response: str) -> bool:
#     """
#     Reduce Hindsight load during demo/testing.
#     Save only if response is valid and objection is meaningful.
#     """
#     if not response or response.startswith("LLM Error"):
#         return False

#     important_objections = {"pricing", "competition", "delay", "not_interested"}
#     return objection in important_objections


# def agent_pipeline(client_name: str, message: str) -> dict:
#     # 1. Recall memory safely
#     try:
#         memories = get_relevant_memory(client_name, message)
#     except Exception as e:
#         print("MEMORY RECALL ERROR:", repr(e))
#         memories = []

#     memory_context = build_memory_context(memories)

#     # 2. Detect objection and strategy
#     objection = detect_objection(message)
#     strategy = get_strategy(objection)

#     # 3. Load real deal context from processed dataset
#     deal_context = build_deal_context(client_name)

#     # 4. Business insights
#     risk_flags = detect_risk_flags(deal_context, objection)
#     next_action = suggest_next_best_action(
#         deal_context.get("stage", "Unknown"),
#         objection
#     )

#     # 5. Build final prompt
#     prompt = f"""
# You are an expert enterprise sales closer.

# Client Profile:
# - Account: {deal_context.get("account")}
# - Sector: {deal_context.get("sector")}
# - Office Location: {deal_context.get("office_location")}
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

#     # 6. Generate LLM response
#     response = call_llm(prompt)

#     # 7. Save memory safely and lightly
#     if should_save_memory(objection, response):
#         try:
#             save_interaction(client_name, message, response, objection)
#         except Exception as e:
#             print("MEMORY SAVE WARNING:", repr(e))

#     # 8. Return enriched response
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
#         "client_profile": {
#             "account": deal_context.get("account"),
#             "sector": deal_context.get("sector"),
#             "office_location": deal_context.get("office_location"),
#             "revenue": deal_context.get("revenue"),
#             "employees": deal_context.get("employees"),
#         },
#     }

"""
backend/agent.py

Purpose:
    This module acts as the core decision layer for the DealMind-AI sales agent.

What this file does:
    1. Recalls relevant past client interactions from memory
    2. Detects the type of objection in the client message
    3. Chooses an appropriate response strategy
    4. Builds current deal context from business data
    5. Detects sales risk flags
    6. Suggests the next best sales action
    7. Sends a prompt to the LLM to generate a persuasive reply
    8. Optionally stores useful interactions back into memory

Why this matters:
    This pipeline helps the sales agent behave more intelligently by combining:
    - memory recall
    - deal intelligence
    - objection handling
    - LLM-based response generation
"""

from backend.memory import get_relevant_memory, save_interaction
from backend.llm import call_llm
from backend.deal_engine import (
    build_deal_context,
    detect_risk_flags,
    suggest_next_best_action,
)


def detect_objection(message: str) -> str:
    """
    Detect the type of objection present in the client message.

    Args:
        message (str): The latest message received from the client.

    Returns:
        str: One of the following objection categories:
            - "pricing"
            - "not_interested"
            - "delay"
            - "competition"
            - "general"

    Logic:
        The function performs simple keyword-based rule matching.
        It converts the message to lowercase and checks whether
        specific words or phrases appear in the text.

    Example:
        Input: "This looks too expensive for our budget"
        Output: "pricing"
    """
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
    """
    Map an objection type to a persuasive response strategy.

    Args:
        objection (str): Detected objection category.

    Returns:
        str: A short strategic instruction to guide the LLM response.

    Purpose:
        Instead of responding randomly, the agent uses objection-aware
        strategy selection so the generated reply aligns with the
        client’s concern.
    """
    strategy_map = {
        "pricing": "Emphasize ROI, efficiency gains, and long-term value over upfront cost.",
        "not_interested": "Reconnect the solution to a relevant business pain point and spark curiosity.",
        "delay": "Reduce commitment and suggest a simple next step with urgency.",
        "competition": "Differentiate based on business outcomes, fit, and support quality.",
        "general": "Be consultative, concise, and move the conversation toward the next action.",
    }

    return strategy_map.get(objection, "Be persuasive and helpful.")


def build_memory_context(memories: list) -> str:
    """
    Convert recalled memory items into a readable bullet-style context block.

    Args:
        memories (list): List of recalled memory records.
                         Each record is expected to be a dictionary
                         containing a 'content' key.

    Returns:
        str: A formatted string summarizing past interactions.

    Example output:
        - Client previously asked for discount options
        - They preferred a cloud-based deployment
    """
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
    Decide whether the current interaction should be stored in memory.

    Args:
        objection (str): Detected objection type.
        response (str): LLM-generated response.

    Returns:
        bool: True if the interaction is worth saving, otherwise False.

    Why this function exists:
        Saving every single conversation to memory can overload the
        memory system during demos or testing. This function keeps
        memory selective and efficient.

    Save conditions:
        - The response must not be empty
        - The response must not be an LLM error
        - The objection must be one of the important business objections
    """
    if not response or response.startswith("LLM Error"):
        return False

    important_objections = {"pricing", "competition", "delay", "not_interested"}
    return objection in important_objections


def agent_pipeline(client_name: str, message: str) -> dict:
    """
    Main orchestration pipeline for the sales agent.

    Args:
        client_name (str): Name of the client or account.
        message (str): Current incoming client message.

    Returns:
        dict: A structured response containing:
            - generated sales reply
            - objection type
            - selected strategy
            - deal insights
            - suggested next action
            - detected risk flags
            - client profile information

    Full pipeline steps:
        1. Recall relevant memory for the client
        2. Detect objection type from message
        3. Select persuasive strategy
        4. Build live deal context from processed data
        5. Detect risk flags
        6. Recommend next best action
        7. Create final LLM prompt
        8. Generate response
        9. Save useful interaction to memory
        10. Return enriched structured result
    """

    # ------------------------------------------------------------
    # 1. Recall memory safely
    # ------------------------------------------------------------
    # The agent tries to retrieve relevant past interactions
    # for this client from Hindsight memory or another memory layer.
    try:
        memories = get_relevant_memory(client_name, message)
    except Exception as e:
        print("MEMORY RECALL ERROR:", repr(e))
        memories = []

    # Convert recalled memory into prompt-friendly text
    memory_context = build_memory_context(memories)

    # ------------------------------------------------------------
    # 2. Detect objection and choose response strategy
    # ------------------------------------------------------------
    objection = detect_objection(message)
    strategy = get_strategy(objection)

    # ------------------------------------------------------------
    # 3. Load current deal context from processed business data
    # ------------------------------------------------------------
    # This provides account-level context like sector, stage, product,
    # revenue, employees, and assigned sales agent.
    deal_context = build_deal_context(client_name)

    # ------------------------------------------------------------
    # 4. Generate business insights
    # ------------------------------------------------------------
    # Risk flags warn the system about deal threats.
    # Next action suggests what the seller should do next.
    risk_flags = detect_risk_flags(deal_context, objection)
    next_action = suggest_next_best_action(
        deal_context.get("stage", "Unknown"),
        objection
    )

    # ------------------------------------------------------------
    # 5. Build the final LLM prompt
    # ------------------------------------------------------------
    # The LLM receives:
    # - client profile
    # - deal context
    # - past memory
    # - current message
    # - objection type
    # - strategy
    # - suggested next action
    #
    # This makes the response more personalized and sales-aware.
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

    # ------------------------------------------------------------
    # 6. Generate response using the LLM
    # ------------------------------------------------------------
    response = call_llm(prompt)

    # ------------------------------------------------------------
    # 7. Save useful interaction into memory
    # ------------------------------------------------------------
    # Only important interactions are stored to reduce unnecessary load.
    if should_save_memory(objection, response):
        try:
            save_interaction(client_name, message, response, objection)
        except Exception as e:
            print("MEMORY SAVE WARNING:", repr(e))

    # ------------------------------------------------------------
    # 8. Return structured output
    # ------------------------------------------------------------
    # This is useful for frontend display, debugging, analytics,
    # and future expansion of the system.
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