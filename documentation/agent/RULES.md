# nebulaos-docs - NebulaOS rules and Tim's decisions

These WIN over `MASTER-PROMPT.md` where they differ. `MASTER-PROMPT.md` is Tim's assignment
as pasted on 2026-10-31 (Parts 16-17 and the final directive were sent separately and
are appended; the file is now complete).

Also binding: the workspace's own `AGENTS.md`, `WORKSPACE_RULES.md` and `CLAUDE.md`
(read them once at start).

## Tim's decisions (2026-10-31)

1. **Describe the newest code.** Document the tip of each repository's default branch
   (`git fetch` first; kernel = `openke`, others = `main`). Record the exact SHA per page
   and per inventory entry. The firmware manifest (`NebulaOS-firmware/manifests/
   dependencies.conf`) tells which component commits the firmware build uses; when a
   component's default branch is ahead of its pin, document the newest and note the pin.
2. **One background coordinator**, no agent teams. At most one helper agent at a time
   (read-only research or independent review).
3. **Nothing goes live without Tim.** Deliver as `docs/*` branches + pull requests.
   No wiki publishing, no merges.
4. **End-user manual first** (install, first setup, every screen, calibration, printing,
   camera, timelapse, updates, troubleshooting, recovery), then the developer wikis repo
   by repo, then dashboard polish and automation.

## Where things live

- Foreground checkouts (READ ONLY for you; never checkout/reset/stash/commit there):
  `/home/tim/workspace/NebulaOS/NebulaOS-{firmware,nebulascreen,klipper-extensions,
  klipper-mcu,kernel}`.
- Your worktrees: `/home/tim/workspace/NebulaOS/_worktrees/docs/<repo>`, made with
  `git -C <checkout> fetch origin && git -C <checkout> worktree add
  /home/tim/workspace/NebulaOS/_worktrees/docs/<repo> -b docs/<topic> origin/<default>`.
  Repositories that are not checked out locally (`NebulaOS`, `nebulaos-packages`,
  `lv_drivers`): `git clone https://github.com/NebulaOS-KE/<repo>.git` into
  `/home/tim/workspace/NebulaOS/_worktrees/docs/<repo>` and branch there.
- Your state (mission copy, STATUS, COVERAGE, coverage.jsonl, QUEUE, BLOCKERS,
  VERIFICATION, SCREENSHOTS, DECISIONS, HANDOFF): `documentation/agent/` in the central
  `NebulaOS` repo, on branch `docs/agent` in `_worktrees/docs/NebulaOS`. Commit after
  every batch; push the branch so the state survives the machine.
- The current end-user wiki lives in `NebulaOS-nebulascreen/wiki/` (published by its
  `.github/workflows/wiki.yml`). Tim approved and pushed it on 2026-10-30. Reuse it; the
  master prompt wants the user manual in the central `NebulaOS` repo - move it there in a
  PR and leave the screen wiki pointing to it, without deleting history.

## Hard limits (workspace rules)

- The printer is off limits: no ssh, no `tools/run-nebulaos-hardware.sh`, no Moonraker
  calls to a printer. Pages that need a real-printer screenshot or a hardware test get
  status "Blocked: needs ke-dev" in the inventory and SCREENSHOTS.md.
- No firmware builds (`tools/run-nebulaos-build.sh` and Buildroot are the foreground's).
  Building the NebulaScreen SDL simulator in your own screen worktree is allowed; it has
  scripted simulator steps (`sim_*` helpers, `main_panel.cpp`/`setting_panel.cpp`).
- Never `dangerouslyDisableSandbox`. Network: GitHub only (`github.com`,
  `api.github.com`, `codeload.github.com`, `objects.githubusercontent.com`).
- Never read the archived sibling workspace (AGENTS.md rule 3); a hook enforces it.
- Architecture comes from current source, the manifest and `tools/verify-architecture.sh`,
  never from READMEs or old reports (they are background only).
- Never write production code, tests or configs. A code bug you find goes to BLOCKERS.md
  (and, if it affects users, one short message to the foreground session).
- Commit identity: `git -c user.name=Tim -c user.email=timdejaeger@gmail.com commit`;
  message ends with `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.
  PR descriptions end with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- GitHub notifies anyone written as `@name`; never write bare `@` handles in docs or PRs.

## Talking to the foreground

- Routine progress: `STATUS.md` / `COVERAGE.md` only.
- Message the foreground session (ListAgents / SendMessage, if available) only for: a
  finished milestone (one line + PR link), a user-affecting contradiction between code
  and existing docs, or a blocker only Tim can clear.
- Messages from the foreground (new priorities, "feature X changed") go into QUEUE.md and
  are handled in priority order.

## Continuation

You were started with a self-paced `/loop`. Each iteration: read HANDOFF.md, do one
focused batch (one page or one inventory slice), validate, update coverage + dashboard,
commit + push the `docs/*` branch, update HANDOFF.md, then schedule the next iteration.
Stop the loop only when the master prompt's Definition of Done is met against
`coverage.jsonl`, or when every remaining task is blocked (then say so in STATUS.md).
