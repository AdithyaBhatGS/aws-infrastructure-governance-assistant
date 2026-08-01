import boto3

class ResourceDiscoveryService:
    def __init__(self):
        self.ec2_client = boto3.client(
            "ec2"
        )

        self.s3_client = boto3.client(
            "s3"
        )

        self.elbv2_client = boto3.client(
            "elbv2"
        )

    def discover_resources(self):
        recommendations = []

        recommendations.extend(
            self.find_unused_ebs_volumes()
        )
        recommendations.extend(
            self.find_unused_elastic_ips()
        )
        recommendations.extend(
            self.find_empty_s3_buckets()
        )
        recommendations.extend(
            self.find_nat_gateways()
        )
        recommendations.extend(
            self.find_load_balancers()
        )
        return recommendations

    def find_unused_ebs_volumes(self):

        response = self.ec2_client.describe_volumes(
            Filters = [
                {
                    "Name": "status",
                    "Values": [
                        "available"
                    ]
                }
            ]
        )

        unused_volumes = []

        for volume in response.get("Volumes", []):

            unused_volumes.append(
                {
                    "resource_type": "EBS_VOLUME",
                    "resource_id": volume["VolumeId"],
                    "size": volume["Size"],
                    "state": volume["State"],
                    "severity": "HIGH",
                    "category": "Unused Resource",
                    "recommendation":
                        "EBS volume is not attached to any instance"
                }
            )

        return unused_volumes

    def find_unused_elastic_ips(self):

        response = self.ec2_client.describe_addresses()

        unused_eips = []

        for address in response.get("Addresses", []):
            if "AssociationId" not in address:
                unused_eips.append(
                    {
                        "resource_type": "ELASTIC_IP",
                        "resource_id": address.get("AllocationId"),
                        "public_ip": address.get("PublicIp"),
                        "severity": "HIGH",
                        "category": "Unused Resource",
                        "recommendation": "Elastic IP is not associated with any resource"
                    }
                )

        return unused_eips

    def find_empty_s3_buckets(self):

        response = self.s3_client.list_buckets()

        empty_buckets = []

        for bucket in response.get("Buckets", []):

            bucket_name = bucket["Name"]

            objects = self.s3_client.list_objects_v2(
                Bucket = bucket_name,
                MaxKeys = 1
            )

            if objects.get("KeyCount", 0) == 0:
                empty_buckets.append(
                    {
                        "resource_type": "S3_BUCKET",
                        "resource_id": bucket_name,
                        "severity": "LOW",
                        "category": "Unused Resource",
                        "recommendation": "Bucket is empty and can be reviewed"
                    }
                )

        return empty_buckets

    def find_nat_gateways(self):

        response = self.ec2_client.describe_nat_gateways()

        nat_gateways = []

        for nat in response.get("NatGateways", []):

            if nat["State"] == "available":

                nat_gateways.append(
                    {
                        "resource_type": "NAT_GATEWAY",
                        "resource_id": nat["NatGatewayId"],
                        "state": nat["State"],
                        "severity": "MEDIUM",
                        "category": "Cost Optimization",
                        "recommendation": "Review NAT Gateway usage. NAT Gateways are a common source of AWS cost."
                    }
                )

        return nat_gateways

    def find_load_balancers(self):
        response = self.elbv2_client.describe_load_balancers()

        load_balancers = []

        for lb in response.get("LoadBalancers", []):

            if lb["State"]["Code"] == "active":

                load_balancers.append(
                    {
                        "resource_type": "LOAD_BALANCER",
                        "resource_id": lb["LoadBalancerArn"],
                        "name": lb["LoadBalancerName"],
                        "severity": "MEDIUM",
                        "category": "Cost Optimization",
                         "recommendation": "Review whether this Load Balancer is still required."
                    }
                )
        return load_balancers