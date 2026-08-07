import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone
import logging
from app.services.aws_identity_service import AWSIdentityService

awsIdentityService = AWSIdentityService()
logger = logging.getLogger(__name__)

class ResourceDiscoveryService:
    def __init__(self):
        self.sts_client = boto3.client(
            "sts"
        )

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
        warnings = []

        ebs_response = self.find_unused_ebs_volumes()

        recommendations.extend(
            ebs_response["recommendations"]
        )
        warnings.extend(
            ebs_response["warnings"]
        )

        eips_response = self.find_unused_elastic_ips()

        recommendations.extend(
            eips_response["recommendations"]
        )

        warnings.extend(
            eips_response["warnings"]
        )

        s3_response = self.find_empty_s3_buckets()

        recommendations.extend(
            s3_response["recommendations"]
        )

        warnings.extend(
            s3_response["warnings"]
        )

        nat_gateway_response = self.find_nat_gateways()

        recommendations.extend(
            nat_gateway_response["recommendations"]
        )

        warnings.extend(
            nat_gateway_response["warnings"]
        )

        lb_response = self.find_load_balancers()

        recommendations.extend(
            lb_response["recommendations"]
        )

        warnings.extend(
            lb_response["warnings"]
        )

        high = 0
        medium = 0
        low = 0

        for recommendation in recommendations:

            severity = recommendation["severity"]

            if severity == "HIGH":
                high += 1
            elif severity == "MEDIUM":
                medium += 1
            elif severity == "LOW":
                low += 1

        scantime = datetime.now(
            timezone.utc
        ).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        account_id = awsIdentityService.get_account_id()

        return {
            "account_id": account_id,

            "scan_time": scantime,

            "summary": {
                "total_recommendations": len(recommendations),

                "high": high,

                "medium": medium,

                "low": low
            },

            "warnings": warnings,

            "recommendations": recommendations
        }

    def find_unused_ebs_volumes(self):

        try:
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
                        "severity": "HIGH",
                        "category": "Unused Resource",
                        "recommendation":
                            "EBS volume is not attached to any instance",
                        "details": {
                            "size": volume.get("Size"),
                            "state": volume.get("State")
                        }
                    }
                )

            return {
                "recommendations": unused_volumes,
                "warnings": []
            }

        except ClientError:
            logger.exception(
                "Failed to discover unused EBS volumes"
            )

            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "EBS",
                        "message": "Unable to scan EBS volumes."
                    }
                ]
            }

        except Exception:

            logger.exception(
                "Unexpected error while discovering unused EBS volumes"
            )

            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "EBS",
                        "message": "Unexpected error occurred while scanning EBS volumes."
                    }
                ]
            }

    def find_unused_elastic_ips(self):

        try:
            response = self.ec2_client.describe_addresses()
            
            unused_eips = []

            for address in response.get("Addresses", []):
                if "AssociationId" not in address:
                    unused_eips.append(
                        {
                            "resource_type": "ELASTIC_IP",
                            "resource_id": address.get("AllocationId"),
                            "severity": "HIGH",
                            "category": "Unused Resource",
                            "recommendation": "Elastic IP is not associated with any resource",
                            "details": {
                                "public_ip": address.get("PublicIp")
                            }
                        }
                    )
    
            return {
                "recommendations": unused_eips,
                "warnings": []
            }

        except ClientError:
            logging.exception(
                "Failed to discover unused ELASTIC_IPs"
            )

            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "ELASTIC_IP",
                        "message": "Unable to scan elastic IPs"
                    }
                ]
            }

        except Exception:
            logger.exception(
                "Unexpected error while discovering unused EIPs"
            )

            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "EIP",
                        "message": "Unexpected error occurred while scanning EIP."
                    }
                ]
            }

    def find_empty_s3_buckets(self):

        try:
            response = self.s3_client.list_buckets()

        except ClientError as e:
            logger.exception(
                "Failed to list S3 buckets"
            )

            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "S3_BUCKET",
                        "message": "Unable to list S3 buckets"
                    }
                ]
            }

        empty_buckets = []
        warnings = []

        for bucket in response.get("Buckets", []):

            bucket_name = bucket["Name"]

            try:
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
                            "recommendation": "Bucket is empty and can be reviewed",
                            "details": {}
                        }
                    )
            except ClientError as e:
                logger.exception(
                    f"Failed to scan S3 bucket: {bucket_name}"
                )

                warnings.append(
                    {
                        "service": "S3",
                        "resource_id": bucket_name,
                        "message":
                            "Unable to inspect bucket."
                    }
                )
            except Exception:

                logger.exception(
                    f"Unexpected error while scanning bucket: {bucket_name}"
                )

                warnings.append(
                    {
                        "service": "S3",
                        "resource_id": bucket_name,
                        "message":
                            "Unexpected error while inspecting bucket."
                    }
                )

        return {
            "recommendations": empty_buckets,
            "warnings": warnings
        }

    def find_nat_gateways(self):

        try:
            response = self.ec2_client.describe_nat_gateways()
            
            nat_gateways = []

            for nat in response.get("NatGateways", []):
    
                if nat["State"] == "available":
    
                    nat_gateways.append(
                        {
                            "resource_type": "NAT_GATEWAY",
                            "resource_id": nat.get("NatGatewayId"),
                            "severity": "MEDIUM",
                            "category": "Cost Optimization",
                            "recommendation": "Review NAT Gateway usage. NAT Gateways are a common source of AWS cost.",
                            "details": {
                                "state": nat.get("State")
                            }
                        }
                    )
    
            return {
                "recommendations": nat_gateways,
                "warnings": []
            }

        except ClientError as e:

            logging.exception(
                "Failed to discover NAT_GATEWAYs"
            )

            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "NAT_GATEWAY",
                        "message": "Unable to scan nat gateway"
                    }
                ]
            }

        except Exception:
            logger.exception(
                "Unexpected error while discovering NAT gateways"
            )
            
            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "NAT_GATEWAY",
                        "message": "Unexpected error occurred while scanning NAT gateway."
                    }
                ]
            }

    def find_load_balancers(self):
        try:
            response = self.elbv2_client.describe_load_balancers()
            
            load_balancers = []

            for lb in response.get("LoadBalancers", []):
    
                if lb["State"]["Code"] == "active":
    
                    load_balancers.append(
                        {
                            "resource_type": "LOAD_BALANCER",
                            "resource_id": lb.get("LoadBalancerArn"),
                            "severity": "MEDIUM",
                            "category": "Cost Optimization",
                            "recommendation": "Review whether this Load Balancer is still required.",
                            "details": {
                                "name": lb.get("LoadBalancerName"),
                            }
                        }
                    )

            return {
                "recommendations": load_balancers,
                "warnings": []
            }

        except ClientError as e:
            logging.exception(
                "Failed to discover LOAD_BALANCERs"
            )
            
            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "LOAD_BALANCER",
                        "message": "Unable to scan LOAD_BALANCER"
                    }
                ]
            }

        except Exception:
            logger.exception(
                "Unexpected error while discovering LOAD_BALANCER"
            )
                    
            return {
                "recommendations": [],
                "warnings": [
                    {
                        "service": "LOAD_BALANCER",
                        "message": "Unexpected error occurred while scanning LOAD_BALANCER."
                    }
                ]
            }