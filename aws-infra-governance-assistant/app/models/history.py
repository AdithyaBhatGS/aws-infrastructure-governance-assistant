from pydantic import BaseModel, Field
from typing import List
from app.models.drift import PropertyDifference
from datetime import datetime


class PropertyChanges(BaseModel):
    """Represents property additions and removals for a resource.

    Attributes:
        added: Properties that were added compared to the previous scan.
        removed: Properties that were removed compared to the previous scan.
    """

    added: List[PropertyDifference] = Field(default_factory=list)
    removed: List[PropertyDifference] = Field(default_factory=list)


class ChangedResource(BaseModel):
    """Represents a resource whose properties changed over time.

    Attributes:
        stack_name: The CloudFormation stack that owns the resource.
        logical_id: The logical resource identifier.
        resource_type: The AWS resource type.
        property_changes: The list of additions and removals for the resource.
    """

    stack_name: str
    logical_id: str
    resource_type: str
    property_changes: PropertyChanges


class HistoricalResponse(BaseModel):
    """Represents a historical property comparison result.

    Attributes:
        stack_name: The CloudFormation stack name.
        logical_id: The logical resource identifier.
        resource_type: The AWS resource type.
        property_differences: Historical property differences for the resource.
    """

    stack_name: str
    logical_id: str
    resource_type: str
    property_differences: List[PropertyDifference]


class DriftHistoryEntry(BaseModel):
    """Represents a single drift scan and its historical changes.

    Attributes:
        scan_time: The timestamp when the drift scan was recorded.
        added: Historical entries for resources that were newly detected.
        removed: Historical entries for resources that disappeared.
        changed: Historical entries for resources whose properties changed.
    """

    scan_time: datetime
    added: List[HistoricalResponse] = Field(default_factory=list)
    removed: List[HistoricalResponse] = Field(default_factory=list)
    changed: List[ChangedResource] = Field(default_factory=list)
    total_drifts: int
