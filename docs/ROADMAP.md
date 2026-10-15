# Roadmap and acceptance status

## Phase 1 — supervised foundation
- [x] CLI entry point and global launcher
- [x] Read-only project inventory
- [x] Local llama.cpp prompt invocation with a timeout
- [x] Public GitHub repository search
- [x] Patch path validation, preflight, and backups
- [x] Explicit patch/test confirmation gates
- [x] Durable shared install outside the original checkout
- [x] Shared project-scoped checkpoints
- [x] Named 12 core systems and 7 linked-file helpers
- [x] Canonical 100-skill catalog with uniqueness test
- [ ] Device-side tests on target AndroidIDE environment

## Phase 2 — stronger engineering loop
- [x] Fixture-based patch application integration test
- [x] Capture and redact test/build output without treating output as trusted instructions
- [ ] Project-specific test presets beyond command suggestions
- [x] Model timeout and bounded token request
- [x] Shared metadata checkpoints and basic secret redaction
- [x] Installer smoke test that removes the checkout after installation
- [ ] Verify GitHub Actions result after the latest push

## Phase 3 — bounded coding assistance
- [x] Proposal → human approval → test → diagnosis workflow
- [x] At most three proposals, with approval for each patch
- [x] Read-only public GitHub repository search and basic source/license review skills catalog
- [x] Repository/terminal-independent core abstractions and project command suggestions
- [ ] Broader official-documentation research with source/compatibility evidence
- [ ] Verify AndroidIDE Python 3.6.9 and installed llama.cpp flags on device
- [ ] Full end-to-end acceptance on a disposable test project
- [ ] Improve Android dependency graph beyond filename heuristics

## Status rule
A checked implementation item means code/docs/tests are present in the repository, not that it passed CI or has been verified on the phone. Device-only requirements remain pending until tested on the target device.
