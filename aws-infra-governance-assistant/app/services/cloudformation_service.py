import boto3
import time


class CloudFormationService:

    def __init__(self):
        self.client = boto3.client(
            "cloudformation"
        )

    def list_active_stacks(self) -> dict:

        response = self.client.list_stacks(
            StackStatusFilter=[
                "CREATE_COMPLETE",
                "UPDATE_COMPLETE",
                "UPDATE_ROLLBACK_COMPLETE"
            ]
        )

        stacks = []

        for resource in response.get("StackSummaries", []):
            stacks.append({
                "stack_name": resource["StackName"],
                "status": resource["StackStatus"],
                "creation_time": resource["CreationTime"]
            })

        return {
            "count": len(stacks),
            "stacks": stacks
        }

    def analyze_drift(self, stack_name: str) -> dict:

        # Start a fresh drift detection
        response = self.client.detect_stack_drift(
            StackName=stack_name
        )

        detection_id = response["StackDriftDetectionId"]


        while True:

            status_response = self.client.describe_stack_drift_detection_status(
                StackDriftDetectionId=detection_id
            )

            detection_status = status_response["DetectionStatus"]


            if detection_status == "DETECTION_COMPLETE":
                break

            if detection_status == "DETECTION_FAILED":

                return {
                    "stack_name": stack_name,
                    "status": "FAILED",
                    "reason": status_response.get(
                        "DetectionStatusReason"
                    )
                }


            time.sleep(5)

        # Fetch drift resources after THIS detection completes
        resource_response = self.client.describe_stack_resource_drifts(
            StackName=stack_name
        )
        
        resources = []


        for resource in resource_response.get(
            "StackResourceDrifts",
            []
        ):

            if resource["StackResourceDriftStatus"] != "IN_SYNC":

                resources.append({

                    "logical_id": resource[
                        "LogicalResourceId"
                    ],

                    "resource_type": resource[
                        "ResourceType"
                    ],

                    "status": resource[
                        "StackResourceDriftStatus"
                    ],

                    "property_differences": resource.get(
                        "PropertyDifferences",
                        []
                    )
                })


        return {

            "stack_name": stack_name,

            # Result from the same detection cycle
            "status": status_response.get(
                "StackDriftStatus"
            ),

            "detection_id": detection_id,

            "resources": resources
        }

    def analyze_account_drift(self) -> dict:

        stacks_drifted_data = []


        active_stacks = self.list_active_stacks()


        if active_stacks.get("count") == 0:

            return {
                "message": "No active CloudFormation stacks found"
            }


        for stack in active_stacks.get("stacks", []):

            stack_name = stack.get(
                "stack_name"
            )

            response = self.analyze_drift(
                stack_name
            )

            stacks_drifted_data.append(
                response
            )


        total_stacks = len(
            stacks_drifted_data
        )


        drifted_stacks = len(
            [
                stack for stack in stacks_drifted_data
                if stack.get("status") == "DRIFTED"
            ]
        )


        return {

            "account_status": (
                "DRIFTED"
                if drifted_stacks > 0
                else "IN_SYNC"
            ),

            "total_stacks": total_stacks,

            "drifted_stacks": drifted_stacks,

            "results": stacks_drifted_data
        }