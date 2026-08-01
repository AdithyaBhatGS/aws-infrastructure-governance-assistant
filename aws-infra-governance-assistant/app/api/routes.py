from fastapi import APIRouter

import os
import boto3

from app.services.cloudformation_service import CloudFormationService
from app.services.dynamodb_services import DynamoDBService
from app.services.resource_discovery_service import ResourceDiscoveryService

# Create mini apps rather than a single giant router file
router = APIRouter()

# boto3 logic
service = CloudFormationService()
dynamodbService = DynamoDBService()
resourceDiscoveryService = ResourceDiscoveryService()

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

@router.get("/stacks")
def list_stacks():
    return service.list_active_stacks()

@router.post("/drift/analyze/{stack_name}")
def analyze_drift(stack_name: str):
    return service.analyze_drift(stack_name)

@router.get("/drift/analyze/account")
def analyze_account_drift():
    response = service.analyze_account_drift()

    account_id = sts_client.get_caller_identity()["Account"]

    dynamodbService.save_snapshot(
        account_id=account_id,
        environment=os.environ["ENVIRONMENT"],
        drift_result=response
    )

    return response

@router.get("/drift/latest")
def get_latest_drift():

    account_id = sts_client.get_caller_identity()["Account"]

    response = dynamodbService.get_latest_snapshot(
        account_id=account_id,
    )

    return response

@router.get("/drift/history")
def get_historical_trend():

    account_id = sts_client.get_caller_identity()["Account"]

    response = dynamodbService.get_history(
        account_id=account_id
    )

    return response

@router.get("/resource_discovery")
def get_resource_discovery():
    response = resourceDiscoveryService.discover_resources()
    return response