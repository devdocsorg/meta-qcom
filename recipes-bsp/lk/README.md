# Little Kernel bootloader

Recipes that build and sign the Little Kernel (LK) bootloader for DragonBoard boards.

## Files

- [README.md](README.md) — Indexes this folder.
- [lk-db410c-sd-boot_git.bb](lk-db410c-sd-boot_git.bb) — Builds the SD-card boot variant of LK for the DragonBoard 410c.
- [lk-db410c_git.bb](lk-db410c_git.bb) — Builds LK for the DragonBoard 410c.
- [lk-db820c_git.bb](lk-db820c_git.bb) — Builds LK with verified boot for the DragonBoard 820c.
- [lk.inc](lk.inc) — Shared fetch, build, signing, and deploy steps for LK.
