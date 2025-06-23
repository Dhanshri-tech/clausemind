from .mongodb import get_collection
from datetime import datetime

# Connect to 'agent_logs' collection
logs = get_collection("agent_logs")

def log_agent_action(agent_name: str, contract_id: str, action: str, affected_section: str, notes: str = "") -> str:
    """
    Logs an action taken by an agent.

    Args:
        agent_name (str): Name of the agent (e.g., 'ClauseAgent').
        contract_id (str): ID of the related contract document.
        action (str): What action was performed (e.g., 'CLAUSE_DETECTED').
        affected_section (str): Which part of the contract it relates to.
        notes (str, optional): Any extra context or output. Defaults to "".

    Returns:
        str: The inserted log ID as a string.
    """
    log = {
        "timestamp": datetime.utcnow(),
        "agent_name": agent_name,
        "contract_id": contract_id,
        "action": action,
        "affected_section": affected_section,
        "notes": notes,
    }
    result = logs.insert_one(log)
    return str(result.inserted_id)
