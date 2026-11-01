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

**Phase 2 is complete. Phase 3 is underway.**

The end-user manual is 29 pages with **no stubs**, covering all ten mission sections (10/10 on
`user-manual-section`). 128 screenshots, 41 of 57 required items captured.

**The extensions reference is done and is PR #3 on that repository** - 49 commands, 155
options, generated with `ast` from `a2e7634`. Branch `docs/extensions`.

**Those 193 items are `draft`, not `documented`, and that is deliberate.** The generated tables
give name, module, kind, description, type, default and constraints. Mission 6.5 and 6.6 also
require per-command preconditions, examples, expected output, errors, side effects and safety
warnings, and per-option purpose, runtime behaviour and restart requirements. Marking them
documented took the headline from 14% to 49% in one step, which was flattering and false. Do
not re-upgrade them without writing that detail.

**The firmware reference is PR #5 on that repository** - 58 API endpoints and 35 boot services,
branch `docs/firmware`, generated from `c377230`.

**Two fields, two meanings, do not merge them again.** `blockers` means something that cannot
proceed without hardware, access or a decision. `gaps` means work not yet done. Both were in
`blockers` at one point and the dashboard reported 57% "blocked", which reads as a stuck
project; the real split is 6 blocked and 311 gaps.

**Next:** Q-036 and Q-037 raise both references to the mission's per-item bar, which is where
most of the 289 draft items sit. Then NebulaScreen developer pages, the MCU, the kernel, and
`nebulaos-packages` / `lv_drivers` (still not cloned).

## Completed

- All eight organisation repositories enumerated with default branches and tip commits.
- Docs worktree created: `_worktrees/docs/NebulaOS`, branch `docs/agent`.
- Tracking system built in `documentation/agent/`: mission, rules, status, queue, blockers,
  verification policy, screenshot inventory, decisions, handoff, and two scripts.
- `coverage.jsonl` holds 544 items: 8 repository references, 10 manual sections, 49
  NebulaScreen panels, 51 G-code commands, 172 configuration options, 30 extension modules,
  35 boot services, 56 Moonraker API endpoints plus 1 notification, 17 OS helper modules, 14 build pipeline scripts, 11 tool sets, 56 overlay runtime
  helpers, 34 audited existing wiki pages.
- **Q-006 done** - the reuse audit, written up in `REUSE-AUDIT.md`.
- **Q-004 and Q-005 done** - the build pipeline, developer tooling, and the update /
  rollback / recovery surface. Counts verified independently and in agreement.
- **Q-001 done** - the 8 G-code commands whose names are built from module constants are
  resolved and recorded with their constants in `tools/seed_inventory.py`.
- **Q-020 done** - screenshot capture solved; 129 images from the documented commit.
- **Q-003 done** - the public Moonraker API surface, inventoried from the server-side
  registration table and cross-checked against UI call sites. Klipper status objects are the
  remaining follow-up.
- **Q-002 done** - configuration discovery, after fixing a first attempt that mistook 85
  Moonraker status-object pointers for settings. Read the note in `STATUS.md` before
  touching that code: the lesson is that a broad literal sweep over UI source looks
  productive and quietly fabricates inventory.
- `COVERAGE.md` generated from the inventory.
- Firmware shipping pins read from the manifest and recorded in `STATUS.md`.

## Active work

Nothing half-finished. 17 stub pages are placeholders by design, each saying so to the reader,
and each still counted `missing` in the inventory.

**Screenshots are solved.** 129 real captures at 480x272 from commit `94869f7`, in
`wiki/images/`, reproducible with `tools/capture_screenshots.sh`. The app has a built-in
headless tour (`GUPPY_SIM_SHOTS=<dir>`). 36 of 49 panels covered. Read `SCREENSHOTS.md` before
re-running it - three non-obvious build blockers are written up there.

**The remaining screenshot work is embedding, not capturing.** 7 of 129 are used in pages. Do
it page by page as you write, not as a sweep at the end.

**Q-060 is closed.** All of it landed and was verified: extensions `a2e7634`, screen
`3194104`, firmware `c377230`. Screenshots re-captured and compared. **The firmware pins now
match the repository tips exactly** for the extensions and the screen, so there is currently no
gap between documented and shipped behaviour there.

**When a tip moves again:** move the matching worktree, re-run the extensions test suite and
`tools/capture_screenshots.sh`, and compare. Run the capture tour twice against the same build
before concluding anything changed - one image (`07-updates.png`) is timing-dependent and will
otherwise look like a code change every time.

**The seeder now reads from the pinned worktrees, not the root checkouts.** The root ones are
the foreground session's and move without warning. Keep it that way: an evidence citation
naming a commit the tree no longer sits at is worse than no citation, because it looks
checked.

## Remaining work

**Phase 3, the developer wikis, has not been started at all.** That is the larger half of the
mission: six component repositories, 234 extension items, 194 firmware items, the API
reference, the command reference, the configuration reference. The end-user manual is well
advanced; do not mistake that for the project being well advanced.

