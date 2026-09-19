from pydantic import BaseModel, Field
from typing import List, Optional


class PropertyDifference(BaseModel):
    """Represents one property difference between expected and actual values.

    Attributes:
        property_path: The JSON-style path to the property that differs.
        expected_value: The expected value from the CloudFormation template.
        actual_value: The current value from the deployed resource.
        difference_type: The type of difference detected.
    """

    property_path: str = Field(alias="PropertyPath")
    expected_value: str = Field(alias="ExpectedValue")
    actual_value: str = Field(alias="ActualValue")
    difference_type: str = Field(alias="DifferenceType")


class DriftResource(BaseModel):
    """Represents a resource that differs from its expected configuration.

    Attributes:
        logical_id: The logical resource identifier from the stack template.
        resource_type: The AWS resource type.
        status: The drift status for the resource.
        property_differences: The list of property-level differences found.
    """

    logical_id: str
    resource_type: str
    status: str
    property_differences: List[PropertyDifference]


class StackDriftResult(BaseModel):
    """Contains drift detection results for a single CloudFormation stack.

    Attributes:
        stack_name: The name of the CloudFormation stack.
        status: The overall drift status for the stack.
        detection_id: The unique drift detection identifier, if available.
        resources: The list of resources with drift findings.
        reason: A human-readable explanation when the status is not healthy.
    """

    stack_name: str
    status: str
    detection_id: Optional[str] = None
    resources: List[DriftResource] = Field(default_factory=list)
    reason: Optional[str] = None


class DriftResponse(BaseModel):
    """Summary of drift analysis for the current AWS account.

    Attributes:
        account_status: The overall account drift status.
        total_stacks: The total number of stacks evaluated.
        drifted_stacks: The number of stacks showing drift.
        results: Drift results for each evaluated stack.
    """

    account_status: str
    total_stacks: int
    drifted_stacks: int
    results: List[StackDriftResult]