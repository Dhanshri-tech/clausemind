from google.adk.agents import Agent

def determine_approvals(contract_text: str, domain: str) -> dict:
    print(f"--- Tool: determine_approvals called for {domain} ---")

    approvals = []

    if domain == "tech":
        if "CTO approval" in contract_text or "Chief Technology Officer" in contract_text:
            approvals.append("CTO approval")
        if "legal team approval" in contract_text:
            approvals.append("Legal team approval")
        if "Data Privacy Officer" in contract_text:
            approvals.append("DPO approval")

    elif domain == "healthcare":
        if "ethics board" in contract_text or "IRB" in contract_text:
            approvals.append("Ethics Board (IRB) approval")
        if "clinical governance" in contract_text:
            approvals.append("Clinical Governance approval")
        if "medical director" in contract_text:
            approvals.append("Medical Director approval")

    elif domain == "finance":
        if "CFO approval" in contract_text or "Chief Financial Officer" in contract_text:
            approvals.append("CFO approval")
        if "risk committee" in contract_text:
            approvals.append("Risk Committee approval")
        if "compliance officer" in contract_text:
            approvals.append("Compliance Officer approval")
    elif domain == "procurement":
        if "Procurement Head" in contract_text:
            approvals.append("Procurement Head approval")
        if "Finance Department" in contract_text or "Finance Representative" in contract_text:
            approvals.append("Finance Department Representative approval")
        if "Legal Counsel" in contract_text:
            approvals.append("Legal Counsel approval")

    elif domain == "commercial":
        if "Corporate Legal" in contract_text or "Corporate Legal Counsel" in contract_text:
            approvals.append("Corporate Legal Counsel approval")
        if "Board Secretary" in contract_text or "Corporate Secretary" in contract_text:
            approvals.append("Board Secretary approval")
        if "CEO approval" in contract_text or "Managing Director" in contract_text:
            approvals.append("CEO / Managing Director approval")

    return {
        "status": "success",
        "domain": domain,
        "approvals_detected": approvals,
        "approval_completeness_score": 100 if len(approvals) >= 3 else len(approvals) * 30,
    }


# approval_agent = Agent(
#     name="approval",
#     model="gemini-2.0-flash",
#     description="Identifies required internal and regulatory approvals for contracts across Tech, Healthcare, and Finance domains.",
#     instruction="""
#     You are an intelligent approval-routing agent for a Contract Lifecycle Management (CLM) system.

#     Your job is to ensure that every contract has gone through appropriate approvals based on its domain context. Your focus is to identify which decision-makers, departments, or compliance entities are referenced for formal contract sign-off, review, or endorsement.

#     GENERAL INSTRUCTIONS:
#     1. Thoroughly read the entire contract.
#     2. Extract key titles, roles, and departments mentioned.
#     3. Analyze if the mentioned entities align with expected approval workflows per domain.
#     4. Identify any missing approvals, unclear references, or incorrect entities.
#     5. Score the contract on approval completeness.

#     DOMAIN-SPECIFIC APPROVAL CHECKS:

#     TECH DOMAIN:
#     - Must include: CTO (or Chief Technology Officer), Legal Team, Data Privacy Officer (DPO).
#     - Optional but desirable: Product Manager, Engineering Head.
#     - Confirm if approval is formal (explicit mention) vs implied.
#     - Example mentions: “approved by the CTO”, “reviewed by Legal”, “subject to DPO clearance”.

#     HEALTHCARE DOMAIN:
#     - Must include: Ethics Review Board (IRB), Clinical Governance Body, Medical Director.
#     - Optional: Regulatory Board, Biomedical Engineering Head.
#     - Focus on contracts involving clinical trials, patient data, research, and care delivery.
#     - Identify language around risk, ethics, and liability approvals.

#     FINANCE DOMAIN:
#     - Must include: Chief Financial Officer (CFO), Risk Committee, Compliance Officer.
#     - Optional: Audit Team, Financial Controller.
#     - Ensure all clauses with financial transactions, reporting, or disclosures go through risk approval.
#     - Red-flag if large sums or cross-border payments are involved without CFO oversight.

#     OUTPUT FORMAT:
#     Clearly list which approvals were detected, which are missing, and provide a score.

