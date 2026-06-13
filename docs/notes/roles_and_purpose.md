## Roles and their purpose

| Role            | Purpose                                                      |
| --------------- | ------------------------------------------------------------ |
| Deployment Role | Tells cloudformation what to do                              |
| Execution Role  | Permissions used by the cloudformation to perform the things |

| Role               | Principal                     | Permissions                                                                                                                                                                                                                                      | Purpose                                                                                               |
| ------------------ | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| ValidationRole     | GitHub PR Validation Worlflow | <ul><li>cloudformation:ValidateTemplate</li><li>sts:GetCallerIdentity</li></ul>                                                                                                                                                                  | To perform validation of stacks                                                                       |
| InfraDeployRole    | Infra Deployment Pipeline     | <ul><li>cloudformation:CreateStack</li><li>cloudformation:UpdateStack</li><li>cloudformation:DeleteStack</li><li>cloudformation:Describe\*</li><li>iam:PassRole\(only for InfraExecutionRole\)</li></ul>                                         | For performing create, delete and updating the infra related stacks                                   |
| AppDeployRole      | App Deployment Pipeline       | <ul><li>cloudformation:CreateStack</li><li>cloudformation:UpdateStack</li><li>cloudformation:DeleteStack</li><li>cloudformation:Describe\*</li><li>s3:GetObject</li><li>s3:PutObject</li><li>iam:PassRole\(only for AppExecutionRole\)</li></ul> | For performing create, delete and updating the app related stacks, updating the application artifacts |
| InfraExecutionRole | CloudFormation                | <ul><li>VPC</li><li>Subnets</li><li>Route Tables</li><li>Internet Gateway</li><li>NAT</li><li>NAT</li><li>Security Groups</li><li>S3</li><li>IAM</li><li>CloudFront</li></ul>                                                                    | For creating the infrastructure                                                                       |
| AppExecutionRole   | CloudFormation                | <ul><li>EC2</li><li>Launch Template</li><li>Auto Scaling</li><li>ALB</li><li>Target Group</li><li>CloudWatch</li><li>SSM</li></ul>                                                                                                               | For creating the application resources                                                                |

| Permissions Boundary | Attached to | Allow | Deny |
| -------------------- | ----------- | ----- | ---- |

| Name of the boundary | <ul><li>InfraDeployRole</li><li>AppDeployRole</li><li>InfraExecutionRole</li><li>AppExecutionRole</li></ul> | <ul><li>CloudFormation</li><li>EC2</li><li>S3</li><li>ALB</li><li>ASG</li><li>CloudWatch</li><li>IAM \(limited\)</li></ul> | <ul><li>Organizations</li><li>Account-level admin operations</li></ul> |
