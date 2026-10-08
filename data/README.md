# Data provenance and redistribution

The study uses generated in-process simulator traces, not CIC-IDS2017, UNSW-NB15, human-subject data, or production attack traffic. Full raw traces are under analysis/validation-v1 and analysis/simulator-development-v1. Their manifests hash the exact released bytes. Do not pool the development and validation populations.

Cyberwheel source and network configurations are acquired from ORNL/cyberwheel at 6e535b50eea991ed48bb9eeb46b4b267090cc897 under its MIT license. The unmodified checkout is ignored rather than vendored. Source-audit-v0 records the initial selected-file audit; runtime-provenance.json adds a full tracked-file inventory and the actual installed environment.

The author's original generated records and code remain unlicensed for now. Public availability does not imply an open-source license for original work. Third-party notices remain in THIRD_PARTY_NOTICES.md. CoADAM and OPEN source checkouts were reviewed locally, not copied into this repository. No copyrighted paper PDFs are redistributed.

The trace schema includes synthetic host identifiers and simulated impact observations. Memory counts include repeated successes; the outcome counts each impacted original server only once per encounter. Oracle decoy labels and protected-target membership are evidence for scoring/audit, not input to the added memory selector.
