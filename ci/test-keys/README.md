# Capsule test keys

Development PKI files that `ci/capsule-test-keys.yml` uses to sign UEFI
capsules in CI. They are public test material; never use them in production
images.

## Files

- [README.md](README.md) — Indexes this folder.
- [QcFMPCert.pem](QcFMPCert.pem) — Holds the test signing certificate and its private key (`CAPSULE_CERT_PEM`).
- [QcFMPRoot.cer](QcFMPRoot.cer) — Holds the test root certificate in DER form (`CAPSULE_ROOT_CER`).
- [QcFMPRoot.pub.pem](QcFMPRoot.pub.pem) — Holds the test root certificate in PEM form (`CAPSULE_ROOT_PUB`).
- [QcFMPSub.pub.pem](QcFMPSub.pub.pem) — Holds the test intermediate certificate (`CAPSULE_SUB_PUB`).
