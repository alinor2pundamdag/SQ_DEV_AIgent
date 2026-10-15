# Roadmap

## Phase 1 — supervised foundation
- [x] CLI entry point and global launcher
- [x] Read-only project inventory
- [x] Local llama.cpp prompt invocation
- [x] Public GitHub repository search
- [x] Patch path validation and backups
- [x] Explicit patch/test confirmation gates
- [ ] Device-side tests on the target AndroidIDE environment

## Phase 2 — stronger engineering loop
- [ ] Add fixture-based patch application integration tests
- [ ] Capture and parse test/build output without treating output as trusted instructions
- [ ] Add configurable project-specific test presets
- [ ] Add model output budget and timeout configuration
- [ ] Add structured logs with secret redaction

## Phase 3 — bounded autonomous assistance
- [ ] Build a proposal → human approval → test → diagnosis workflow
- [ ] Limit repair attempts to at most three and require approval before applying each repair
- [ ] Add a read-only dependency/license/security review
- [ ] Add repository adapter interface for multiple terminal environments

No phase should be marked complete without tests and evidence from the target environment.
