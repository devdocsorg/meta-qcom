# time-services

Recipe for the time-services daemon.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [time-services_0.1.1.bb](time-services_0.1.1.bb) — Builds `time-daemon`, which sets the system time from the modem once it is on a network, with its systemd service; it does not coordinate with systemd-timesyncd, NTP, or chrony.
