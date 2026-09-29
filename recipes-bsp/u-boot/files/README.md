# recipes-bsp/u-boot/files

Patch and configuration fragments that u-boot-qcom uses.

## Files

- [0001-Add-support-for-OpenSSL-Provider-API.patch](0001-Add-support-for-OpenSSL-Provider-API.patch) — Adds OpenSSL Provider API support.
- [disable-eficapsule-tool.cfg](disable-eficapsule-tool.cfg) — Disables the mkeficapsule tool.
- [efi-rt-volatile-store.cfg](efi-rt-volatile-store.cfg) — Allows EFI SetVariable at runtime on the in-RAM variable store.
- [gunyah-exit.cfg](gunyah-exit.cfg) — Enables Gunyah EL2 exit handling.
- [README.md](README.md) — Introduces this folder and indexes its contents.
- [spl-fit-signature.cfg](spl-fit-signature.cfg) — Makes the SPL enforce FIT signatures.
- [tfa-optee.cfg](tfa-optee.cfg) — Enables TF-A based OP-TEE support.
