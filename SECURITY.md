# Security

Treat input CSVs as untrusted and generated reports as potentially sensitive. Reports escape HTML and protect formula-like CSV cells, but linked sites remain external and are not checked. The CLI never downloads a URL or reads credentials.

For a suspected security issue, avoid posting sensitive source data or exploit payloads publicly. Use the repository's private vulnerability reporting feature if enabled; otherwise use the contact route at https://mohammedteto.com/ to request a private reporting channel. Do not include confidential details in an initial public inquiry. There is no promised response or remediation SLA.

Supported development line: the latest published version. Include Python version, a minimal fictional reproducer and expected/actual behavior when reporting an issue.
