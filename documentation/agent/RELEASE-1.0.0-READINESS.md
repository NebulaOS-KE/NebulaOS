# Publish-readiness report: the end-user manual for release 1.0.0

**Date:** 2026-11-02 (second pass — supersedes the first pass of the same day)
**Verified against:** firmware `ba98eec` (`NEBULAOS_VERSION=1.0.0`, tag `v1.0.0`),
NebulaScreen `36490ed` (`NEBULASCREEN_VERSION=v1.0.0`), extensions `f498796` (branch
`production`), host Klipper `58bd67d`, kernel `d86790d`
**Branch:** `docs/agent` — PR #3 on the central `NebulaOS` repository
**Published:** no. Nothing has been published and no wiki workflow has been run.


> **Updated 2026-11-04 after 1.0.0 was rebuilt and republished.** The first published `.img`
> used a 192 MB LZMA dictionary and could not be unpacked in the printer's 248 MB, so an online
> update ran out of memory. The release was rebuilt with a 16 MB dictionary, the version name
> kept, and the `v1.0.0` tag moved from `70ad0b0` to **`ba98eec`**.
>
> Every reference in this report was re-pointed. That is safe to do rather than merely
> convenient: `scripts/build/overlay`, `manifests` and `scripts/build` are **byte-identical**
> between the two commits, so nothing this report verified changed. The difference is the
> packaging scripts and two host-only capture profiles.
## Summary

The manual is **ready to publish**: 30 pages, no stubs, 129 real screenshots, every internal
and external link resolving, and every page re-checked against the release candidate. The one
judgement call the first pass left for Tim has since been decided by him and applied.

The first pass of today verified against firmware `211d804`. The release candidate has since
moved to `ba98eec`, which changed the screen pin and added a user-visible feature. This pass
closes that gap. Everything named below was read at `ba98eec` / `36490ed` / `f498796`, not
carried over.

## What changed in this pass

### 1. Statistics — the new 1.0.0 feature, now documented

**Settings → Printer → Statistics.** A full section in `wiki/Screen-Reference.md`, linked from
`Home`, `Printing` and `Resetting`, with a real capture (`images/20a-statistics.png`).

It covers what the page shows (total print time; the NebulaOS figures — print time, prints
done/cancelled/failed, filament, longest print; the two *Before NebulaOS* sources; the four
most recent prints and their marks), and the two things about it that surprise people:

- **Print time is printing time** — Klipper's print duration, first extrusion to end, without
  heating or pauses.
- **The total is not a sum.** *Before NebulaOS* is the **larger** of Creality's counter and an
  earlier Moonraker's history, never their sum, because under OpenKE both counted the same
  prints. Documented from `combine_stats` rather than from the screen's output.

It also states where each number comes from (`nebulaos-osconfig stats baseline`, imported once
into `/usr/data/nebulaos/system/stats-baseline.json`, reading Creality's files and the old
Moonraker database read-only), what survives a cleanup, and what a clean reset does to it.

### 2. Storage / cleanup text

`Resetting` now says that **Clean up Creality files keeps the print statistics** — Creality's
lifetime counter, its print list, and the old Moonraker database — with the source named
(`cleanup.STATISTICS_KEEP`, `KEEP_IN_PRINTER_DATA`). The `Screen-Reference` Storage row says
the same and points at the Statistics section. This was the one place where the old text would
have told a reader the opposite of what 1.0.0 does.

### 3. Release references re-pointed from `211d804` to `ba98eec`

44 inventory items relabelled, the `Recovery` trial-bounds citation re-cited (the constants
were re-read at `ba98eec`: still `TRIAL_SECONDS = 300`, `TRIAL_ATTEMPTS = 3`), and this report
rewritten. No `211d804` reference remains anywhere in the branch.

### 4. Screenshots re-captured at the release screen pin

The tour was re-run against a build of `36490ed` — the exact commit `ba98eec` pins. 130
captures; **one new** (`20a-statistics`) and **four changed**:

