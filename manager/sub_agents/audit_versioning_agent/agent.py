# manager/sub_agents/audit_versioning_agent/agent.py

import os
from google.adk.agents import Agent
from manager.tools.prompt_loader import load_prompt

# Define your audit_versioning agent
audit_versioning_agent = Agent(
    name="audit_versioning",
    model="gemini-2.0-flash",
    description="Tracks contract edits, analyzes conversation history, and generates a versioned audit trail.",
    instruction="""
You are an Audit & Versioning Agent in a Contract Lifecycle Management (CLM) system.

Your responsibilities include:
- Analyzing the contract's chat history or version drafts to extract key decisions and change events.
- Tracking contract evolution: additions, deletions, or modifications to clauses.
- Identifying who made changes and highlighting significant legal or operational impacts.
- Flagging risky edits, tampering, or deviations from standard templates.
- Detecting missing key clauses or unauthorized modifications.
- Providing a structured version summary or changelog with timestamps if available.

Output Guidelines:
- Be concise and professional.
- Use markdown bullet points or a numbered format for version history.
- Group similar changes together if the history is long.
- Emphasize the legal/contractual impact where applicable.

Always maintain a clear, chronological audit trail that is easy to read and use.
"""
)

# ✅ Safely load prompts using absolute path
current_dir = os.path.dirname(__file__)
prompt_path = os.path.join(current_dir, "prompts.yaml")

try:
    prompts_dict = load_prompt(prompt_path)
    audit_prompts = prompts_dict["audit_versioning"]
except Exception as e:
    print(f"⚠️ ERROR loading prompts: {e}")
    audit_prompts = []

# 🔎 Helper function to get a specific prompt by name
def get_audit_prompt(prompt_name: str) -> str:
    for prompt in audit_prompts:
        if prompt["name"] == prompt_name:
            return prompt["prompt"]
    raise ValueError(f"Prompt with name '{prompt_name}' not found.")

# 🧪 Function to compare two contract versions
def compare_contract_versions(contract_version_1: str, contract_version_2: str) -> dict:
    selected_prompt = get_audit_prompt("detect_changes")
    formatted_prompt = selected_prompt.replace("Version A", contract_version_1).replace("Version B", contract_version_2)

    response = audit_versioning_agent.generate(
        system="You are a contract audit agent.",
        prompt=formatted_prompt
    )
    return response
