# QCA utility patch and generators

Files the qca-swiss-army-knife recipe fetches: a patch and scripts that describe WLAN board data files in board-2.json format.

## Files

- [0001-scripts-use-usr-bin-env-python3.patch](0001-scripts-use-usr-bin-env-python3.patch) — Makes the upstream scripts run python3 through /usr/bin/env.
- [ath10k-generate-board-2_json.sh](ath10k-generate-board-2_json.sh) — Writes a board-2.json list of ath10k SNOC board files.
- [ath10k-generate-pci-board-2_json.sh](ath10k-generate-pci-board-2_json.sh) — Writes a board-2.json list of ath10k PCI board files.
- [ath11k-generate-ahb-board-2_json.sh](ath11k-generate-ahb-board-2_json.sh) — Writes a board-2.json list of ath11k AHB board files.
- [ath11k-generate-pci-board-2_json.sh](ath11k-generate-pci-board-2_json.sh) — Writes a board-2.json list of ath11k PCI board files.
- [README.md](README.md) — Indexes this folder.
