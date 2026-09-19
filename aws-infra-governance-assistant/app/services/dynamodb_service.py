import boto3
import os
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key
import json


class DynamoDBService:
    """Service for persisting and retrieving drift snapshots in DynamoDB.

    The service reads the configured drift table from SSM and provides
    helper methods to save and query account drift history.
    """

    def __init__(self):
        """Initialize the DynamoDB service.

        Reads the active deployment environment from the ENVIRONMENT
        variable, resolves the drift table name from SSM, and creates the
        DynamoDB table resource.
        """
        self.environment = os.environ["ENVIRONMENT"]

        self.ssm = boto3.client("ssm")

        response = self.ssm.get_parameter(
            Name=f'/portfolio/{self.environment}/drift-table'
        )

        self.table_name = response["Parameter"]["Value"]

        self.dynamodb = boto3.resource("dynamodb")

        self.table = self.dynamodb.Table(
            self.table_name
        )

    def save_snapshot(self, account_id: str, environment: str, drift_result: dict) -> dict:
        """Store a drift snapshot for an AWS account.

        Args:
            account_id (str): AWS account identifier.
            environment (str): Deployment environment for the snapshot.
            drift_result (dict): Drift summary payload to persist.

        Returns:
            dict: A confirmation message indicating the snapshot was stored.
        """
        scan_time = datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        item = {
            "AccountId": account_id,
            "ScanTime": scan_time,
            "Environment": environment,
            "AccountStatus": drift_result["account_status"],
            "TotalStacks": drift_result["total_stacks"],
            "DriftedStacks": drift_result["drifted_stacks"],
            "Results": drift_result["results"]
        }

        self.table.put_item(
            Item=item
        )

        return {
            "message": "Drift snapshot stored successfully"
        }

    def get_latest_snapshot(self, account_id: str) -> dict:
        """Retrieve the most recent saved snapshot for an AWS account.

        Args:
            account_id (str): AWS account identifier.

        Returns:
            dict: The newest snapshot item for the account, or a message
                indicating no snapshots exist.
        """
        response = self.table.query(
            KeyConditionExpression=Key("AccountId").eq(account_id),
            ScanIndexForward=False,
            Limit=1
        )

        items = response.get("Items", [])

        if not items:
            return {
                "message": "No snapshots found!"
            }

        return items[0]

    def get_drift_snapshots(self, account_id: str) -> list[dict]:
        """Fetch all saved drift snapshots for an AWS account.

        Args:
            account_id (str): AWS account identifier.

        Returns:
            list[dict]: A list of snapshot records for the account.
        """
        response = self.table.query(
            KeyConditionExpression=Key("AccountId").eq(account_id)
        )

        return response.get("Items", [])