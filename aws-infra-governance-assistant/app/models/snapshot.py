from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.models.drift import StackDriftResult

class SnapshotResponse(BaseModel):
    account_id: str = Field(alias="AccountId")

    scan_time: datetime = Field(alias="ScanTime")

    environment: str = Field(alias="Environment")

    account_status: str = Field(alias="AccountStatus")

    total_stacks: int = Field(alias="TotalStacks")

    drifted_stacks: int = Field(alias="DriftedStacks")

    results: List[StackDriftResult] = Field(alias="Results")