All of it, in `QUEUE.md`, in priority order. Phase 1 needs four more discovery slices
(configuration keys, APIs, developer commands, update/recovery mechanisms) before Phase 2
writing starts in earnest.

## Architectural findings so far

- **NebulaOS is not a Klipper fork.** Host Klipper is pristine upstream `Klipper3d/klipper`
  pinned at `58bd67d` and owned by the firmware build. Custom behaviour lives in
  `NebulaOS-klipper-extensions` as loadable `extras/` modules. Documentation must never
  present upstream Klipper behaviour as NebulaOS behaviour.
- **One install path is documented but untested, and the caveat must survive.** The existing
  install page says the Creality-touchscreen route (from stock firmware) has not been tested
  - and that is the route most first-time users take. Carry that caveat into the manual with
  full prominence. Deleting it while relocating the page would be the most harmful single
  edit available in this migration: a promise of a tested procedure on the one operation that
  can brick a mainboard. Recorded as `BLOCKERS.md` B-003.
- **Five overlay executables have ordinary system names and are not what they look like.**
  `sudo` is an adapter that is not sudo, `supervisorctl` is a deliberate fake so Moonraker
  believes a supervisor exists, `passwd` redirects because the image `/etc/shadow` is
  read-only, `sftp-server` relocates SFTP to `/opt/printer_data`, and `git` is a wrapper
  first on Moonraker's PATH. Any of these would mislead a developer who assumed standard
  behaviour. They were nearly filtered out of discovery as vendor noise.
- **The extensions pin gap is cosmetic.** The firmware manifest pins the extensions to
  branch `production` at `31d6d65`; `main` is at `8e3447a`. The diff is three files - a CI
  workflow, a CI script and a README edit - with nothing under `extras/`. Runtime code is
  identical, so every documented extension behaviour is shipped behaviour and pages get a
  footnote with the pin SHA rather than a development-only label. Do not re-derive this from
  the SHAs alone: a pin gap is a question, and the answer is in the diff.
- **The UI surface is large and well-structured.** 49 panels in `src/*_panel.cpp`, which is
  both the screen reference and the screenshot plan.
- **NebulaOS has a deliberate public API.** 56 Moonraker endpoints under
  `machine.nebulaos.*`, served by `scripts/build/overlay/usr/lib/nebulaos/moonraker/
  nebulaos.py` in Moonraker's own process - no second daemon. The full chain is
  panel -> JSON-RPC -> that component -> the `nebulaos-osconfig` CLI (argv in, one JSON
  object out, validated and atomic) -> 17 `nebulaos_osconfig` modules. The component is
  symlinked into Moonraker by `S05nebulaos-activate` and configured by `[nebulaos]` in
  `/etc/nebulaos/moonraker/nebulaos.conf`; without that file Moonraker runs without it,
  which is precisely the difference between a printer that shows OS settings and one that
  does not.
- **Inventory the API from the server, not from the UI.** Two endpoints
  (`ota.discard`, `system.notify_refused`) are served but never called by the shipped UI.
  Discovering from call sites would have missed both.
- **Boot and lifecycle are script-driven.** 35 ordered init scripts in the firmware overlay,
  covering revert safety, Wi-Fi, MCU guard, update supervision, image trial and
  confirm-good. These are the real source for the update, rollback and recovery pages.
- **The extensions test suite passes, and has been run.** 29 of 31 suites, 899 individual
  tests, at `8e3447a`. 21 modules are now test-verified with per-file citations. Two traps
  when re-running it: strip ANSI before matching `OK` (the coloured line defeats
  `grep '^OK'` and makes every suite look broken), and run per-module rather than via
  `unittest discover` (discovery reports 42 bogus errors). Both are written up in
  `VERIFICATION.md`.
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

## Worktrees and build areas

- `_worktrees/docs/NebulaOS` - the manual and agent state, branch `docs/agent`.
- `_worktrees/docs/NebulaOS-firmware` - pinned at `c377230`, branch `docs/firmware`. **Read
  evidence from here, not from the workspace-root checkout** - the foreground session moves
  that one under you (it was already one commit ahead when checked).
- `_worktrees/docs/NebulaOS-klipper-extensions` - **`a2e7634`**, branch `docs/extensions`,
  used for the test suite.
- `_worktrees/docs/NebulaOS-nebulascreen` - `3194104`, branch `docs/screen`.
- `_worktrees/docs/screen-sim` - a **separate clone** with submodules, for building the
  simulator. Not a worktree, deliberately: submodule init needs to write the parent repo's
  `.git/config`, which lives in the foreground checkout and is write-protected.

One mistake to avoid: `git worktree add` resolves a *relative* path against the `-C`
directory, not the shell's cwd. That briefly created a worktree **inside** the foreground
checkout on 2026-11-01. It was removed and the checkout verified clean, but use absolute
paths.

## Branches and pull requests

- `docs/extensions` in `NebulaOS-klipper-extensions` - worktree at
  `_worktrees/docs/NebulaOS-klipper-extensions`, used for running the test suite. No
  commits, nothing to push. Note that `git worktree add` could not write the parent repo's
  `.git/config` (sandbox), which is harmless - the worktree itself works.
