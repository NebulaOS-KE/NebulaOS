# For Tim: what is ready to merge, and what is still open

Written 2026-11-11, after the 1.0.2 refresh (inbox note `2026-11-10-RELEASE-1.0.2-REFRESH.md`),
and extended the same day with the two older PRs (inbox note `2026-11-11-OLDER-PRS.md`).
Nothing here has been merged or published - that is yours.

## The eight pull requests

| PR | Branch | State | Read this before merging |
|---|---|---|---|
| [NebulaOS #3](https://github.com/NebulaOS-KE/NebulaOS/pull/3) | `docs/agent` | **Ready** | Contains the wiki as files plus this agent's state. You already publish the wiki yourself, so merging this is about keeping the source of the pages and the inventory in the repository. |
| [firmware #5](https://github.com/NebulaOS-KE/NebulaOS-firmware/pull/5) | `docs/firmware` | **Ready** | Describes `b95b156`, and says where 1.0.2 differs: after a freeze a 1.0.2 printer reports `PSTORE_DUMP=no` while `REASON=FREEZE` is already right. |
| [extensions #3](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions/pull/3) | `docs/extensions` | **Ready** | At `178a0c2` - the 1.0.2 pin and the tip of `main` and `production` at once, so there is no pin gap to explain. |
| [kernel #2](https://github.com/NebulaOS-KE/NebulaOS-kernel/pull/2) | `docs/kernel` | **Ready** | At `95d0321e`, which is the 1.0.2 pin. Documents the freeze-diagnosis layer and `CONFIG_PREEMPT`; claims no mitigation is proven. |
| [nebulascreen #6](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/pull/6) | `docs/screen` | **Ready** | Describes the pin `fd47cb6`; the gap to `main` (two wiki commits, one comment-only pass) was read from the diff, not assumed. |
| [klipper-mcu #1](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/pull/1) | `docs/mcu` | **Ready, but it changes a claim you may want to read first** | The README's *"no firmware built here has been flashed to a real printer"* is no longer true, so it now reads as *no qualification claim* instead of *never run*. `compatibility.json` is untouched: `hardware_qualified` stays `false`, because that is your call. |

Both older PRs now have the same treatment (2026-11-11). Neither repository needed a rebase:
each docs branch is one commit sitting directly on the current tip of its default branch
(`nebulaos-packages/main` `9d0d264`, `lv_drivers/master` `ea2e4cc`), and neither default branch
has moved since the pages were written.

| PR | Branch | State | Read this before merging |
|---|---|---|---|
| [packages #2](https://github.com/NebulaOS-KE/nebulaos-packages/pull/2) | `docs/packages` | **Ready** | Re-verified at `9d0d264`; `tests/run-tests.sh` re-run 2026-11-11, 10 passed, 0 failed. New: the image side of the contract from firmware `3bdf3ff` - runtime-only dependency, and `06-verify.sh` refusing an image whose `pip.conf` carries an `extra-index-url`, which is the hard version of "the printer never talks to PyPI". |
| [lv_drivers #1](https://github.com/NebulaOS-KE/lv_drivers/pull/1) | `docs/lv-drivers` | **Ready** | The fork did not move (`master` `ea2e4cc`, `guppyscreen-ke-next` `0406ccb`). The page named NebulaScreen `36490ed` - the 1.0.0 screen - and now names `fd47cb6` (1.0.2) and `84db432` (tip of `main`), which pin the same submodule commit. |

One correction worth knowing from the lv_drivers page: NebulaScreen does not register the fork's
`evdev_read` directly any more, it registers `evdev_read_smoothed` around it. The fork still
decides every press and release; only the coordinates are filtered afterwards.

## Three things that want a decision from you

1. **`creality_flash.py` exists twice and the shipped copy is not the repository's.**
   `NebulaOS-klipper-mcu/tools/creality_flash.py` still hashes to the value recorded in the
   firmware's `provenance.json`; the copy the image deploys to `/opt/nebulaos/tools/` has since
   gained two fixes that only hardware found - pyserial 3.5 DTR/RTS handling (ke-dev could not
   open the port at all, 2026-10-03) and closing the transport before the post-flash identify
   (every successful restore reported as failed, 2026-11-05). The mcu README now says so. Fixing
   it is a code change and not mine to make.
2. **Eleven screenshots print a version inside the picture that 1.0.2 no longer matches.** The
   list, with what each one says today, is at the end of `SCREENSHOTS.md`. `r-system.png` first:
   it shows `NebulaOS v1.0.0`, `NebulaScreen v1.0.0` **and** `Kernel 6.6.157-rt79`, while the
   1.0.2 kernel pin contains the commit that removed `localversion-rt` - so a 1.0.2 printer does
   not print `-rt79` at all. These need a printer; you or the main session take them.
3. **Do the GuppyScreen-inherited NebulaScreen settings belong in the inventory?** The
   configuration page documents about 25; the inventory tracks 20. Until that is settled, no
   document quotes a settings count. (`QUEUE.md`, Q-083.)

## What is still open, and why it stays open

- **Eight API endpoints have no documented response**, because their keys cannot be resolved
  from source and they are POST actions the printer snapshot does not contain. Each page says
  so rather than carrying a plausible example. The ninth closed this week from a recorded
  response - that is the pattern for the rest, if you ever capture them.
- **Three blockers, one fact: no printer here.** The stock-touchscreen install route is still
  unverified (documented as the normal route by your decision D-009/D-011), and two screens
  cannot be captured honestly by a headless tour.
- **Fifteen screenshots missing**, mostly panels the tour does not reach; each affected page
  says what is missing instead of borrowing a near-enough picture.

## The one number worth knowing

560 inventory items: 552 documented, 8 draft, **0 missing**, 560 code-verified, 47 test-verified,
**0 hardware-verified**. The last two are separate on purpose. Nothing in this documentation has
been observed on a printer by this session, and no page implies otherwise.
