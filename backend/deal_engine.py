# from typing import Dict, List

# from backend.data_loader import get_latest_client_record


# def detect_deal_stage(record: Dict) -> str:
#     if not record:
#         return "Unknown"

#     for key in ["deal_stage", "stage", "sales_stage", "opportunity_stage"]:
#         value = record.get(key)
#         if value not in [None, ""]:
#             return str(value)

#     return "Unknown"


# def get_deal_value(record: Dict):
#     if not record:
#         return "Unknown"

#     for key in ["close_value", "deal_value", "amount", "opportunity_value"]:
#         value = record.get(key)
#         if value not in [None, ""]:
#             return value

#     return "Unknown"


# def get_product_name(record: Dict) -> str:
#     if not record:
#         return "Unknown"

#     return str(record.get("product", "Unknown"))


# def detect_risk_flags(record: Dict, objection: str) -> List[str]:
#     risks: List[str] = []

#     stage = detect_deal_stage(record).lower()
#     deal_value = get_deal_value(record)

#     if objection == "pricing":
#         risks.append("pricing_pressure")

#     if "negotiation" in stage:
#         risks.append("late_stage_pressure")

#     if deal_value != "Unknown":
#         try:
#             if float(deal_value) > 10000:
#                 risks.append("high_value_deal")
#         except (ValueError, TypeError):
#             pass

#     return risks


# def suggest_next_best_action(stage: str, objection: str) -> str:
#     stage = stage.lower()

#     if objection == "pricing":
#         return "Share ROI summary and offer a pricing walkthrough"
#     if objection == "competition":
#         return "Send differentiation points and customer proof"
#     if objection == "delay":
#         return "Propose a smaller pilot or a time-boxed next step"
#     if objection == "not_interested":
#         return "Reconnect to their business pain and ask a discovery question"

#     if "prospecting" in stage:
#         return "Qualify needs and schedule a discovery discussion"
#     if "qualification" in stage:
#         return "Clarify pain points and decision criteria"
#     if "proposal" in stage:
#         return "Send a tailored proposal with business value summary"
#     if "negotiation" in stage:
#         return "Address objections and align on final commercial terms"
#     if "closed" in stage:
#         return "Confirm the outcome and document the deal status"

#     return "Move the deal to the next clear action"


# def build_deal_context(client_name: str) -> Dict:
#     record = get_latest_client_record(client_name)

#     if not record:
#         return {
#             "account": client_name,
#             "stage": "Unknown",
#             "product": "Unknown",
#             "deal_value": "Unknown",
#             "sales_agent": "Unknown",
#             "sector": "Unknown",
#             "office_location": "Unknown",
#             "revenue": "Unknown",
#             "employees": "Unknown",
#         }

#     return {
#         "account": record.get("account", client_name),
#         "stage": detect_deal_stage(record),
#         "product": get_product_name(record),
#         "deal_value": get_deal_value(record),
#         "sales_agent": record.get("sales_agent", "Unknown"),
#         "sector": record.get("sector", "Unknown"),
#         "office_location": record.get("office_location", "Unknown"),
#         "revenue": record.get("revenue", "Unknown"),
#         "employees": record.get("employees", "Unknown"),
#     }


"""
backend/deal_engine.py

Purpose:
    This module provides business intelligence logic for DealMind-AI.

What this file does:
    1. Extracts key deal attributes (stage, value, product)
    2. Detects risk signals in the deal
    3. Suggests the next best sales action
    4. Builds a structured deal context for the AI agent

Why this matters:
    The LLM alone is not enough for decision-making.
    This module adds structured business logic so the agent behaves
    like a real sales expert instead of just a chatbot.
"""

from typing import Dict, List

from backend.data_loader import get_latest_client_record


# -------------------------------------------------------------------
# Deal Attribute Extraction
# -------------------------------------------------------------------

def detect_deal_stage(record: Dict) -> str:
    """
    Extract the deal stage from a client record.

    Args:
        record (Dict): Client record dictionary.

    Returns:
        str: Deal stage (e.g., 'Prospecting', 'Negotiation', etc.)
             Returns "Unknown" if not found.

    Logic:
        The function checks multiple possible column names because
        datasets may use different naming conventions.

    Example:
        record = {"sales_stage": "Negotiation"}
        Output: "Negotiation"
    """
    if not record:
        return "Unknown"

    for key in ["deal_stage", "stage", "sales_stage", "opportunity_stage"]:
        value = record.get(key)
        if value not in [None, ""]:
            return str(value)

    return "Unknown"


def get_deal_value(record: Dict):
    """
    Extract the deal value from the client record.

    Args:
        record (Dict): Client record dictionary.

    Returns:
        Any: Deal value (numeric or string) or "Unknown".

    Why flexible return type:
        Some datasets store values as strings, others as numbers.
    """
    if not record:
        return "Unknown"

    for key in ["close_value", "deal_value", "amount", "opportunity_value"]:
        value = record.get(key)
        if value not in [None, ""]:
            return value

    return "Unknown"


