from checkov.cloudformation.checks.resource.base_resource_check import (
    BaseResourceCheck
)
from checkov.common.models.enums import CheckResult


class MandatoryTagsCheck(BaseResourceCheck):

    REQUIRED_TAGS = [
        "Environment",
        "Project",
        "Owner",
        "ManagedBy"
    ]

    TAGGABLE_RESOURCES = [
        "AWS::ElasticLoadBalancingV2::LoadBalancer",
        "AWS::ElasticLoadBalancingV2::TargetGroup",
        "AWS::AutoScaling::AutoScalingGroup",
        "AWS::EC2::VPC",
        "AWS::EC2::Subnet",
        "AWS::EC2::InternetGateway",
        "AWS::EC2::EIP",
        "AWS::EC2::NatGateway",
        "AWS::EC2::RouteTable",
        "AWS::EC2::SecurityGroup",
        "AWS::Logs::LogGroup",
        "AWS::IAM::Role",
        "AWS::S3::Bucket"
    ]


    def __init__(self):

        name = (
            "Ensure AWS resources have mandatory organization tags"
        )

        id = "CKV_ORG_002"

        super().__init__(
            name=name,
            id=id,
            categories=["CONVENTION"],
            supported_resources=self.TAGGABLE_RESOURCES
        )


    def scan_resource_conf(self, conf):

        properties = conf.get(
            "Properties",
            {}
        )

        tags = properties.get(
            "Tags"
        )


        if not tags:
            return CheckResult.FAILED


        existing_tags = []

        for tag in tags:

            key = tag.get("Key")

            if isinstance(key, str):
                existing_tags.append(key)


        for required_tag in self.REQUIRED_TAGS:

            if required_tag not in existing_tags:
                return CheckResult.FAILED


        return CheckResult.PASSED



check = MandatoryTagsCheck()