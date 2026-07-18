# Concepts, important things to remeber

- Run **dos2unix** before yamllint(as yamllint considers Unix(/n) and when you edit the code in Windows machine it considers /r/n).

- Cloudwatch
  1. Log event
  2. Log group
  3. Log stream

- **cloud-init**

- Understand the user-data

- Check about describe-stack, query

- **Working of GitHub OIDC**
  1. **GitHub Actions** acts as an **_OIDC Identity Provider_** and uses the OIDC protocol to issue a short-lived **_JWT_** containing metadata such as **_repository, branch, workflow, job, and environment._**

  2. When GitHub Actions needs AWS access, it sends this JWT to **_AWS STS_** using **_AssumeRoleWithWebIdentity_**.

  3. **_AWS STS_** verifies the authenticity of the token (signature, issuer, audience) and validates the claims against the **_IAM role trust policy_**.

  4. If validation succeeds, STS issues short-lived **_temporary credentials_** scoped to the permissions of the IAM role.

  5. GitHub Actions then uses these temporary credentials to interact with AWS services for the duration of the job.

- Why we need CreationPolicy, UpdatePolicy, UpdateReplacePolicy

- Why we should not do the below one
  - app/\* changes -> trigger app pipeline -> pushes to s3 -> deploy the changed app code into all existing/running servers using ssm
  - This is a mutable deployment model where we are deploying the code changes to running servers
  - If there is some bug or anything wrong we would be applying the same to all servers
  - Possibility of significant downtime, ssm is being used for app deployment rather than for debugging, patching, automating, conducting operational task

- cfn-signal -> provisioning success
  ALB health -> runtime health check
  Both should be successful for the server to receive the traffic

- PauseTime -> Wait time after each batch is successfully deployed

- How **rollback** works?
  - On success:
    - _new instance fails_ → terminate it → keep old version → stop rollout
  - On failure:
    - _launch new_ → verify → terminate old → repeat
  - Point to note:
    - ASG only replaces old instances AFTER new ones are proven healthy

- WaitOnResourceSignals
  - until we get a success from cfn-signal post launch of a serer with new version, it will not mark it as healthy
  - If not mentioned, as soon as an instance boots it will mark it as healthy during updates(does'nt wait for installation of packages, creation of files, running commands, ensuring that services are up)
