import boto3
import os
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key
import json

class DynamoDBService:

    def __init__(self):
        self.table_name = os.environ["DRIFT_TABLE_NAME"]

        self.dynamodb = boto3.resource("dynamodb")

        self.table = self.dynamodb.Table(
            self.table_name
        )

    def save_snapshot(self, account_id: str, environment: str, drift_result: dict) -> dict:

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

        response = self.table.query(
            KeyConditionExpression = Key("AccountId").eq(account_id),
            ScanIndexForward = False,
            Limit = 1
        )

        items = response.get("Items",[])

        if not items:
            return {
                "message": "No snapshots found!"
            }

        return items[0]

    def get_drift_snapshots(self, account_id: str) -> list:

        response = self.table.query(
            KeyConditionExpression = Key("AccountId").eq(account_id)
        )

        return response.get("Items", [])