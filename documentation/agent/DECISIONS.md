# Documentation decisions

Decisions worth remembering, with the reasoning, so a later session does not relitigate
them or accidentally reverse them.

## D-001 - The end-user manual lives in the central `NebulaOS` repository

**Date:** 2026-10-31

A beginner should not have to visit a component developer wiki to load filament. The
mission makes the central repository the authoritative home of the complete end-user
experience, and that is where the manual is being written.

There is already a good end-user wiki in `NebulaOS-nebulascreen/wiki/` (34 pages, approved
and pushed on 2026-10-30). It is reused rather than rewritten: correct explanations and
examples move across, and the screen wiki keeps short pages pointing at the central manual.
No wiki history is deleted.

## D-002 - Document the newest code, and name the shipping pin

**Date:** 2026-10-31
**Revised:** 2026-10-31, after checking the diff instead of assuming

Pages describe the tip of each repository's default branch, with the exact commit recorded.
Where the firmware manifest pins an older commit of a component, the page says so.

The first version of this decision treated the `NebulaOS-klipper-extensions` gap - manifest
pins branch `production` at `31d6d65`, `main` is at `8e3447a` - as a reason to label
extension behaviour "development only". **That was wrong, and the mistake was reasoning from
the existence of a gap rather than from its contents.**

Checked directly:

```
git diff --name-status origin/production origin/main
A  .github/workflows/tests.yml
M  README.md
A  scripts/ci-tests.sh
```

Three files, 96 insertions, nothing under `extras/`. The two branches are identical in
runtime code, so **every documented extension behaviour is shipped behaviour** and none of
it should carry a development-only label. A footnote naming the pin is the right amount of
caution; a warning on every page would have been noise that quietly taught readers to
distrust correct documentation.

The general rule this leaves behind: a pin gap is a question, not an answer. Diff it before
labelling anything, every time, because the label is a claim about what users have.

## D-003 - Coverage is generated, never hand-counted

**Date:** 2026-10-31

`COVERAGE.md` is rendered from `coverage.jsonl` by a script. Nobody types a percentage.
The seeder preserves existing statuses, so re-running discovery can add items but cannot
silently mark anything done. The point of the dashboard is to make undocumented
functionality impossible to hide behind a few attractive pages.

## D-004 - Four separate verification columns

**Date:** 2026-10-31

Code, test, hardware and release-compatibility verification are reported separately. Blending
them into one number would let a pile of code-read-only pages look like a verified manual.
Since this agent has no printer, the hardware column is expected to stay empty, and saying
so plainly is more useful than hiding it.

## D-005 - Delivery is by pull request only

**Date:** 2026-10-31

Everything lands on `docs/*` branches with pull requests. No merges, no pushes to `main`,
`openke` or `production`, no wiki publish workflow runs. The project owner decides when
documentation goes live.
