from manager.db.contract_db import create_contract, update_contract, get_contract
from manager.db.scheme import Contract
from typing import Optional

def storage_agent(task_type: str, data: dict, contract_id: Optional[str] = None):
    """
    Acts as a general-purpose agent for storing and retrieving contract data.

    Parameters:
    - task_type: "create", "update", or "fetch"
    - data: dictionary with contract fields
    - contract_id: required for fetch/update

    Returns:
    - Success message or contract data
    """
    if task_type == "create":
        validated = Contract(**data)
        inserted_id = create_contract(validated.dict())
        return {"status": "success", "contract_id": inserted_id}

    elif task_type == "update" and contract_id:
        result = update_contract(contract_id, data)
        return {"status": "updated", "matched": result.matched_count}

    elif task_type == "fetch" and contract_id:
        contract = get_contract(contract_id)
        return contract if contract else {"error": "Contract not found"}

    else:
        return {"error": "Invalid storage operation"}
