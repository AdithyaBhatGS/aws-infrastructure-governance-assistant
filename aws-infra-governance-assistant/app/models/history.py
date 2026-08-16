from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.drift import PropertyDifference
from datetime import datetime

class PropertyChanges(BaseModel):

    added: List[PropertyDifference] = Field(default_factory=list)

    removed: List[PropertyDifference] = Field(default_factory=list)

class ChangedResource(BaseModel):

    stack_name: str

    logical_id: str

    resource_type: str

    property_changes: PropertyChanges

class HistoricalResponse(BaseModel):

    stack_name: str

    logical_id: str

    resource_type: str

    property_differences: List[PropertyDifference]

class DriftChanges(BaseModel):

    added: List[HistoricalResponse] = Field(default_factory=list)

    removed: List[HistoricalResponse] = Field(default_factory=list)

    changed: List[ChangedResource] = Field(default_factory=list)

class DriftHistoryEntry(BaseModel):

    scan_time: datetime

    added: List[HistoricalResponse] = Field(default_factory=list)

    removed: List[HistoricalResponse] = Field(default_factory=list)

    changed: List[ChangedResource] = Field(default_factory=list)
