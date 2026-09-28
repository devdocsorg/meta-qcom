# linux-yocto-dev workarounds

Device tree patches that linux-yocto-dev.bbappend applies to work around board issues.

## Files

- [README.md](README.md) — Indexes this folder.
- [0001-PENDING-arm64-dts-qcom-Remove-voltage-vote-support-f.patch](0001-PENDING-arm64-dts-qcom-Remove-voltage-vote-support-f.patch) — Removes a voltage vote from a Qualcomm device tree node; pending upstream.
- [0001-QCLINUX-arm64-dts-qcom-qcm6490-disable-sdhc1-for-ufs.patch](0001-QCLINUX-arm64-dts-qcom-qcm6490-disable-sdhc1-for-ufs.patch) — Disables SDHC1 on QCM6490 boards that boot from UFS.
