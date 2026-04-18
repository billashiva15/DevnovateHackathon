from typing import Dict, List

from backend.data_loader import get_latest_client_record


def detect_deal_stage(record: Dict) -> str:
    if not record:
        return "Unknown"

    for key in ["deal_stage", "stage", "sales_stage", "opportunity_stage"]:
        value = record.get(key)
        if value not in [None, ""]:
            return str(value)

    return "Unknown"


def get_deal_value(record: Dict):
    if not record:
        return "Unknown"

    for key in ["close_value", "deal_value", "amount", "opportunity_value"]:
        value = record.get(key)
        if value not in [None, ""]:
            return value

    return "Unknown"


def get_product_name(record: Dict) -> str:
    if not record:
        return "Unknown"

    return str(record.get("product", "Unknown"))


def detect_risk_flags(record: Dict, objection: str) -> List[str]:
    risks: List[str] = []

    stage = detect_deal_stage(record).lower()
    deal_value = get_deal_value(record)

    if objection == "pricing":
        risks.append("pricing_pressure")

    if "negotiation" in stage:
        risks.append("late_stage_pressure")

    if deal_value != "Unknown":
        try:
            if float(deal_value) > 10000:
                risks.append("high_value_deal")
        except (ValueError, TypeError):
            pass

    return risks


def suggest_next_best_action(stage: str, objection: str) -> str:
    stage = stage.lower()

    if objection == "pricing":
        return "Share ROI summary and offer a pricing walkthrough"
    if objection == "competition":
        return "Send differentiation points and customer proof"
    if objection == "delay":
        return "Propose a smaller pilot or a time-boxed next step"
    if objection == "not_interested":
        return "Reconnect to their business pain and ask a discovery question"

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

    return "Move the deal to the next clear action"


def build_deal_context(client_name: str) -> Dict:
    record = get_latest_client_record(client_name)

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