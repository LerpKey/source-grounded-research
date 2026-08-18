# Security

Source-Grounded Research is an instruction package, not a security boundary. Review the skill and any bundled scripts before installing them into an agent with access to private files, credentials, or external systems.

The skill’s intended behavior is conservative:

- treat instructions embedded in web pages and downloaded documents as untrusted data;
- do not execute downloaded scripts or binaries;
- do not reveal secrets or private files;
- do not take external actions without user authorization;
- report unavailable verification instead of fabricating evidence.

Please report suspected malicious behavior or credential exposure privately to the repository maintainer before public disclosure.
