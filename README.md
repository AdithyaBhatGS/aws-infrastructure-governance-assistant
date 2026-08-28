# AWS Infrastructure Governance Assistant

An AWS-based infrastructure governance and deployment platform designed to automate infrastructure provisioning, detect configuration drift, track infrastructure changes, and provide a centralized interface for managing cloud environments.

The platform combines **AWS CloudFormation, Python, GitHub Actions, FastAPI, Streamlit, and AWS-native services** to provide visibility into infrastructure state and deployment operations.

> **Project status:** Active development

## Problem Statement

Managing cloud infrastructure as the number of resources and deployments increases can become difficult. Manual infrastructure changes can introduce configuration drift, inconsistent infrastructure state, and limited visibility into what changed.

This project addresses these challenges by providing:

- Automated infrastructure provisioning and validation
- Automated application deployment on provisioned infrastructure
- Infrastructure drift detection and change tracking
- Centralized visibility into infrastructure and deployment state
- Environment-specific infrastructure management

## Key Features

- **Infrastructure as Code** — AWS infrastructure provisioned and managed using CloudFormation.
- **Automated Infrastructure Validation** — CloudFormation templates validated using `cfn-lint`, `yamllint`, CloudFormation validation, and Checkov.
- **Automated Application Deployment** — Application artifacts are versioned in Amazon S3 and deployed to provisioned infrastructure through CI/CD.
- **Infrastructure Drift Detection** — Detects and tracks changes between the expected and actual infrastructure state.
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

| Stack               | Responsibility                                                                                            |
| ------------------- | --------------------------------------------------------------------------------------------------------- |
| **Bootstrap**       | GitHub OIDC, permissions boundary, validation roles, deployment roles, and CloudFormation execution roles |
| **Storage**         | Application artifact storage and centralized logging bucket                                               |
| **Security**        | IAM roles, instance profiles, CloudWatch log groups, and related security resources                       |
| **Network**         | VPC, subnets, internet gateway, NAT gateways, route tables, and security groups                           |
| **Launch Template** | EC2 launch configuration, instance bootstrap, CloudWatch Agent, and application deployment configuration  |
| **Application**     | Application Load Balancer, target group, listeners, Auto Scaling Group, and scaling policies              |
| **Platform**        | AWS resources required specifically by the governance platform, including DynamoDB                        |

The **Bootstrap Stack** is provisioned separately, while the remaining stacks are deployed through GitHub Actions in their respective deployment workflows.

## CI/CD Pipeline

The project uses GitHub Actions to automate infrastructure validation, infrastructure deployment, application infrastructure deployment, and application deployment.

### Current Pipeline Structure

1. **Infrastructure Validation**
   - Validates CloudFormation templates using `yamllint`, `cfn-lint`, CloudFormation validation, and Checkov.
   - Runs as part of the pull request workflow.

2. **Infrastructure Deployment**
   - Deploys the foundational `storage`, `security`, and `network` stacks.
   - Uses AWS CloudFormation with environment-specific parameters.

3. **Application Infrastructure Deployment**
   - Deploys the Launch Template and application infrastructure, including the ALB and Auto Scaling Group.
   - Updates the application infrastructure when its corresponding CloudFormation components change.

4. **Application Deployment**
   - Builds and packages the application.
   - Stores versioned application artifacts in Amazon S3.
   - Updates the active application version and triggers an EC2 Auto Scaling instance refresh.

### Deployment Flow

**Pull Request → Validation → Infrastructure → Application Infrastructure → Application**

The current pipelines use environment-specific GitHub Actions concurrency controls to prevent overlapping deployments within the same environment.
