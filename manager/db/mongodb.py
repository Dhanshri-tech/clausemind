import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Match variable names with .env keys
MONGO_URI = os.getenv("MONGO_URI")  # ✅ correct
DB_NAME = os.getenv("MONGO_DB_NAME")  # ✅ correct

# Optional: collection name if you need it
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "contracts")  # ✅ fallback to "contracts"


if not MONGO_URI:
    raise ValueError("MONGODB_URI not found in environment variables!")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
except Exception as e:
    raise ConnectionError(f"Could not connect to MongoDB: {e}")

def get_collection(name: str):
    """
    Returns a MongoDB collection by name.

    Args:
        name (str): Collection name.

    Returns:
        pymongo.collection.Collection
    """
    return db[name]
