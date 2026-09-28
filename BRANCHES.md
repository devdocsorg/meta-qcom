# Branches

Upstream support status comes from the Yocto Project
[releases page](https://wiki.yoctoproject.org/wiki/Releases); last commits
were read on 2026-09-28 from each branch's
[commit history](https://github.com/qualcomm-linux/meta-qcom/branches/all).
[CONTRIBUTING.md](CONTRIBUTING.md) says where changes go.

| Branch | Why it exists | Status | Relationship to master |
| --- | --- | --- | --- |
| `master` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Active; last commit 2026-09-28. | Canonical branch. |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Active; last commit 2026-09-28. Yocto Project 6.0 has long-term support until April 2030. | Maintained separately; fixes land on `master` first and are backported, as the [agent guide](AGENTS.md#8-backporting-to-a-release-branch) describes. |
| `next` | For testing workflow changes before being merged to master, as the [branch's README](https://github.com/qualcomm-linux/meta-qcom/blob/118efae71cfbaaa16fb79f14f83bfa23e4f2b151/README.md#branches) states. | Last commit 2026-09-25. | Its workflow changes are tested there before they merge to `master`. |
| `kirkstone`, `scarthgap`, `styhead`, `honister`, `dunfell`, `zeus`, `warrior`, `thud`, `sumo`, `rocko`, `pyro`, `morty`, `krogoth`, `jethro` | Legacy stable branches maintained by Linaro, prior to the migration to [qualcomm-linux](https://github.com/qualcomm-linux); each targets the Yocto Project release it is named after. | Last commits: `styhead` 2025-01-29, `kirkstone` 2024-12-20, `honister` and `dunfell` 2024-12-10, `scarthgap` 2024-12-03, `sumo` 2021-02-12, `zeus` 2020-03-30, `warrior` 2020-02-13, `thud` 2019-05-15, `rocko` 2018-08-23, `morty` 2018-06-28, `pyro` 2017-10-16, `jethro` 2017-05-10, `krogoth` 2016-11-04. Upstream, Yocto Project 5.0 (`scarthgap`) has long-term support until April 2028; the other releases are end of life. | Maintained separately; not merged back. |
| `backport/<pull request>-to-wrynose` | Temporary branches that [backport.yml](.github/workflows/backport.yml) creates for merged pull requests labelled `backport wrynose`. | One per open automated backport. | Each is the head of a pull request into `wrynose`. |

[SECURITY.md](SECURITY.md) accepts patches only for the LTS releases and
`master`. The repository does not document how long `backport/*` branches are
kept.
