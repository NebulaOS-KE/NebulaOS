# Publish-readiness report: the end-user manual for release 1.0.0

**Date:** 2026-11-02
**Verified against:** firmware `211d804` (`NEBULAOS_VERSION=1.0.0`), NebulaScreen `dee0f6f`
(`v1.0.0`), extensions `f498796` (branch `production`), kernel `d86790d`, UI API `1`
**Branch:** `docs/agent` — PR #3 on the central `NebulaOS` repository
**Published:** no. Nothing has been published and no wiki workflow has been run.

## Summary

The manual is **ready to publish** as far as this agent can take it: 30 pages, no stubs, 128
real screenshots, every internal and external link resolving, and every page checked against
the release commit.

Four things remain that this agent cannot close. None is a reason to withhold the manual; one
is a judgement call for the owner.

## What was verified for 1.0.0

| Area | Result |
|---|---|
| Release identity | Read from the manifest at `211d804`. All five pins confirmed. |
| Extensions behaviour | `ed99372..f498796` is a **pure version bump** (one line in `nebulaos-extensions.json`), so the power-loss-recovery behaviour documented yesterday is exactly what 1.0.0 ships. |
| Screenshots | Captured from `dee0f6f`, which **is** the release screen pin. Current; no re-capture needed. |
| Trial bounds | Still `TRIAL_SECONDS = 300`, `TRIAL_ATTEMPTS = 3`. Recovery and update pages hold. |
| Root password | `nebulaos-shadow.sh` seeds the persistent copy **once**, so upgraders keep their existing password. Documented. |
| SSH prompt | `PS1='\u@\h:\w# '`. Documented, with the source's own reason: so a session says which printer it is on. |
| Links | 30 pages, 12 external links, all resolving. |

## Fixed in this pass

1. **An asset-name bug.** The install page listed the checksum as
   `NebulaOS-Ender3V3KE-<version>.sha256`; the published asset is `...-<version>.img.sha256`,
   and the page's own command four lines later used the correct name. A reader following the
   list would have hunted for a nonexistent file at the first step.
2. **The asset list** is now a table of all five 1.0.0 files, with the `.ingenic` marked as USB
   recovery only and **not** for a normal install — the two differ by one extension and one of
   them erases the data partition.
3. **Every `<version>` placeholder** is now concrete `1.0.0`, with one note on adapting for
   later releases.
4. **Both "version 0.9.0" statements** are now 1.0.0.
5. **Two links that would have 404'd at publication** — they pointed at the NebulaScreen
   GitHub wiki, which is not published. Switched to in-repo URLs that resolve today.
6. **Two unverifiable size figures removed** ("about 133 MB", "about 140 MB"). Inherited from
   the old wiki, not checkable here, and they drift every release. The text now points at the
   screen, which shows the exact size before a download starts.

## What is left, and who can close it

### 1. The stock-touchscreen install route is still unverified on hardware — owner

`BLOCKERS.md` B-003. The manual documents it as the normal route, per Tim's decision of
2026-11-01, and carries no warning. The verification record stays in `VERIFICATION.md`.

**This is the one judgement call before publishing.** It is the route most first-time users
take, and no one has confirmed it end to end. The decision to present it without a caveat was
deliberate and is Tim's; it is worth re-confirming now that it ships, because publication is
when it starts affecting strangers rather than the project's own testers.

### 2. Thirteen screenshots are missing — owner, or a later pass

Of 57 required images, 41 are captured. The gaps, each acknowledged in the page text rather
than hidden:

- **Needs a photograph of real hardware:** the first-boot screen, and the MCU firmware page.
- **Needs a live printer:** the Updates page. Its capture is timing-dependent without
  Moonraker — it would show greyed-out buttons that are not greyed out on a real printer, so
  publishing it would contradict the page.
- **Reachable in the simulator, not yet captured:** 10 panels, including Storage (which has the
  new **Free up space** button), the Spoolman spool list and the bed-mesh 3D view. These need
  the frozen screen worktree, so they wait for the freeze to lift.

None blocks publication. Every affected page says plainly that the picture is missing.

### 3. The NebulaScreen wiki should point at this manual — needs the frozen repo

The reuse audit's plan was to leave short redirect pages in the component wiki so existing
links reach the central manual. That is a change in `NebulaOS-nebulascreen`, which is frozen,
so it is queued rather than done. Until then the two wikis coexist without cross-links, which
is untidy but not wrong.

### 4. Publishing itself — owner

The central repository has no wiki publish workflow yet; the NebulaScreen one
(`.github/workflows/wiki.yml`) is the working example to copy. This agent has not created or
run one, by instruction.

## Honest notes on scope

**No page claims hardware verification.** Everything is established from source at `211d804`
and from the repositories' own tests. Where behaviour was reported by the owner rather than
observed here — the nozzle-clean routine, the install route — the inventory records
`reported-by-owner`, not `verified`.

**One correction worth remembering.** Until yesterday this manual led with a warning that
power-cycling a printer on Creality's system could break it permanently. That was false — the
MCU guard restores the native firmware automatically — and it was caught by the owner, not by
this agent. The current text says switching is safe and names the one real caution. If any
reviewer remembers the old warning, that is why it is gone.

**Coverage is 50% overall (275 of 549 items), and that is not the manual's number.** The
end-user sections are 10/10. The remaining half is developer documentation, which Tim has
confirmed is not required for this release.
