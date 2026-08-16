from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class Recommendation(BaseModel):
    resource_type: str

    resource_id: str

    severity: str

    category: str

    recommendation: str

    details: Dict

class Warning(BaseModel):
    service: str

    message: str

    resource_id: Optional[str] = None

class ResourceSummary(BaseModel):
    total_recommendations: int

    high: int

    medium: int

    low: int

class ResourceDiscoveryResponse(BaseModel):
    account_id: str

    scan_time: datetime

    summary: ResourceSummary

    warnings: List[Warning]

    recommendations: List[Recommendation]



