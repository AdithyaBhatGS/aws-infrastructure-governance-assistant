from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.models.drift import StackDriftResult

class HistorySummaryResponse(BaseModel):
    ScanTime: datetime

    AccountStatus: str

    TotalStacks: int

    DriftedStacks: int

class SnapshotResponse(BaseModel):
    AccountId: str

    ScanTime: datetime

    Environment: str

    AccountStatus: str

    TotalStacks: int

    DriftedStacks: int

    Results: List[StackDriftResult]