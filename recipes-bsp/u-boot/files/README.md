# U-Boot patch and fragments

Files that u-boot-qcom_git.bb adds to the U-Boot build.

## Files

- [README.md](README.md) — Indexes this folder.
- [0001-Add-support-for-OpenSSL-Provider-API.patch](0001-Add-support-for-OpenSSL-Provider-API.patch) — Adds OpenSSL Provider API support to U-Boot.
- [disable-eficapsule-tool.cfg](disable-eficapsule-tool.cfg) — Disables building the `mkeficapsule` tool.
- [efi-rt-volatile-store.cfg](efi-rt-volatile-store.cfg) — Lets the OS set EFI variables at runtime through the in-RAM store.
- [gunyah-exit.cfg](gunyah-exit.cfg) — Enables Gunyah EL2 exit handling, used when the machine has the kvm feature.
- [spl-fit-signature.cfg](spl-fit-signature.cfg) — Enables FIT signature checking in the SPL.
- [tfa-optee.cfg](tfa-optee.cfg) — Enables the TF-A based OP-TEE interface, used when the machine has the optee feature.
