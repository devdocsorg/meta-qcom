---
name: Bug report
about: Report a problem with the layer, its builds, or its documentation
---

<!-- markdownlint-disable-file MD041 -->

For vulnerabilities, use the private route in
[SECURITY.md](https://github.com/qualcomm-linux/meta-qcom/blob/master/SECURITY.md).
Search existing issues before submitting and remove confidential information.

## Problem

Describe the problem and identify the affected recipe, machine, branch, or commit.

## Reproduction

Give the smallest sequence of steps that shows the problem, including the kas
fragments or `MACHINE` and `DISTRO` you built with.

## Expected and actual result

Explain what should happen and what happens instead. Include error messages
and relevant log excerpts as text.

## Context

Include related issues, the host and container setup, and the layer revisions
from `ci/base.lock.yml` or `bitbake-layers show-layers`. Omit fields that do
not apply.
