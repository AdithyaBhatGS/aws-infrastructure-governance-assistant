from fastapi import APIRouter
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
from app.models.snapshot import SnapshotResponse
from app.models.stack import StackListResponse

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
def home():
    return {
        "application": "AWS Infrastructure Assistant"
    }

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }

@router.get("/stacks/list", response_model=StackListResponse)
def list_stacks():
    return service.list_active_stacks()

@router.post("/drift/analyze/stack/{stack_name}", response_model=StackDriftResult)
def analyze_drift(stack_name: str):
    return service.analyze_drift(stack_name)

@router.post("/drift/analyze/account", response_model=DriftResponse)
def analyze_account_drift():
    response = service.analyze_account_drift()

    account_id = awsIdentityService.get_account_id()

    dynamodbService.save_snapshot(
        account_id=account_id,
        environment=os.environ["ENVIRONMENT"],
        drift_result=response
    )

    return response

@router.get("/drift/latest", response_model=SnapshotResponse)
def get_latest_drift():

    account_id = awsIdentityService.get_account_id()

    response = dynamodbService.get_latest_snapshot(
        account_id=account_id,
    )

    return response

@router.get("/drift/history")
def get_historical_trend():

    account_id = awsIdentityService.get_account_id()
    environment = os.environ["ENVIRONMENT"]

    response = dynamodbService.get_drift_snapshots(
        account_id=account_id
    )

    return historyService.get_history(response, environment)

@router.get("/resource_discovery", response_model=ResourceDiscoveryResponse)
def get_resource_discovery():
    response = resourceDiscoveryService.discover_resources()
    return response

