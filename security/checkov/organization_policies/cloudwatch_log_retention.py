from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult


class CloudWatchLogRetentionCheck(BaseResourceCheck):

    def __init__(self):
        name = "Ensure CloudWatch Log Groups have retention >= 30 days"
        id = "CKV_ORG_001"
        supported_resources = ["AWS::Logs::LogGroup"]

        super().__init__(
            name=name,
            id=id,
            categories=["LOGGING"],
            supported_resources=supported_resources
        )

    def scan_resource_conf(self, conf):

        properties = conf.get("Properties", {})
    
        retention = properties.get("RetentionInDays")
    
        if retention is None:
            return CheckResult.FAILED
    
        if retention == 30:
            return CheckResult.PASSED
    
        return CheckResult.FAILED


check = CloudWatchLogRetentionCheck()