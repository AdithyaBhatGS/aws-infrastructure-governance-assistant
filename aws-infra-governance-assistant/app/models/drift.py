from pydantic import BaseModel, Field
from typing import List, Optional

class PropertyDifference(BaseModel):
    property_path: str = Field(alias="PropertyPath")

    expected_value: str = Field(alias="ExpectedValue")

    actual_value: str = Field(alias="ActualValue")

    difference_type: str = Field(alias="DifferenceType")

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