# ModemManager patches

Patches that the ModemManager append applies on Qualcomm machines.

## Files

- [README.md](README.md) — Indexes this folder.
- [0001-iface-modem-messaging-sms-Add-TA-storage-support-for.patch](0001-iface-modem-messaging-sms-Add-TA-storage-support-for.patch) — Adds TA storage support to modem messaging and SMS.
- [0001-port-qmi-add-BAM-DMUX-DPM-support-and-fix-QRTR-WDA.patch](0001-port-qmi-add-BAM-DMUX-DPM-support-and-fix-QRTR-WDA.patch) — Adds BAM-DMUX DPM support to the QMI port and fixes QRTR WDA.
- [0001-qcom-soc-add-QRTR-MHI-based-modem-support.patch](0001-qcom-soc-add-QRTR-MHI-based-modem-support.patch) — Adds QRTR and mhi_net support for PCIe-attached SDX modems.
- [0002-base-modem-allow-QMI-modem-creation-without-net-port.patch](0002-base-modem-allow-QMI-modem-creation-without-net-port.patch) — Allows QMI modems to be created without a net port.
- [0002-fixup-move-json-glib-dep-to-root-meson.build-add-to-.patch](0002-fixup-move-json-glib-dep-to-root-meson.build-add-to-.patch) — Moves the json-glib dependency to the root meson.build.
- [0003-bearer-qmi-use-BindMuxDataPort-for-BAM-DMUX-WDS-client.patch](0003-bearer-qmi-use-BindMuxDataPort-for-BAM-DMUX-WDS-client.patch) — Uses BindMuxDataPort for the BAM-DMUX WDS client.
- [0003-whitespace-cleanup.patch](0003-whitespace-cleanup.patch) — Cleans up whitespace in the SMS storage changes.
- [0004-plugins-qcom-soc-send-DPM-open-port-during-enabling.patch](0004-plugins-qcom-soc-send-DPM-open-port-during-enabling.patch) — Sends the DPM open-port request while enabling the qcom-soc modem.
- [0004-whitespace-cleanup-fix-error-freeing.patch](0004-whitespace-cleanup-fix-error-freeing.patch) — Cleans up whitespace and fixes error freeing.
- [0005-plugins-qcom-soc-replace-sio_port_per_port_number.patch](0005-plugins-qcom-soc-replace-sio_port_per_port_number.patch) — Replaces the qcom-soc plugin's sio_port_per_port_number table.
- [0005-remove-dead-code.patch](0005-remove-dead-code.patch) — Removes dead code from the SMS storage changes.
- [0006-qmi-error-free-fixup.patch](0006-qmi-error-free-fixup.patch) — Fixes QMI error freeing.
- [0007-whitespace-fixes-some-memory-leak-fixes.patch](0007-whitespace-fixes-some-memory-leak-fixes.patch) — Fixes whitespace and some memory leaks.
- [0008-whitespace-fixes-and-adjust-some-sms-storage-functio.patch](0008-whitespace-fixes-and-adjust-some-sms-storage-functio.patch) — Fixes whitespace and adjusts some SMS storage functions.
- [0009-sms-storage-do-hex-binary-conversion-in-sms-storage.patch](0009-sms-storage-do-hex-binary-conversion-in-sms-storage.patch) — Moves hex and binary conversion into SMS storage.
- [0010-sms-storage-Add-slot-info-for-TA-SMS-in-DB.patch](0010-sms-storage-Add-slot-info-for-TA-SMS-in-DB.patch) — Stores slot information for TA SMS in the database.
