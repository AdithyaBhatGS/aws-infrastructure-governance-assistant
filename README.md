# AWS Infrastructure Governance Assistant

An AWS-based infrastructure governance and deployment platform designed to automate infrastructure provisioning, detect configuration drift, track infrastructure changes, and provide a centralized interface for managing cloud environments, identify idle resources(EIPs, EBS volumes, S3 buckets), issue a simple warning regarding existing resources(NAT gateways, ELBs) for cost optimization.

The platform combines **AWS CloudFormation, Python, GitHub Actions, FastAPI, Streamlit, and AWS-native services** to provide visibility into infrastructure state, drift history, resource discovery across 5 categories(EIPs, EBS volumes, S3 buckets, NAT gateways, ELBs) for cost optimization.

> **Project status:** Active development

## Problem Statement

Managing cloud infrastructure as the number of resources and deployments increases can become difficult. Manual infrastructure changes can introduce configuration drift, inconsistent infrastructure state, and limited visibility into what changed.

On top of that organizations might have 1000s of resources which are being managed manually or using IAC. There is a possibility of resources being idle. Users might not realize this and might be accidentally kept them running or idle.

The project is constructed to solve these problems through:

1. Providing the centralized dashboard depecting account level drift status, stack creation status and stack drift status.
2. <img src="./docs/images/dashboard.png" width="40%" alt="Dashboard view">

- Fresh drift scans at the account level to provide live information about your infrastructure, providing granular details including what exactly have changed in which stack in which particular resource.
- Providing a simple drift history panel which gives information about how many drifts are being added, removed and changed at the account level per scan, what are they.
- Providing resource discovery recommendations across 2 categories for cost optimization:
  1. Unused/Idle - EIPs, EBS volumes, s3 buckets.
  2. Cost optimization - ELB, NAT gateways.

## Key Features

- **Infrastructure as Code** — AWS infrastructure provisioned and managed using CloudFormation.
- **Automated Infrastructure Validation** — CloudFormation templates validated using `cfn-lint`, `yamllint`, CloudFormation validation, and Checkov.
- **Automated Application Deployment** — Application artifacts are versioned in Amazon S3 and deployed to provisioned infrastructure through CI/CD.
- **Infrastructure Drift Detection** — Detects and tracks changes between the expected and actual infrastructure state.
- **Resource discovery** - Detects idle resources based on their status, association IDs, number of objects. Provides general warning on existing NAT gateways, ELBs as they can increase the bills significantly.
- **Drift History & Change Tracking** — Maintains visibility into infrastructure changes over time.
- **AWS-Native Governance** — Uses IAM, CloudFormation, SSM, CloudWatch, and other AWS services to support infrastructure management and observability.
- **CI/CD Automation** — GitHub Actions manages validation and deployment workflows.
- **Secure CI/CD Bootstrap** — Separates GitHub OIDC, permissions boundaries, validation roles, deployment roles, and CloudFormation execution roles from the automated deployment workflows.
- **Platform Interface** — FastAPI provides the backend services while Streamlit provides the user interface.

## Architecture

The platform is divided into two primary components:

### Infrastructure

AWS infrastructure is provisioned using modular CloudFormation stacks, including:

- Storage and logging
- IAM and security resources
- VPC, subnets, route tables, NAT gateways, and security groups
- EC2 Launch Template
- Application Load Balancer and Auto Scaling Group
- Platform-specific AWS resources

The platform also uses a manually provisioned **Bootstrap Stack** containing the foundational security and CI/CD resources required to deploy the remaining infrastructure. These include the GitHub Actions OIDC provider, permissions boundary, validation, deployment, and CloudFormation execution roles.

The Bootstrap Stack is intentionally deployed outside the automated deployment pipeline to avoid a circular dependency: the pipeline requires permissions to manage these IAM resources, while those permissions themselves are established by the Bootstrap Stack.

### Application

The application is hosted on EC2 instances and consists of:

- **FastAPI** — backend API service
- **Streamlit** — web-based platform interface
- **DynamoDB** — application data storage

The application infrastructure is deployed into private subnets behind an internet-facing Application Load Balancer.

### Current Deployment Model

The current deployment model uses:

**GitHub → GitHub Actions → AWS CloudFormation → AWS infrastructure → EC2 → Application**

Application releases are packaged as versioned artifacts and stored in Amazon S3. EC2 instances retrieve the current application version during deployment rather than receiving in-place code updates.

## Infrastructure Stack Structure