def get_product_name(record: Dict) -> str:
    """
    Extract the product name from the client record.

    Args:
        record (Dict): Client record dictionary.

    Returns:
        str: Product name or "Unknown".
    """
    if not record:
        return "Unknown"

    return str(record.get("product", "Unknown"))


# -------------------------------------------------------------------
# Risk Detection Logic
# -------------------------------------------------------------------

def detect_risk_flags(record: Dict, objection: str) -> List[str]:
    """
    Identify potential risks associated with the deal.

    Args:
        record (Dict): Client deal record.
        objection (str): Detected objection type.

    Returns:
        List[str]: List of risk flags.

    Risk Types:
        - pricing_pressure → Client concerned about cost
        - late_stage_pressure → Negotiation stage risk
        - high_value_deal → Large deal requiring careful handling

    Why this matters:
        Helps the agent adjust tone and strategy based on deal risk.
    """
    risks: List[str] = []

    stage = detect_deal_stage(record).lower()
    deal_value = get_deal_value(record)

    # Pricing objection risk
    if objection == "pricing":
        risks.append("pricing_pressure")

    # Late-stage negotiation risk
    if "negotiation" in stage:
        risks.append("late_stage_pressure")

    # High-value deal risk
    if deal_value != "Unknown":
        try:
            if float(deal_value) > 10000:
                risks.append("high_value_deal")
        except (ValueError, TypeError):
            # Ignore if conversion fails
            pass

    return risks


# -------------------------------------------------------------------
# Next Best Action Logic
# -------------------------------------------------------------------

def suggest_next_best_action(stage: str, objection: str) -> str:
    """
    Recommend the next best action for the sales agent.

    Args:
        stage (str): Current deal stage.
        objection (str): Detected objection type.

    Returns:
        str: Action recommendation.

    Priority:
        1. Objection-based actions (higher priority)
        2. Stage-based actions (fallback)

    Why this matters:
        Guides the conversation forward instead of just responding.
    """
    stage = stage.lower()

    # ------------------------------------------------------------
    # Objection-based actions (highest priority)
    # ------------------------------------------------------------
    if objection == "pricing":
        return "Share ROI summary and offer a pricing walkthrough"

    if objection == "competition":
        return "Send differentiation points and customer proof"

    if objection == "delay":
        return "Propose a smaller pilot or a time-boxed next step"

    if objection == "not_interested":
        return "Reconnect to their business pain and ask a discovery question"

    # ------------------------------------------------------------
    # Stage-based fallback actions
    # ------------------------------------------------------------
    if "prospecting" in stage:
        return "Qualify needs and schedule a discovery discussion"

    if "qualification" in stage:
        return "Clarify pain points and decision criteria"

    if "proposal" in stage:
        return "Send a tailored proposal with business value summary"

    if "negotiation" in stage:
        return "Address objections and align on final commercial terms"

    if "closed" in stage:
        return "Confirm the outcome and document the deal status"

    # Default fallback
    return "Move the deal to the next clear action"


# -------------------------------------------------------------------
# Deal Context Builder (Core Function)
# -------------------------------------------------------------------

def build_deal_context(client_name: str) -> Dict:
    """
    Build a structured deal context for a given client.

    Args:
        client_name (str): Name of the client/account.

    Returns:
        Dict: Structured deal context including:
            - account
            - stage
            - product
            - deal_value
            - sales_agent
            - sector
            - office_location
            - revenue
            - employees

    Flow:
        1. Fetch latest client record from data_loader
        2. Extract key deal attributes
        3. Return structured dictionary

    Why this matters:
        This context is injected into the LLM prompt to make responses:
        - personalized
        - data-driven
        - business-aware
    """
    record = get_latest_client_record(client_name)

    # ------------------------------------------------------------
    # Handle case where no record exists
    # ------------------------------------------------------------
    if not record:
        return {
            "account": client_name,
            "stage": "Unknown",
            "product": "Unknown",
            "deal_value": "Unknown",
            "sales_agent": "Unknown",
            "sector": "Unknown",
            "office_location": "Unknown",
            "revenue": "Unknown",
            "employees": "Unknown",
        }

    # ------------------------------------------------------------
    # Build structured context from record
    # ------------------------------------------------------------
    return {
        "account": record.get("account", client_name),
        "stage": detect_deal_stage(record),
        "product": get_product_name(record),
        "deal_value": get_deal_value(record),
        "sales_agent": record.get("sales_agent", "Unknown"),
        "sector": record.get("sector", "Unknown"),
        "office_location": record.get("office_location", "Unknown"),
        "revenue": record.get("revenue", "Unknown"),
        "employees": record.get("employees", "Unknown"),
    }