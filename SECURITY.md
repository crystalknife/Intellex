# Security Policy

Thank you for helping keep Intellex secure.

The security of Intellex is an important part of the project's long-term success. If you discover a security vulnerability, we encourage you to report it responsibly so it can be investigated and resolved before public disclosure.

---

# Supported Versions

At this stage of development, only the latest release is actively supported.

| Version | Supported |
|----------|-----------|
| v0.1.x | ✅ |
| Earlier Versions | ❌ |

As Intellex evolves, this policy will be updated to include supported release branches.

---

# Reporting a Vulnerability

If you believe you have found a security vulnerability, please do **not** open a public GitHub issue.

Instead:

- Open a private GitHub Security Advisory (if enabled), or
- Contact the project maintainer directly through GitHub.

When reporting a vulnerability, please include:

- Description of the issue
- Steps to reproduce
- Potential impact
- Affected components
- Suggested mitigation (if known)

Reports with clear reproduction steps are greatly appreciated.

---

# Responsible Disclosure

Please allow reasonable time for the vulnerability to be investigated and addressed before publicly disclosing details.

Responsible disclosure helps protect users while fixes are prepared.

---

# Scope

Examples of issues that should be reported include:

- Remote code execution
- Authentication bypass
- Privilege escalation
- Sensitive information exposure
- Dependency vulnerabilities
- Injection attacks
- Cross-Site Scripting (XSS)
- Server-Side Request Forgery (SSRF)
- Cross-Site Request Forgery (CSRF)
- API authorization issues

---

# Out of Scope

The following are generally considered out of scope:

- UI suggestions
- Performance improvements
- Documentation mistakes
- Feature requests
- Browser compatibility issues
- Non-security-related bugs

Please report these through GitHub Issues instead.

---

# Dependencies

Intellex relies on several open-source libraries and frameworks.

Dependencies should be kept up to date to receive important security fixes.

Major dependencies include:

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Next.js
- React
- TypeScript
- spaCy

---

# Security Best Practices

Contributors should:

- Never commit secrets or API keys.
- Use environment variables for configuration.
- Keep dependencies updated.
- Validate external input.
- Follow the principle of least privilege.
- Review third-party packages before adding them.

---

# Future Security Roadmap

Future releases will introduce additional security features, including:

- Authentication
- Role-based access control
- API keys
- Audit logging
- Rate limiting
- HTTPS deployment guidance
- Security scanning in CI/CD

---

# Acknowledgements

We appreciate everyone who takes the time to responsibly report security issues and help improve Intellex.

Security is a shared responsibility, and every contribution helps make the project more reliable.