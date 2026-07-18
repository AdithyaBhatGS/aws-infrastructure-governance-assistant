from checkov.cloudformation.checks.resource.base_resource_check import (
    BaseResourceCheck
)
from checkov.common.models.enums import CheckResult


class LaunchTemplateGP3Check(BaseResourceCheck):

    def __init__(self):
        name = "Ensure Launch Template root volume uses GP3"

        id = "CKV_ORG_003"

        supported_resources = [
            "AWS::EC2::LaunchTemplate"
        ]

        super().__init__(
            name=name,
            id=id,
            categories=["GENERAL"],
            supported_resources=supported_resources
        )

    def scan_resource_conf(self, conf):

        properties = conf.get("Properties", {})

        launch_template_data = properties.get(
            "LaunchTemplateData",
            {}
        )

        block_devices = launch_template_data.get(
            "BlockDeviceMappings",
            []
        )

        if not block_devices:
            return CheckResult.FAILED

        for mapping in block_devices:

            ebs = mapping.get("Ebs")

            if not ebs:
                continue

            volume_type = ebs.get("VolumeType")

            if volume_type == "gp3":
                return CheckResult.PASSED

        return CheckResult.FAILED


check = LaunchTemplateGP3Check()