- `docs/agent` in `NebulaOS` - the agent's state and the user manual. Pushed.
- **PR #3** - https://github.com/NebulaOS-KE/NebulaOS/pull/3 - the first batch: manual
  skeleton, install, recovery, safety, and the coverage dashboard. Open, awaiting review.
  Later batches continue on the same branch and update this PR; do not open a second PR for
  the manual unless the owner asks for one.

## Next actions, in order

1. `git fetch` every repository and compare tips against the table above. If a tip moved,
   mark the affected items for re-verification instead of assuming the pages still hold.
2. **Q-017:** replace stubs with real pages, highest-traffic first - `First-Time-Setup`,
   `Connecting-To-WiFi`, `Opening-Mainsail`, then `Resetting` and `Updating-NebulaOS`. The
   existing NebulaScreen wiki already covers the last two well; reconcile rather than rewrite.
3. **Q-020, continued:** fetch the four submodules into
   `_worktrees/docs/NebulaOS-nebulascreen`, build with `GUPPY_SMALL_SCREEN=1`, and try to
   drive one panel and capture one image. Record the answer in `SCREENSHOTS.md` either way.
4. **Q-052:** run the two Klipper-dependent test suites the way `scripts/ci-tests.sh` does,
   by composing `extras/` into a scratch copy of the pinned Klipper at `58bd67d`.
5. Keep running `tools/check_links.py` before every commit that touches `wiki/`.
5. Follow-ups, when their sections come up and not before: Klipper status objects (find the
   `printer.objects.subscribe` call sites; the ~85 rejected pointers are candidates, but tie
   each to a real subscription first), and cloning `nebulaos-packages` and `lv_drivers`.

Each batch ends the same way: update `coverage.jsonl`, regenerate `COVERAGE.md`, update
`STATUS.md` and `QUEUE.md`, commit, push, update this file.

## A habit this work has earned

Two of the first three discovery slices shipped a bug that mis-sized the inventory: a sweep
that over-collected 85 non-existent configuration options, and a regex that silently dropped
an API endpoint whose path contains a digit. Neither announced itself - a wrong inventory
looks exactly like a right one.

So every extractor gets a second, independent count before its output is trusted. Compare
against a different signal: total path literals in the file, a hand count on one module, the
other side of the same interface. It has caught something every time.

## Tim's decisions you must not re-litigate

- **D-009:** the Creality-touchscreen install route is documented as the normal route, with no
  "untested" warning on user pages. The verification record lives in `VERIFICATION.md` and the
  inventory only. This reversed an earlier position of this agent's; it is Tim's call. Do not
  reinstate the warning.
- **D-010:** free rein to rename, merge and restructure the wiki, via PRs.

Note what D-009 did *not* license: no page claims the route is tested, and `verify_hardware`
stays unverified in the inventory. Removing a warning is not the same as asserting a
verification.

## A process rule, learned the hard way

Never chain `render_dashboard.py && <state updates>` in one shell command. A path mistake in
the render short-circuited the `&&` on 2026-10-31, the state updates silently did not run,
and the commit that followed described a blocker it had not actually written. The dashboard
was left reporting 510 items while the inventory held 544 - the exact stale-dashboard failure
the mission warns about.

Run the updates, then render, then **verify the files say what the commit message claims**
before committing. A commit message is a claim like any other.

## The screen reference, and a rule it established

`wiki/Screen-Reference.md` was adapted from the component wiki, not rewritten, and carries a
generated 49-panel index so no panel can drop off the list.

**The rule: never point a caption at a screenshot of a different screen.** Eight image
references were removed rather than remapped to plausible-looking candidates -
`m10b-bedmesh-saved` is the mesh *after saving* and not the 3D view, `36-spoolman` is the
Spoolman *server settings* and not the spool list, `m13-tmc-metrics` is TMC *status* and not
autotune. Using them would have made the page look finished. A caption naming a screen the
reader is not looking at is worse than no picture at all: the reader trusts it, then cannot
find the control, and stops trusting the rest.

## How to write a page here

Read `REUSE-AUDIT.md` first - 15 of the existing wiki pages move largely as they stand, so
check whether the work is already done before authoring.

Every procedure page follows the mission's shape: what the guide is for, what you need, what
to check first, numbered steps, expected result, troubleshooting, and how to undo it.

Three habits that the first batch proved out:

- **Verify the numbers, do not copy them.** The old wiki's "about 5 minutes" and "three
  times" were correct, but that was established by reading `TRIAL_SECONDS` and
  `TRIAL_ATTEMPTS` in source. Two accurate documents agreeing with each other is not
  evidence.
- **Give caveats their own heading.** The untested install route got a *How much of this is
  tested* section near the top of the page, not a footnote. A reader deciding whether to
  flash their printer needs that before the steps, not after.
- **Cite the commit.** Any claim about timing, defaults or behaviour names the file and the
  commit it came from, so a later reader can re-check it instead of trusting it.

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
