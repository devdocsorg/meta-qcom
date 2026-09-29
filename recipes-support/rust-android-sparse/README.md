# rust-android-sparse

Recipe for android-sparse, a Rust implementation of Android's sparse image format, available for the target and as a native tool.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [rust-android-sparse-crates.inc](rust-android-sparse-crates.inc) — Lists the crates from `Cargo.lock` and their checksums, generated with `bitbake -c update_crates rust-android-sparse`.
- [rust-android-sparse_0.6.0.bb](rust-android-sparse_0.6.0.bb) — Builds the android-sparse 0.6.0 crate from crates.io with cargo.