| Image | Why it changed |
|---|---|
| `05-printer`, `15-printer` | the Printer settings page gained the **Statistics** button |
| `35-restart-klipper-refused` | that same page is the dialog's background |
| `37-spoolman-typing` | the **Use** button's pressed shade — not a code change |

`07-updates` stays excluded for the reason recorded in `SCREENSHOTS.md`. `screenshots.json`
now records `36490ed`.

### 5. Power-loss recovery: one undocumented 1.0.0 behaviour added

Checking the extensions pin showed that `a2e7634..f498796` is **not** the pure version bump
the first pass reported — that was true of `ed99372..f498796` only. The real change
(`ed99372`) added three things, two of which the page already described. The third did not
exist on any page: **a timelapse keeps the frames recorded before the power cut**, merged back
in front of the new ones when the print ends. Now documented, with the shipped configuration
that enables it named (`machine.cfg`, `timelapse_frame_path`).

The page's two source citations now name `f498796`, the commit 1.0.0 ships.

## What is left, and who can close it

### 1. The stock-touchscreen install route — closed by Tim, nothing left to decide

B-003 is closed (2026-11-02, decision D-011). The route stays the normal route and the manual
states nothing about what was or was not tested, anywhere. Three other places that did — two
`Recovery` notes and three "not observed on a printer" footnotes — were removed in this pass
for the same reason, and `Updating-NebulaOS`'s "the tested versions" became the factual claim
it was reaching for.

What was deliberately **not** removed: the consequences. The full USB rewrite still says it
erases settings, print files and calibration. The record of what has actually been observed on
a printer now lives only in `VERIFICATION.md` and `coverage.jsonl`.

There is no judgement call left outstanding before publication.

### 2. There is no Timelapse page — a real gap, not a blocker

Timelapse ships (the manifest pins `moonraker-timelapse`, `S57nebulaos-timelapse-seed` seeds
it, `camera.cfg` and `print.cfg` drive it) and the mission lists it as a manual section, but
the word appears on only two pages in the whole manual. The power-loss side is now covered;
a proper page is queued as Q-064 and is the next batch.

If the release can wait an iteration, this is worth having. If it cannot, the manual is not
wrong without it — it is incomplete, and no page promises the section.

### 3. Fifteen screenshots are missing — owner, or a later pass

Of 58 required images, 42 are captured. Unchanged in kind from the first pass: two need a
photograph of real hardware (first boot, MCU firmware page), one needs a live printer
(Updates), and the rest are reachable in the simulator but not on the capture tour — Storage
among them, which is why the **Free up space** and **Clean up Creality files** buttons are
described in words. Every affected page says plainly that the picture is missing.

### 4. The NebulaScreen wiki should point at this manual — needs the frozen repo

Unchanged. It is a change in `NebulaOS-nebulascreen`, which is frozen for the release.

### 5. Publishing itself — owner

The central repository has no wiki publish workflow. This agent has not created or run one,
by instruction.

## Honest notes on scope

**No page claims hardware verification.** Everything here is established from source at
`ba98eec` / `36490ed` / `f498796` and from the repositories' own tests. Where behaviour was
reported by the owner rather than observed here — the nozzle-clean routine, the install route,
the Statistics page on `ke-dev` — the inventory records `reported-by-owner`, not `verified`.

**The screenshots are the real application, not a real printer.** The Statistics capture shows
the simulator's example figures, and the page says so under the image. The alternative — a
screenshot implying a particular printer's history — would be worse.

**Firmware `main` has already moved past the release candidate** to `78da217`, which touches
only `tools/hardware/` (a read-only capture profile). Nothing in the manual is affected.

**The extensions developer reference is behind the release.** 189 inventory items are labelled
at `a2e7634` while 1.0.0 ships `f498796`, and those two differ in runtime code. That is
developer documentation, which Tim has confirmed is not required for this release; it is
queued as Q-065 and cannot start until the component worktrees come back.

**Coverage is 50% overall (276 of 550 items), and that is not the manual's number.** The
end-user sections are 10/10. The remaining half is developer documentation.
