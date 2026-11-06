# Security Policy

## Supported code

Security fixes are considered for the current development version on the main branch. Older snapshots are research references and do not have a separate maintenance commitment. This is an academic project; no response-time guarantee is provided.

## Reporting a vulnerability

Please do not disclose exploitable details, credentials, or personal information in a public issue.

If GitHub private vulnerability reporting is available, use the repository's **Security → Report a vulnerability** option. Otherwise, contact the project lead privately through an existing team contact or a private contact channel the maintainer has published. If no private channel is available, open an issue requesting one without including vulnerability details.

Include the affected version or commit, relevant configuration, steps to reproduce, expected impact, and a minimal example with sensitive data removed. Coordinate any public disclosure with the maintainer after review and remediation.

## Safe usage

- Run only notebooks and code from sources you trust; notebook cells execute Python code.
- Keep Jupyter bound to the local machine unless you have configured appropriate authentication and network controls.
- Do not commit secrets, private data, virtual environments, or generated execution outputs.
- Review dependency updates and rerun the documented checks before using them for reported experiments.
