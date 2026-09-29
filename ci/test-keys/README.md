# ci/test-keys

Development keys and certificates that ci/capsule-test-keys.yml uses to sign UEFI capsules; never use them in products.

## Files

- [QcFMPCert.pem](QcFMPCert.pem) — Holds the test signing key and leaf certificate.
- [QcFMPRoot.cer](QcFMPRoot.cer) — Holds the test root certificate in DER form.
- [QcFMPRoot.pub.pem](QcFMPRoot.pub.pem) — Holds the test root certificate in PEM form.
- [QcFMPSub.pub.pem](QcFMPSub.pub.pem) — Holds the test intermediate certificate in PEM form.
- [README.md](README.md) — Introduces this folder and indexes its contents.
