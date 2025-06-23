from .mongodb import get_collection
from datetime import datetime
from bson.objectid import ObjectId

contracts = get_collection("contracts")

def create_contract(data: dict) -> str:
    """
    Inserts a new contract document.
    """
    data["created_at"] = datetime.utcnow()
    print(f"📥 Inserting into MongoDB: {data}")  # ✅ Debug log
    result = contracts.insert_one(data)
    return str(result.inserted_id)

def get_contract(contract_id: str) -> dict:
    """
    Fetch contract using Mongo ObjectId or custom ID.
    """
    try:
        return contracts.find_one({"_id": ObjectId(contract_id)})
    except:
        return contracts.find_one({"contract_id": contract_id})

def update_contract(contract_id: str, updates: dict):
    """
    Update fields of a contract by ObjectId or contract_id.
    """
    updates["last_modified"] = datetime.utcnow()
    try:
        return contracts.update_one({"_id": ObjectId(contract_id)}, {"$set": updates})
    except:
        return contracts.update_one({"contract_id": contract_id}, {"$set": updates})

def get_all_contracts(domain: str = None) -> list:
    """
    Retrieve all contracts or filter by domain.
    """
    query = {"domain": domain} if domain else {}
    return list(contracts.find(query))

def add_analysis_to_contract(contract_id: str, analysis_result: dict):
    """
    Adds clause analysis result to an existing contract document.
    """
    update = {
        "clause_analysis": analysis_result,
        "clause_analysis.updated_at": datetime.utcnow()
    }
    try:
        return contracts.update_one({"_id": ObjectId(contract_id)}, {"$set": update})
    except:
        return contracts.update_one({"contract_id": contract_id}, {"$set": update})