The infrastructure is organized into modular CloudFormation stacks, with each stack responsible for a specific layer of the platform.

| Stack                                                                    | Responsibility                                                                                            |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [**Bootstrap**](/infra/bootstrap/bootstrap-stack.yaml)                   | GitHub OIDC, permissions boundary, validation roles, deployment roles, and CloudFormation execution roles |
| [**Storage**](/infra/storage/storage-stack.yaml)                         | Application artifact storage and centralized logging bucket                                               |
| [**Security**](/infra/security/security-stack.yaml)                      | IAM roles, instance profiles, CloudWatch log groups, and related security resources                       |
| [**Network**](/infra/network/network-stack.yaml)                         | VPC, subnets, internet gateway, NAT gateways, route tables, and security groups                           |
| [**Launch Template**](/infra/launch-template/launch-template-stack.yaml) | EC2 launch configuration, instance bootstrap, CloudWatch Agent, and application deployment configuration  |
| [**Application**](/infra/application/application-stack.yaml)             | Application Load Balancer, target group, listeners, Auto Scaling Group, and scaling policies              |
| [**Platform**](/infra/platform/platform-stack.yaml)                      | AWS resources required specifically by the governance platform, including DynamoDB                        |

The **Bootstrap Stack** is provisioned separately, while the remaining stacks are deployed through GitHub Actions in their respective deployment workflows.

## CI/CD Pipeline

The project uses GitHub Actions to automate infrastructure validation, infrastructure deployment, application infrastructure deployment, and application deployment.

| Workflow                                                                              | Responsibility                                | Current mechanism                                          |
| ------------------------------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| [**Infrastructure Validation**](/.github/workflows/validate-infra-on-pr.yaml)         | Validate CloudFormation/IaC                   | `cfn-lint`, `yamllint`, CloudFormation validation, Checkov |
| [**Infrastructure Deployment**](/.github/workflows/deploy-infra.yaml)                 | Deploy foundational infrastructure            | CloudFormation                                             |
| [**Application Infrastructure Deployment**](/.github/workflows/deploy-app-infra.yaml) | Deploy compute and application infrastructure | Launch Template, ALB, ASG                                  |
| [**Application Deployment**](/.github/workflows/deploy-app.yaml)                      | Deploy application releases                   | S3 artifacts + EC2 Instance Refresh                        |

### Deployment Flow

**Pull Request → Validation → Infrastructure → Application Infrastructure → Application**

The current pipelines use environment-specific GitHub Actions concurrency controls to prevent overlapping deployments within the same environment.

## Technology Stack

| Category                       | Technologies                                                 |
| ------------------------------ | ------------------------------------------------------------ |
| **Cloud**                      | AWS                                                          |
| **Infrastructure as Code**     | AWS CloudFormation                                           |
| **CI/CD**                      | GitHub Actions                                               |
| **Application**                | Python, FastAPI, Streamlit                                   |
| **Compute**                    | Amazon EC2, Auto Scaling                                     |
| **Networking**                 | VPC, Application Load Balancer, Security Groups, NAT Gateway |
| **Storage & Data**             | Amazon S3, DynamoDB                                          |
| **Identity & Access**          | IAM, GitHub OIDC, Permissions Boundaries                     |
| **Configuration & Operations** | AWS Systems Manager, CloudWatch                              |
| **Security & Validation**      | Checkov, cfn-lint, yamllint                                  |
| **Version Control**            | Git, GitHub                                                  |

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       ├── validate-infra-on-pr.yaml
│       ├── deploy-infra.yaml
│       ├── deploy-app-infra.yaml
│       └── deploy-app.yaml
├── aws-infra-governance-assistant/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── ui/
│   │   └── main.py
│   └── requirements.txt
├── infra/
│   ├── application/
│   ├── bootstrap/
│   ├── launch-template/
│   ├── network/
│   ├── platform/
│   ├── security/
│   └── storage/
├── security/
│   └── checkov/
│       └── organization_policies/
├── .gitattributes
├── .gitignore
├── .yamllint.yaml
├── README.md
└── requirements.txt
```

- **`infra/`** — CloudFormation templates and environment-specific parameters for AWS infrastructure.
- **`aws-infra-governance-assistant/`** — Application source for the governance platform.
- **`.github/workflows/`** — CI/CD workflows for validation and deployment.
- **`requirements.txt`** — Python dependencies used by the platform.
- **`security/checkov/organization_policies`** - Custom `checkov` policies for scanning the infrastructure.
