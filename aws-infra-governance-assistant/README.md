### Platform Governance Assistant(AWS Infra):

The platform currently supports environment-level governance for isolated Dev and Prod AWS accounts. Each environment has its own infrastructure, IAM permissions, pipelines, and platform services. Multi-account organizational aggregation is considered a future enhancement.

#### Features:

1. Infra health snapshot
   1. **Purpose:** Provide a consolidated infrastructure health view instead of manually checking every CloudFormation stack.
   2. ```
       Account: dev

       Stacks Checked: 15

       Healthy: 13
       Drifted: 2

       Drifted Resources:

       Network-stack
       - PublicSubnet
       - RouteTable

       Security-stack
       - SecurityGroup

      ```

2. Individual Stack Investigation
   1. **Purpose:** Allow deeper investigation after consolidated detection.
   2. ```
        security-stack

        Status:
        DRIFTED

        Resources:
        WebSG
        Changed:
        Ingress rule modified
      ```

3. Historical trend
   1. **Purpose:** Understand whether infrastructure health is improving or degrading.
   2. ```
        Last 30 days

        July 1:
        5 drifted resources

        July 15:
        2 drifted resources

        July 27:
        0 drifted resources
      ```

4. Developer Resource Lifecycle Manager
   1. **Purpose:** Cost optimization for non-production environments.
   2. Example:
      ```
        Environment = dev
        Interruptable = true
      ```
   3. Policy:

      ```
        6 PM:
        Stop resources

        9 AM:
        Start resources
      ```

5. Unused resource discovery and controlled cleanup
   1. **Purpose:** Help developers identify unnecessary AWS resources.
   2. ```
        Unused Resources:
        EC2 Instance i-12345

        Managed By:
        None

        Status:
        Stopped for 30 days

        Action:
        Cleanup allowed
      ```

---

#### Targeted audience:

1. Developer
   1. ```
       Payment Service

       Stacks:
           - payment-network
           - payment-security
           - payment-app
      ```

   2. Here developer cannot manually check each stack across multiple accounts.

   3. Through this platform he/she would get consolidated results of the drift data on an Account level.

2. DevOps/Platform Engineers/Architects/Engineering Managers
   1. They manage

      ```
      - 100+ AWS accounts
      - 1000+ stacks
      - multiple regions
      ```

   2. Going to each stack and detecting is infeasible

3. Cloud Governance team
   1. Let's say there is a strict mandate saying:

      > "Production infrastructure must only change through IaC."

      Now platform detects:

      ```
      Production VPC modified manually
      ```

---

#### Feature enhancement:

1. Currently we are focussing on account level, in the coming days the platform will support org level visibility providing these features at the overall organization level
