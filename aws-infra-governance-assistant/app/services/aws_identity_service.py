import boto3

class AWSIdentityService:
    """Provides helper methods for AWS identity and account metadata."""

    def __init__(self):
        """Initialize the AWS STS client.

        The STS client is used to query account-level identity information
        such as the current caller account ID.
        """
        self.sts_client = boto3.client(
            "sts"
        )

    def get_account_id(self) -> str:
        """Retrieve the current AWS account ID.

        Returns:
            str: The AWS account ID for the active caller identity.
        """
        response = self.sts_client.get_caller_identity()

        return response["Account"]