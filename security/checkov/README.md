# Custom Infrastructure-as-Code (IaC) Policy Enforcement

This directory contains custom Checkov static analysis policies written in Python. These policies are enforced during our CI/CD linting phase (via GitHub Actions) against CloudFormation templates to ensure all deployed infrastructure meets our organization's security, cost-optimization, and operational baselines.

## Policy Matrix

| Policy File                   | Category            |
| :---------------------------- | :------------------ |
| `cloudwatch_log_retention.py` | Cost & Operations   |
| `launch_template_gp3.py`      | Cost & Performance  |
| `mandatory_tags.py`           | Governance / FinOps |

---

## Detailed Policy Rationales

### 1. CloudWatch Log Retention ([`cloudwatch_log_retention.py`](./organization_policies/cloudwatch_log_retention.py))

- **Rule:** Enforces a strict retention period of exactly 30 days for all CloudWatch Log Groups.
- **Business & Technical Rationale:**
  - **Operational Visibility:** 30 days provides an optimal window to debug application errors, system anomalies, or `cloud-init` boot failures.
  - **FinOps Optimization:** AWS defaults log retention to "Never Expire," leading to silent, compounding storage costs over time. Standardizing on 30 days eliminates dead storage while keeping logs long enough to be shipped to a cold storage data lake if needed for long-term compliance.

### 2. EC2 GP3 Volume Enforcement ([`launch_template_gp3.py`](./organization_policies/launch_template_gp3.py))

- **Rule:** Restricts block device configurations in Launch Templates to `gp3` only, blocking legacy `gp2` or magnetic volumes.
- **Business & Technical Rationale:**
  - **Cost Efficiency:** `gp3` volumes offer a baseline 20% lower price per GB per month compared to `gp2`.
  - **Architectural Decoupling:** Unlike `gp2`, where IOPS and throughput are tied directly to the size of the volume (forcing over-provisioning), `gp3` allows us to scale IOPS and throughput independently of storage capacity. Every volume starts with a free baseline of 3,000 IOPS and 125 MB/s.

### 3. Enterprise Tag Standardization ([`mandatory_tags.py`](./organization_policies/mandatory_tags.py))

- **Rule:** Enforces the presence of four mandatory keys on all taggable resources: `Environment`, `Project`, `Owner`, and `ManagedBy`.
- **Business & Technical Rationale:**
  - **FinOps Accountability:** Essential for accurate cost allocation, budget alerting, and generating granular AWS Cost Explorer reports.

---

## Local Development & Testing

To run these custom policies against your local CloudFormation templates prior to committing:

```bash
checkov --external-checks-dir . --framework cloudformation -f template.yaml
```

In the current context:

```bash
checkov -d ./infra --external-checks-dir . --framework cloudformation -o json > output.json
```
