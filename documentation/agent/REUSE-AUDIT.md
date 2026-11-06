# Audit of the existing documentation (Q-006)

Audited 2026-10-31 against `NebulaOS-nebulascreen` at `94869f7`. All 34 pages in
`NebulaOS-nebulascreen/wiki/` have a disposition; the machine-readable form is in
`coverage.jsonl` under the `existing:` identifiers.

## The headline: this wiki is good, and it is being reused

The existing wiki was approved and pushed on 2026-10-30, and it reads like it was written by
someone who had actually performed the procedures. Concrete evidence of that, from
`Installing-NebulaOS.md` alone:

- It names the exact failure string a renamed image produces
  (`failed to get .../ota_config.in`) and warns not to rename the file, because Creality's
  updater finds the parts inside by file name.
- It names a harmless error that would otherwise frighten a user -
  `sh: 1.1.0.15: bad number` - and says plainly that it stops nothing.
- It warns to reboot with `reboot` rather than a power cycle, because **a stock system that
  starts from power-on can flash old firmware into the mainboard**. That is a genuine
  bricking risk that no amount of code reading would have produced.

None of that gets rewritten. The mission's instruction to reuse before replacing is the
right call here, and the job is mostly relocation plus filling gaps.

## Dispositions

| Disposition | Pages | Meaning |
|---|---|---|
| `move` | 15 | End-user material that belongs in the central manual, largely as it stands |
| `adapt` | 1 | End-user material needing rework before it moves |
| `keep` | 16 | Developer material that stays in the component wiki |
| `historical` | 2 | Describes something NebulaOS does not have; a signpost, not manual content |

### Moving to the central manual

| Page | Manual section |
|---|---|
| `Installing-NebulaOS.md` | 02 - installation |
| `Updating-NebulaOS.md`, `Resetting.md` | 08 - updates and maintenance |
| `Recovery.md` | 10 - recovery |
| `Troubleshooting.md` | 09 - troubleshooting |
| `Calibration-Guide.md`, `Calibration-Explained.md`, `Bed-Tramming.md`, `Load-Cell-Calibration.md`, `Axis-Twist-Compensation.md`, `Skew-Correction.md` | 05 - calibration |
| `TMC-Autotune.md`, `Adaptive-Print-Setup.md`, `Camera-Image-Tuning.md`, `Buzzer-and-Sounds.md` | 07 - advanced features |

### Adapting

`Using-NebulaScreen.md` is 763 lines and the single largest page in the wiki. It is a
screen reference, which is exactly what manual section 04 needs - but the inventory lists
**49 panels**, and one page cannot give each of them the task-oriented treatment the mission
requires. The plan is to keep it as the consolidated reference and build the per-workflow
task pages around it, rather than split it up and lose a document that works.

### Staying put

Sixteen developer pages: architecture, building from source, the simulator, configuration,
config and theme, releases and deployment, testing, CI, contributing, vendored dependencies,
integration with NebulaOS, wiki publishing, history and credits, the component navigation
(`Home.md`, `_Sidebar.md`) and `Installation.md`.

## Two problems found

### 1. `Installation.md` and `Installing-NebulaOS.md` are a trap

Two pages, nearly identical names, completely different audiences. `Installing-NebulaOS.md`
is the end-user guide to flashing the printer. `Installation.md` is a developer page about
where the NebulaScreen app's files live on disk, which paths are bind-mounted, and how the
app is updated independently of the image.

A user hunting for install instructions has a coin-flip chance of landing on the wrong one,
and the wrong one is a table of read-only filesystem paths. The sidebar partly mitigates this
by listing `Installation.md` under *Developers → Screen app install and files*, but the page
title does not.

**Resolution:** the end-user page moves to the central manual. `Installation.md` stays, and
should be retitled to say what it is - component files and paths - rather than
"Installation". That is a change inside the component wiki, so it goes in the same pull
request as the migration and is for the owner to accept or decline.

### 2. One install path is documented but untested, and says so

`Installing-NebulaOS.md` states: *"Tested from OpenKE on 2026-10-29. The path through
Creality's touchscreen is not tested yet."*

So section **2b**, installing from stock Creality firmware via the printer's own touchscreen,
is unverified - and it is the path most first-time users will take, since most arrive from
stock firmware rather than from OpenKE.

That caveat is preserved exactly, and carried into the central manual with the same
prominence. It is tempting to drop a line like that when relocating a page, because it makes
the documentation look weaker. Dropping it would be the single most harmful edit available in
this entire migration: it would promise a tested procedure for the most common installation
route, on the one operation where being wrong can brick a mainboard.

The corresponding inventory items keep `verify_hardware` unset rather than claiming anything,
and this agent cannot clear it - no printer access. It is recorded in `BLOCKERS.md` as
hardware verification that only the owner can supply.

## What this changes about Phase 2

Less authoring than expected, and a different shape of work:

1. The central manual's **navigation and skeleton** are genuinely new and must be written.
2. Sections 02, 05, 07, 08, 09 and 10 start from strong existing pages - relocate, reconcile
   cross-links, fill gaps.
3. Sections **01** (start here, supported hardware, safety, terminology) and **03**
   (first-time setup end to end) have no existing equivalent and are written from scratch.
4. Section **04** needs the 49-panel reference completing around the page that exists.
5. Section **06** (everyday printing) is only partly covered by the existing material and
   needs most of its procedures written.

## Re-verified against current source, 2026-11-03

The Q-006 audit gave each of the 34 existing NebulaScreen wiki pages a disposition. Eighteen of
those were *keep* or *historical* and had never been re-checked against the code since. They
have been now - the instruction was explicitly not to rubber-stamp them.

What was checked on each page, mechanically:

- every internal wiki link resolves to a page that exists
- every `` `make <target>` `` named exists in the Makefile
- every repository path named in backticks exists at the current commit
- no reference to a retired repository

**Result: no problems.** All eighteen hold at NebulaScreen `36490ed`.

Two findings about the *check* rather than the pages, worth recording because both would have
produced a false alarm:

- **`NebulaOS-klipper` matched `NebulaOS-klipper-extensions`.** A word-boundary pattern for the
  retired fork's name matches the live repository's name, because the live one is the retired
  one plus a suffix. Every hit was correct text.
- **`coreflake1/guppyscreen` is not a retired URL.** It is OpenKE, a separate upstream project
  that still exists and is credited correctly. The retired URL was
  `coreflake1/NebulaOS-guppyscreen`, a different path.

The two *historical* dispositions were checked against the thing they claim is absent, not just
read: `Emergency-Factory-Reset.md` describes a service and a USB trigger that NebulaOS does not
have, and neither `S58factoryreset` nor `emergency_factory_reset` appears anywhere in the
repository. `Upgrading.md` is a redirect stub and the anchor it points at exists.
