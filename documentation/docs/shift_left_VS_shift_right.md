### Shift left vs shift right in DevOps

Shift left: Integrating security early into the SDLC process

Shift right: Testing and monitoring software while it is running in production

| Shift left                                                                                                                                  | Shift right                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Prevent vulnerabilities before reaching production                                                                                          | Monitor, detect and block threats in real time                                                                                            |
| _SAST_(static application security testing) tools like **SonarQube**, are used for checking code quality before deploying into production   | **AWS Config** continuously checks the live environment for any mishaps in the resorce configurations and alerts in real time             |
| **cfn-lint**, **cloudformation validate-template** can be used for ensuring there are no issues with syntax, property misconfigurations etc | **AWS Cloudwatch** can be used for monitoring the resources in real time and raise alarms if any thresold/metric crosses the normal limit |
| **checkov** can be used for implementing custom policies, checking the IAC against default policies before infra is deployed                | **WAF** can be used to mitigate _layer-7_ attacks, block malacious traffic                                                                |