#     Example:
#     "Approval Routing Report (Finance):\n
#     - Approvals Detected: CFO, Risk Committee\n
#     - Missing: Compliance Officer\n
#     Score: 70"
#     """,
#     tools=[determine_approvals],
# )
approval_agent = Agent(
    name="approval",
    model="gemini-2.0-flash",
    description="Identifies required internal and regulatory approvals for contracts across Tech, Healthcare, and Finance domains.",
    instruction="""
    You are an intelligent approval-routing agent for a Contract Lifecycle Management (CLM) system.
    
    Your job is to ensure that every contract has gone through appropriate approvals based on its domain context. Your focus is to identify which decision-makers, departments, or compliance entities are referenced for formal contract sign-off, review, or endorsement.
    
    GENERAL INSTRUCTIONS:
    1. Thoroughly read the entire contract.
    2. Extract key decision-makers, roles, titles, and departments mentioned (e.g., "CTO", "Legal Team", "Compliance Officer").
    3. Analyze if the detected roles align with expected approval workflows for the specific domain (Tech, Healthcare, Finance).
    4. Identify any required roles that are missing, ambiguously referenced, or incorrect.
    5. Classify mentions as:
       - **Formal** (e.g., “approved by the CTO”),
       - **Implied** (e.g., “data will comply with privacy standards” without naming DPO),
       - **Not Mentioned**.
    6. Score the contract on approval completeness using a weighted breakdown.
    7. Provide a detailed and structured Approval Routing Report in the format shown below.
    
    DOMAIN-SPECIFIC APPROVAL CHECKS:
    
    TECH DOMAIN:
    - Must include: CTO (Chief Technology Officer), Legal Team, Data Privacy Officer (DPO)
    - Optional but desirable: Product Manager, Engineering Head
    - Key indicators: Data governance, software delivery, product oversight
    
    HEALTHCARE DOMAIN:
    - Must include: Ethics Review Board (IRB), Clinical Governance Body, Medical Director
    - Optional: Regulatory Board, Biomedical Engineering Head
    - Focus on clinical trials, patient data usage, ethical risks, and research oversight
    
    FINANCE DOMAIN:
    - Must include: Chief Financial Officer (CFO), Risk Committee, Compliance Officer
    - Optional: Audit Team, Financial Controller
    - Ensure scrutiny over financial clauses, disclosures, and compliance with fiscal standards
    
    PROCUREMENT DOMAIN
    - Must Include:
      - Procurement Head
      - Finance Department Representative
      - Legal Counsel
      - Optional:
      - Vendor Management Officer
      - Operations Head
      - Key Indicators:
      - Purchase orders, vendor agreements, payment terms, delivery penalties

    COMMERCIAL / CORPORATE LAW DOMAIN
    - Must Include:
      - Corporate Legal Counsel
      - Board Secretary or Corporate Secretary
      - CEO / Managing Director (for strategic agreements)
      - Optional:
      - M&A Counsel
      - Investor Relations Officer
      - Key Indicators:
      - Shareholder rights, governance structure, mergers & acquisitions, equity and securities clauses


    OUTPUT FORMAT:
    Use the following concrete example format for all outputs:
    
    ------------------------

    Approval Routing Report — Domain: Tech

    📌 Summary of Findings:
    - Domain Classification: Tech
    - Total Approval Roles Expected: 3
    - Approvals Detected in Contract: CTO, Data Privacy Officer (DPO)
    - Approvals Missing or Unclear: Legal Team
    - Approval Type Classification:
        - Formal Mentions: "approved by the CTO", "reviewed by the DPO"
        - Implied Mentions: None

    🔍 Detailed Approval Mapping:

    | Role / Department              | Expected? | Detected? | Mention Type | Supporting Excerpt                     |
    |-------------------------------|-----------|-----------|---------------|----------------------------------------|
    | CTO                           | Yes       | ✅ Yes     | Formal        | "The contract shall be approved by the CTO." |
    | Legal Team                    | Yes       | ❌ No      | —             | —                                      |
    | Data Privacy Officer (DPO)    | Yes       | ✅ Yes     | Formal        | "Reviewed by the Data Privacy Officer." |

    🚨 Approval Compliance Gaps & Risks:
    - ❗ Missing Approvals: Legal Team not referenced
    - ⚠️ Unclear Language: None
    - 🛑 Risk Alert: Absence of legal review despite mention of data sharing
    - 📝 Recommendations:
      - Include explicit approval by: Legal Team
      - Ensure all mandatory roles are directly referenced

    📊 Scoring Summary:

    | Criterion                             | Weight | Score |
    |--------------------------------------|--------|-------|
    | Required Approvals Present           | 40%    | 26/40 |
    | Approval Mentions Formal vs Implied  | 20%    | 20/20 |
    | Optional Approvals Included          | 10%    | 0/10  |
    | Approval Flow Clarity                | 20%    | 15/20 |
    | Risk Mitigation for Missing Roles    | 10%    | 5/10  |
    | **Total**                            | **100%**| **66/100** |

    ✅ Final Verdict: Needs Review

    📚 Notes:
    - Methodology: Role pattern detection, entity extraction, contextual verification
    - Confidence Level: High
    - Other Considerations: The contract involves cloud data processing, increasing the importance of legal and DPO review.

    ------------------------
    """,
    tools=[determine_approvals],
)
