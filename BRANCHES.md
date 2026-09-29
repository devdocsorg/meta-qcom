# Branches

Long-lived branches of meta-qcom. Status combines the
[Yocto Project release support](https://wiki.yoctoproject.org/wiki/Releases) for the
branch's release series with its last commit date; the repository does not state a
maintenance period for any branch. Where to send changes for each branch is in the
[contribution guide](docs/source/contributing/CONTRIBUTING.md#where-to-send-changes).

| Branch | Purpose | Status | Build from it | Relationship to `master` |
| --- | --- | --- | --- | --- |
| `master` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Active; supports the `wrynose` series. | Yes: the [quick build](README.md#quick-build) uses it. | The default branch. |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Yocto Project 6.0 is supported until April 2030; last commit September 2026. | Yes, for Qualcomm Linux 2.x. | Maintained separately; fixes are [backported from `master`](docs/source/contributing/AGENTS.md#8-backporting-to-a-release-branch). |
| `next` | Testing workflow changes before they are merged to `master`, as the branch's own README states. | Last commit September 2026. | No: it is not a release; build from `master`. | Its workflow changes are meant to reach `master`. |
| `scarthgap` | Legacy branch maintained by Linaro before the migration to [qualcomm-linux](https://github.com/qualcomm-linux). | Yocto Project 5.0 is supported until April 2028; last commit December 2024. | Only with other `scarthgap` layers; it holds three machine configurations. | Maintained separately. |
| `kirkstone` | Legacy branch maintained by Linaro before the migration. | Yocto Project 4.0 is end of life; last commit December 2024. | Only with other `kirkstone` layers. | Maintained separately. |
| `styhead`, `honister`, `dunfell`, `zeus`, `warrior`, `thud`, `sumo`, `rocko`, `pyro`, `morty`, `krogoth`, `jethro` | Legacy branches maintained by Linaro before the migration, one per Yocto Project release. | Their Yocto Project releases are end of life; last commits between November 2016 (`krogoth`) and January 2025 (`styhead`). | Only with other layers of the same release. | Maintained separately. |

Temporary `backport/<pull-request>-to-wrynose` branches are created by the
[backport workflow](https://github.com/qualcomm-linux/meta-qcom/blob/master/.github/workflows/backport.yml)
and are listed with the other current branches in the
[README](README.md#branches).
