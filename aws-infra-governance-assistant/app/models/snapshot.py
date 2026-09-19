from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.models.drift import StackDriftResult


class SnapshotResponse(BaseModel):
    """Contains a saved drift snapshot for an AWS account.

    Attributes:
        account_id: The AWS account identifier.
        scan_time: The time the drift snapshot was captured.
        environment: The deployment environment associated with the snapshot.
        account_status: The overall drift status of the account.
        total_stacks: The total number of stacks included in the snapshot.
        drifted_stacks: The number of stacks with drift in the snapshot.
        results: The list of drift results for the stacks.
    """

    account_id: str = Field(alias="AccountId")
    scan_time: datetime = Field(alias="ScanTime")
    environment: str = Field(alias="Environment")
    account_status: str = Field(alias="AccountStatus")
    total_stacks: int = Field(alias="TotalStacks")
    drifted_stacks: int = Field(alias="DriftedStacks")
    results: List[StackDriftResult] = Field(alias="Results")


class NoSnapshotResponse(BaseModel):
    """Returned when no drift snapshot exists for the account.

    Attributes:
        message: A message indicating there is no snapshot available.
    """

    message: str