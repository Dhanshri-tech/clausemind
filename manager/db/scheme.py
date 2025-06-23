from pydantic import BaseModel, Field
from pydantic import constr
from typing import Optional
from datetime import datetime
from typing_extensions import Literal

class Contract(BaseModel):
    contract_id: constr(strip_whitespace=True) # type: ignore
    title: str
    domain: Literal["healthcare", "finance", "tech", "procurement","commercial"]
    content: str
    status: Optional[Literal["Draft", "Active", "Reviewed", "Terminated"]] = "Draft"
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    last_modified: Optional[datetime] = None

class AgentLog(BaseModel):
    agent_name: str
    contract_id: str
    action: str
    affected_section: str
    notes: Optional[str] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
