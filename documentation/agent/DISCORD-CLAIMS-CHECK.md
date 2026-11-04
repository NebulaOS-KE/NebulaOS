# Checking the Discord answers against the source

**Date:** 2026-11-04
**Asked by:** Tim, via the main session - *"Don't treat this as true, check against the code."*
**Checked against:** firmware `ba98eec` (tag `v1.0.0`) and `origin/main`, NebulaScreen
`origin/main`, extensions `f498796`. Read-only; the component worktrees stay removed.

Nine claims. **Six hold, two need correcting, one is right but for the wrong reason.** The
pages were written from the source, not from the answers.

## Holds

**1. A/B slots; the NebulaOS `.img` installs through Creality's own updater onto the unused
slot; a button flips back.** Confirmed: `docs/INSTALL_FROM_STOCK.md` uses Creality's
`local_ota_update.sh`, and `image.py` writes `other_slot(running)` and never the running slot.

**2. A Creality OTA could overwrite NebulaOS.** Same mechanism, same rule - Creality's updater
also writes the slot that is not running. True if run from the stock side.

**3a. An OS update always writes the other slot; the second one overwrites stock.** Confirmed
(`image.py`, `target_partitions`). Already documented; now explained end to end.

**3b. Klipper, Moonraker, Mainsail, extensions and NebulaScreen update independently.**
Confirmed: `[update_manager]` entries in the shipped `moonraker.conf`.

**4. Going back.** All three routes confirmed: Creality `.img` through NebulaOS's own image
install (`system_kind()` classifies an image by the kernel name inside it), NebulaOS `.img`
through the stock updater, `.ingenic` over micro-USB.

**8. Mainsail updates itself.** Confirmed. `MAINSAIL_TAG=v2.18.2` ships;
`[update_manager mainsail]` is `type: web`, channel `stable`, repo `mainsail-crew/mainsail`.

## Needs correcting

### 5. "There is a command to return to NebulaOS over SSH" - right, but not the NebulaOS one

There is a command, and it is **Creality's**, not NebulaOS's:

```sh
sh -c '. /etc/ota_bin/ota_local_method.sh; local_set_next_boot_device'
```

`/etc/ota_marker.sh` - the one NebulaOS's own `nebulaos-slot-swap` uses - **exists only on the
NebulaOS side**, so it cannot be the command you run from stock. Creality's toggles rather than
taking a target, which is what you want when coming from stock.

Also worth saying: **stock Creality does not normally give you SSH.** The route assumes OpenKE
or SSH arranged some other way. NebulaOS does not set or change stock's root password.

### 5b. "The config is migrated, and backed up before anything is written"

The backup is real - `/usr/data/nebulaos/system/migration-backups/<UTC timestamp>` - but it
covers the **application checkouts** (Klipper, the extensions, Moonraker, Mainsail,
NebulaScreen) that a newer image replaces. `S04nebulaos-migrate` calls these *image owned*.

**Your configuration is not migrated, because it is never replaced.** `printer.cfg`, macros and
calibration live on the shared data area that no slot write touches. That is the real reason
you do not recalibrate - not a migration step, and not a restore from backup. The distinction
matters: a reader told "your config is migrated and backed up" might go looking for a restore
step that does not exist.

## Right conclusion, wrong mechanism

### 9. "The Z offset from `printer.cfg` shows on the screen"

The screen shows `gcode_move.homing_origin[2]` - Klipper's **live gcode offset**, the
baby-stepping adjustment *on top of* the probe's calibrated offset. It is not the `z_offset`
from `printer.cfg` and never was.

The user who said OpenKE shows `0` was seeing correct behaviour: without NebulaOS's
`nebulaos_z_adjust`, the live offset is plain `SET_GCODE_OFFSET` and is forgotten at every
Klipper restart. **NebulaOS re-applies its saved adjustment at every Klipper start**, which is
why its screen keeps showing yours. So NebulaOS really does behave better here - for a
different reason than the one given.

## Narrowed rather than repeated

### 7. "Every Creality feature that works on stock works on NebulaOS"

Not documented as a blanket claim, because it cannot be checked as one. What was checked is the
accelerometer specifically: NebulaOS configures an **ADXL345 on the KE's stock SPI wiring** and
drives it with **upstream Klipper's `[adxl345]`/`[resonance_tester]`**, not Creality's patched
ones, with `accel_per_hz` and `max_freq` tuned down for this SoC. The guided workflow has you
mount it on the toolhead and then the bed, which is how the Creality unit is used on stock.

### 6. The statistics import - the release notes are wrong, Tim is right

The import runs when something calls `machine.nebulaos.stats`, and the only caller is the
Statistics page opening (`StatisticsPanel::shown()`). **No boot service and no installer calls
it.** So it happens the first time the page is opened, not "once at install" as the release
notes say. Documented as Tim described it.

The rest of the claim holds exactly: Creality's files are read and never written, the larger of
the two prior sources is used rather than their sum, and NebulaOS counts through Moonraker
afterwards.

## Not checkable here

Nothing in this round needed hardware. No claim above was verified **on a printer** by this
agent - all of it is read from source, which is the standing limit recorded in `BLOCKERS.md`
B-001.
