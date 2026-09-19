from fastapi import APIRouter
from typing import Union
import json
import os
import boto3

from app.services.cloudformation_service import CloudFormationService
from app.services.dynamodb_service import DynamoDBService
from app.services.resource_discovery_service import ResourceDiscoveryService
from app.services.aws_identity_service import AWSIdentityService
from app.services.history_service import HistoryService

from app.models.recommendation import ResourceDiscoveryResponse
from app.models.drift import DriftResponse, StackDriftResult
from app.models.snapshot import SnapshotResponse, NoSnapshotResponse
from app.models.stack import StackListResponse
from app.models.history import DriftHistoryEntry

# Create mini apps rather than a single giant router file
router = APIRouter()

# boto3 logic
service = CloudFormationService()
dynamodbService = DynamoDBService()
resourceDiscoveryService = ResourceDiscoveryService()
awsIdentityService = AWSIdentityService()
historyService = HistoryService()
sts_client = boto3.client("sts")

@router.get("/")
def home() -> dict:
    """Return the application home payload.

    Returns:
        dict: A dictionary containing the application name and status.
    """
    return {
        "application": "AWS Infrastructure Assistant"
    }

@router.get("/health")
def health() -> dict:
    """Return the health status of the service.

    Returns:
        dict: A dictionary indicating whether the service is healthy.
    """
    return {
        "status": "healthy"
    }

@router.get("/stacks/list", response_model=StackListResponse)
def list_stacks() -> dict:
    """List the active CloudFormation stacks.

    Returns:
        dict: A dictionary containing the active stack count and stack details.
    """
    return service.list_active_stacks()

@router.post("/drift/analyze/stack/{stack_name}", response_model=StackDriftResult)
def analyze_drift(stack_name: str) -> dict:
    """Analyze drift for a specific CloudFormation stack.

    Args:
        stack_name (str): The name of the CloudFormation stack to evaluate.

    Returns:
        dict: Drift analysis results for the specified stack.
    """
    return service.analyze_drift(stack_name)

@router.post("/drift/analyze/account", response_model=Union[DriftResponse, NoSnapshotResponse])
def analyze_account_drift() -> Union[DriftResponse, NoSnapshotResponse]:
    """Analyze drift for the current AWS account and persist the snapshot.

    Returns:
        Union[DriftResponse, NoSnapshotResponse]: The account drift summary, or a
            no-snapshot response if no active stacks are found.
    """
    response = service.analyze_account_drift()

    account_id = awsIdentityService.get_account_id()

    dynamodbService.save_snapshot(
        account_id=account_id,
        environment=os.environ["ENVIRONMENT"],
        drift_result=response
    )

    return response

@router.get("/drift/latest", response_model=Union[SnapshotResponse, NoSnapshotResponse])
def get_latest_drift() -> Union[SnapshotResponse, NoSnapshotResponse]:
    """Fetch the latest drift snapshot for the current AWS account.

    Returns:
        Union[SnapshotResponse, NoSnapshotResponse]: The most recent saved snapshot
            for the account, or a message indicating that no snapshot exists.
    """
    account_id = awsIdentityService.get_account_id()

    response = dynamodbService.get_latest_snapshot(
        account_id=account_id,
    )

    return response


@router.get("/drift/history", response_model=list[DriftHistoryEntry])
def get_historical_trend() -> list[dict]:
    """Return the historical drift trend for the current AWS account.

    Returns:
        list[dict]: A list of historical drift entries for the active environment.
    """
    account_id = awsIdentityService.get_account_id()
    environment = os.environ["ENVIRONMENT"]

    response = dynamodbService.get_drift_snapshots(
        account_id=account_id
    )

    return historyService.get_history(response, environment)


@router.get("/resource_discovery", response_model=ResourceDiscoveryResponse)
def get_resource_discovery() -> dict:
    """Discover AWS resources available in the account and generate recommendations.

    Resource categories:
        EBS, S3, EIPs, NAT gateway, ELB.

    Returns:
        dict: A response containing account metadata, findings, warnings, and
            recommendations.
    """
    response = resourceDiscoveryService.discover_resources()
    return response

