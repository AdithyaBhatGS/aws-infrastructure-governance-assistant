import boto3

class AWSIdentityService:

    def __init__(self):

        self.sts_client = boto3.client(
            "sts"
        )

    def get_account_id(self):

        response = self.sts_client.get_caller_identity()

        return response["Account"]