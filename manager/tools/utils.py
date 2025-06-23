# manager/tools/utils.py

import re
from typing import Optional


def clean_contract_text(text: str) -> str:
    """
    Cleans and normalizes raw contract text.
    - Removes extra whitespace, HTML tags, and control characters.
    - Normalizes line breaks and encodings.
    """
    if not text:
        return ""

    # Remove HTML tags if any
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize whitespace and line breaks
    text = re.sub(r"\r\n|\r|\n", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)

    # Strip leading/trailing whitespace
    return text.strip()


# def infer_contract_domain(text: str) -> Optional[str]:
#     """
#     Attempts to infer the domain (tech, finance, healthcare) from contract text.
#     Returns the domain string or None if inconclusive.
#     """
#     lowered = text.lower()

#     tech_keywords = ["saas", "software", "licensing", "ip rights", "source code", "uptime"]
#     finance_keywords = ["aml", "kyc", "bank", "financial", "loan", "interest rate", "investment"]
#     healthcare_keywords = ["hipaa", "patient", "clinical", "pharma", "healthcare", "medical"]

#     if any(k in lowered for k in tech_keywords):
#         return "tech"
#     elif any(k in lowered for k in finance_keywords):
#         return "finance"
#     elif any(k in lowered for k in healthcare_keywords):
#         return "healthcare"
#     else:
#         return None











from typing import Optional

def infer_contract_domain(text: str) -> Optional[str]:
    """
    Attempts to infer the domain (tech, finance, healthcare, procurement, corporate) from contract text.
    Returns the domain string or None if inconclusive.
    """
    lowered = text.lower()

    tech_keywords = ["saas", "software", "licensing", "ip rights", "source code", "uptime"]
    finance_keywords = ["aml", "kyc", "bank", "financial", "loan", "interest rate", "investment"]
    healthcare_keywords = ["hipaa", "patient", "clinical", "pharma", "healthcare", "medical"]
    procurement_keywords = ["vendor", "purchase order", "rfp", "supply chain", "delivery schedule", "procurement"]
    corporate_keywords = ["shareholder", "merger", "acquisition", "board resolution", "governance", "corporate", "equity"]

    if any(k in lowered for k in tech_keywords):
        return "tech"
    elif any(k in lowered for k in finance_keywords):
        return "finance"
    elif any(k in lowered for k in healthcare_keywords):
        return "healthcare"
    elif any(k in lowered for k in procurement_keywords):
        return "procurement"
    elif any(k in lowered for k in corporate_keywords):
        return "corporate"
    else:
        return None













def extract_key_metadata(text: str) -> dict:
    """
    Extracts lightweight metadata such as potential parties, dates, or contract title.
    (Optional function - may be expanded later.)
    """
    metadata = {}

    # Match parties (e.g., between Company A and Company B)
    match = re.search(r"between\s+(.*?)\s+and\s+(.*?)\s", text, re.IGNORECASE)
    if match:
        metadata["party_a"] = match.group(1).strip()
        metadata["party_b"] = match.group(2).strip()

    # Match date
    date_match = re.search(r"dated\s+as\s+of\s+([a-zA-Z0-9, ]+)", text, re.IGNORECASE)
    if date_match:
        metadata["effective_date"] = date_match.group(1).strip()

    return metadata

