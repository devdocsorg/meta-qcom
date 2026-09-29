# test-keys

Test PKI files for signing UEFI firmware capsules in CI. `ci/capsule-test-keys.yml` points the `qcom-capsule` class at them through `LAYERDIR_qcom`; they must not be used for production images.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [QcFMPCert.pem](QcFMPCert.pem) — Test signing certificate and its private key in PEM form, used as `CAPSULE_CERT_PEM`.
- [QcFMPRoot.cer](QcFMPRoot.cer) — DER-encoded test root CA certificate, used as `CAPSULE_ROOT_CER`.
- [QcFMPRoot.pub.pem](QcFMPRoot.pub.pem) — Test root CA certificate in PEM form, used as `CAPSULE_ROOT_PUB`.
- [QcFMPSub.pub.pem](QcFMPSub.pub.pem) — Test intermediate CA certificate in PEM form, used as `CAPSULE_SUB_PUB`.
