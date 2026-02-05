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
