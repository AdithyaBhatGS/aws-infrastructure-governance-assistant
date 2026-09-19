from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class Recommendation(BaseModel):
    """Represents a recommended action for a specific AWS resource.

    Attributes:
        resource_type: The AWS service or resource type.
        resource_id: The unique identifier of the resource.
        severity: The severity of the recommendation.
        category: The category of the recommendation.
        recommendation: The recommended remediation or action.
        details: Additional details for the recommendation.
    """

    resource_type: str
    resource_id: str
    severity: str
    category: str
    recommendation: str
    details: Dict


class Warning(BaseModel):
    """Represents a warning raised during resource discovery.

    Attributes:
        service: The AWS service associated with the warning.
        message: A description of the warning.
        resource_id: The affected resource identifier, if available.
    """

    service: str
    message: str
    resource_id: Optional[str] = None


class ResourceSummary(BaseModel):
    """Summary of recommendation counts by severity.

    Attributes:
        total_recommendations: The total number of recommendations.
        high: The number of high-severity recommendations.
        medium: The number of medium-severity recommendations.
        low: The number of low-severity recommendations.
    """

    total_recommendations: int
    high: int
    medium: int
    low: int


class ResourceDiscoveryResponse(BaseModel):
    """Response containing discovered AWS resources and recommendations.

    Attributes:
        account_id: The AWS account identifier.
        scan_time: The timestamp of the discovery scan.
        summary: A summary of recommendation counts.
        warnings: Any warnings generated during discovery.
        recommendations: Recommendations generated from the discovery results.
    """

    account_id: str
    scan_time: datetime
    summary: ResourceSummary
    warnings: List[Warning]
    recommendations: List[Recommendation]



