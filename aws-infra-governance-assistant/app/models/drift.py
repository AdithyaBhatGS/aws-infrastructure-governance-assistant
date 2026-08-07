from pydantic import BaseModel, Field
from typing import List, Optional

class PropertyDifference(BaseModel):
    PropertyPath: str

    ExpectedValue: str

    ActualValue: str

    DifferenceType: str

class DriftResource(BaseModel):
    logical_id: str

    resource_type: str

    status: str

    property_differences: List[PropertyDifference]

class StackDriftResult(BaseModel):
    stack_name: str

    status: str

    detection_id: Optional[str] = None

    resources: List[DriftResource] = Field(default_factory=list)

    reason: Optional[str] = None

class DriftResponse(BaseModel):
    account_status: str

    total_stacks: int

    drifted_stacks: int

    results: List[StackDriftResult]