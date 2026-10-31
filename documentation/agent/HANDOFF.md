# Handoff - read this to resume

You are `nebulaos-docs`, a long-running background documentation session for NebulaOS. This
file is the resume point. Read it, then continue with "Next actions" at the bottom. Do not
start the project over.

## The mission in one paragraph

Produce the real documentation for the whole NebulaOS project - a complete beginner-friendly
end-user manual in the central `NebulaOS` repository, and developer references for every
component repository - written from the actual source code, with an honest, generated
coverage dashboard, delivered as `docs/*` branches and pull requests. Not a plan, not an
outline: the pages themselves. The full assignment is in `MISSION.md`; `RULES.md` holds the
workspace rules and the owner's decisions and wins wherever the two differ.

## Current phase

**Phase 1 - repository discovery and coverage inventory.** Commands, configuration,
screens and services are discovered: **355 items** recorded. Phase 0 (infrastructure) is
finished. Two discovery slices remain before Phase 2 writing begins in earnest.

## Completed

- All eight organisation repositories enumerated with default branches and tip commits.
- Docs worktree created: `_worktrees/docs/NebulaOS`, branch `docs/agent`.
- Tracking system built in `documentation/agent/`: mission, rules, status, queue, blockers,
  verification policy, screenshot inventory, decisions, handoff, and two scripts.
- `coverage.jsonl` holds 355 items: 8 repository references, 10 manual sections, 49
  NebulaScreen panels, 51 G-code commands, 172 configuration options, 30 extension modules,
  35 boot services.
- **Q-001 done** - the 8 G-code commands whose names are built from module constants are
  resolved and recorded with their constants in `tools/seed_inventory.py`.
- **Q-002 done** - configuration discovery, after fixing a first attempt that mistook 85
  Moonraker status-object pointers for settings. Read the note in `STATUS.md` before
  touching that code: the lesson is that a broad literal sweep over UI source looks
  productive and quietly fabricates inventory.
- `COVERAGE.md` generated from the inventory.
- Firmware shipping pins read from the manifest and recorded in `STATUS.md`.

## Active work

Nothing half-finished. The next batch starts clean.

## Remaining work

All of it, in `QUEUE.md`, in priority order. Phase 1 needs four more discovery slices
(configuration keys, APIs, developer commands, update/recovery mechanisms) before Phase 2
writing starts in earnest.

## Architectural findings so far

- **NebulaOS is not a Klipper fork.** Host Klipper is pristine upstream `Klipper3d/klipper`
  pinned at `58bd67d` and owned by the firmware build. Custom behaviour lives in
  `NebulaOS-klipper-extensions` as loadable `extras/` modules. Documentation must never
  present upstream Klipper behaviour as NebulaOS behaviour.
- **The extensions pin gap is cosmetic.** The firmware manifest pins the extensions to
  branch `production` at `31d6d65`; `main` is at `8e3447a`. The diff is three files - a CI
  workflow, a CI script and a README edit - with nothing under `extras/`. Runtime code is
  identical, so every documented extension behaviour is shipped behaviour and pages get a
  footnote with the pin SHA rather than a development-only label. Do not re-derive this from
  the SHAs alone: a pin gap is a question, and the answer is in the diff.
- **The UI surface is large and well-structured.** 49 panels in `src/*_panel.cpp`, which is
  both the screen reference and the screenshot plan.
- **Boot and lifecycle are script-driven.** 35 ordered init scripts in the firmware overlay,
  covering revert safety, Wi-Fi, MCU guard, update supervision, image trial and
  confirm-good. These are the real source for the update, rollback and recovery pages.
- **The extensions have a real test suite** - 30 modules, 31 test files. That makes
  `verify_test` genuinely reachable for the Klipper command reference, which is rare and
  worth exploiting early: run the suite, cite the test, promote the status honestly.
- **Upstream commands are overridden, not just added.** `nebulaos_bed_soak.py` replaces
  upstream Klipper's `SET_PIN`, and `nebulaos_z_adjust.py` deregisters and replaces
  `Z_OFFSET_APPLY_PROBE`. Those two must be documented as modified upstream behaviour, not
  as NebulaOS inventions - getting attribution wrong here would mislead anyone coming from
  stock Klipper.
- **Existing documentation is substantial, not disposable.** 34 end-user wiki pages in
  `NebulaOS-nebulascreen/wiki/` approved on 2026-10-30, and about 70 design and analysis
  documents in `NebulaOS-firmware/docs/`. Reuse before rewriting.

## Source revisions in use

| Repository | Branch | Commit |
|---|---|---|
| `NebulaOS` | `main` | `bef8693fb1f415ee874a250a7e9a0115831c14ef` |
| `NebulaOS-firmware` | `main` | `82e132088fc789edc920e4f9e13173effacac50d` |
| `NebulaOS-nebulascreen` | `main` | `94869f75657270200a306c5a54d694eb6adf7b74` |
| `NebulaOS-klipper-extensions` | `main` | `8e3447ac0da435d42be6d6e699c54385fedf846d` |
| `NebulaOS-klipper-mcu` | `main` | `33f5d16daccd9ff5e5c0be61f3d44406440558f2` |
| `NebulaOS-kernel` | `openke` | `d86790d2e23178e52054c71562f9c40994a5469b` |

Re-check these at the start of each session with `git fetch`; if a tip moved, mark the
affected inventory items for re-verification rather than assuming the pages still hold.

## Blockers

`BLOCKERS.md`: B-001 no printer access (by design; simulator is the mitigation), B-002 two
repositories not yet cloned locally.

## Branches and pull requests

- `docs/agent` in `NebulaOS` - the agent's state and the user manual. Pushed.
- No pull requests open yet.

## Next actions, in order

1. `git fetch` every repository and compare tips against the table above. If a tip moved,
   mark the affected items for re-verification instead of assuming the pages still hold.
2. Work **Q-003**: the Moonraker / JSON-RPC and WebSocket surface NebulaScreen uses, plus
   NebulaOS-specific methods and the Klipper status objects. The 85 status-object pointers
   rejected from configuration discovery are a ready-made starting list - find where they
   are subscribed and requested, and inventory them as API items.
3. Work **Q-004** and **Q-005**: developer commands and build targets across the five
   cloned repositories, then the update, rollback, A/B slot and recovery mechanisms.
4. Work **Q-006**: audit the 34 existing wiki pages and record a reuse decision for each -
   this decides how much of Phase 2 is writing versus adapting, so do it before writing.
5. Then open Phase 2 with **Q-010** and **Q-011**, the manual skeleton and the installation
   section, and raise the first pull request.

Each batch ends the same way: update `coverage.jsonl`, regenerate `COVERAGE.md`, update
`STATUS.md` and `QUEUE.md`, commit, push, update this file.

## Working rules that are easy to get wrong

- Commit with `git -c user.name=Tim -c user.email=timdejaeger@gmail.com commit`, message
  ending `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.
- Push only `docs/*`. Never `main`, `openke` or `production`. Never merge, never force-push,
  never run a wiki publish workflow.
- Edit only inside `_worktrees/docs/`. The checkouts at the workspace root belong to the
  foreground session - read them, never write them.
- Never write production code, tests or configuration. A code bug goes to `BLOCKERS.md`.
- No printer, no firmware builds, no `dangerouslyDisableSandbox`, never read the archived
  sibling workspace.
- Never write a bare GitHub handle with an at-sign in a document or pull request - it
  notifies a real person.
- Routine progress goes in these files. Message the foreground session only for a finished
  milestone, a user-affecting code/doc contradiction, or a real blocker.
