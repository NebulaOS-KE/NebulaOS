# Ender-3 V3 SE on NebulaOS - community board

> **A community port.** NebulaOS is made and tested for the Ender-3 V3 KE. The SE runs it thanks to
> owners who use it every day and share what they find. That also means: no guarantee, and the
> community helps each other here. Got it working, found a fix, or stuck? Tell us - on
> [Discord](https://discord.com/invite/k3HdqpdB) or in an issue - so everyone else gets it too.

NebulaOS is made for the Creality Ender-3 V3 KE. The Ender-3 V3 SE has no touchscreen computer of
its own, so here NebulaOS runs on a **Nebula Pad** connected to the SE's mainboard. This folder has
everything for that: the printer configuration, a slicer profile and the steps. The mainboard
firmware is in every [NebulaOS release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest).

Thank you **Hazok652**, who made the first SE setup and runs it every day
([issue #8](https://github.com/NebulaOS-KE/NebulaOS/issues/8)).

## Status

| Your mainboard's chip | Status |
|---|---|
| **GD32F303** | **Community proven** - in daily use (Hazok652, C13 board) |
| **STM32F401** | **Untested with NebulaOS** - built from a recipe that works with another Nebula Pad system ([SOURCES.md](SOURCES.md)). First testers wanted! |

## What you need

- An Ender-3 V3 SE and a Nebula Pad connected to it with the display cable.
- A small micro SD card (FAT32) for the mainboard, and a USB stick (FAT32) for the pad.
- A PC with a browser on the same network as the printer (for Mainsail).
- About an hour.

## Step 1 - Find out which chip your mainboard has

The SE was sold with two different mainboard chips, and each needs its own firmware.
**Putting the wrong firmware on a board can brick it** - so check first.

- Switch the printer off and unplug it.
- Open the cover under the printer and find the mainboard.
- The board has a label ending in **C13** or **C14** (for example `CR4NS200320C14`).

| Label on the board | What to do |
|---|---|
| **C13** | Your chip is a **GD32F303** (every C13 board we know of). If you want to be sure: the large square chip says `GD32F303`. |
| **C14** | **Look at the chip** - a C14 board can have **either** chip. The large square chip says `GD32F303` **or** `STM32F401`. |

Write it down: **GD32F303** or **STM32F401**. From here on, only the chip counts, not the label.

## Step 2 - Put NebulaOS on the Nebula Pad

The pad file depends on the software the pad runs now, not on the printer.

| Your pad today | Use this file from the [latest release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest) |
|---|---|
| A Nebula Pad bought separately, with Creality's software (this is almost every SE owner) | `NebulaOS-NebulaPad-NEBULA_ota_img_V9.<version>.img` |
| A pad that already had Creality's **KE** software put on it | `NebulaOS-Ender3V3KE-F005_ota_img_V9.<version>.img` |
| A pad already running NebulaOS | Nothing to download: update from **Settings → Updates** |

1. Copy the file to the top level of a FAT32 USB stick. **Do not rename it.**
2. Plug the stick into the pad. The pad offers the update; confirm it.
3. Not offered? Then your pad has the other software - try the other `.img` file. A pad only
   opens the file made for it, so the wrong one cannot install.
4. When NebulaOS is up, switch the printer off and on once.

The `NEBULA` file exists from NebulaOS **1.0.4**. With an older release, first put Creality's
KE software on the pad: [KE firmware V1.1.0.12](https://github.com/CrealityOfficial/Ender-3_V3_KE_Klipper/releases/tag/V1.1.0.12)
with [Creality's cloner](https://github.com/CrealityOfficial/Ender-3_V3_KE_Annex/tree/main/firmware%20recovery%20tool),
then use the `F005` file.

## Step 3 - Flash the mainboard

Download the file for **your chip** from the same
[NebulaOS release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest) as your pad file:

| Chip | File | Where on the SD card |
|---|---|---|
| **GD32F303** | `nebulaos-ender-3-v3-se-gd32f303.bin` | the **top level** of the card |
| **STM32F401** | `nebulaos-ender-3-v3-se-stm32f401.bin` | a folder named **`STM32F4_UPDATE`** |

1. Rename the file to a **new, short name**: letters and numbers only, under 12 characters,
   ending in `.bin` - for example `fw1116.bin`. The board ignores a name it has seen before, so
   use a new name every time you flash.
2. Put it on the micro SD card as in the table above.
3. With the printer **off**, insert the card. Switch the printer on and wait one minute.
4. Switch off, take the card out.

Never use NebulaOS's own mainboard tools (**Settings → Printer → MCU firmware**) on the SE:
they are for the KE's board only.

## Step 4 - Upload the printer configuration

The same configuration works for both chips.

1. Open Mainsail in your browser (the printer's IP address) and go to **Machine**.
2. Create a folder **`Ender3V3SE`** next to `printer.cfg`, and upload
   `config/Ender3V3SE/machine.cfg` and `config/Ender3V3SE/overrides.cfg` into it.
3. Open `printer.cfg`. Replace the `[include ...]` lines at the top with the block from
   `config/printer.cfg.includes`. Leave everything from the `SAVE_CONFIG` block down as it is.
4. **Save & Restart.**

Your `Ender3V3SE/` files and your `printer.cfg` are yours: NebulaOS updates never change them.

## Step 5 - Test, in this order

Do the steps one by one. If a step is not OK, **stop** there - don't go on to heating or moving.
All commands go into Mainsail's console.

| # | Test | OK when |
|---|---|---|
| 1 | **Connection** | Mainsail shows Klipper **Ready**. (Not ready: wrong firmware for your chip, or the cable.) |
| 2 | **Temperatures** | Hotend and bed both show room temperature, within ±3 °C. |
| 3 | **Endstops** | `QUERY_ENDSTOPS` says `open` for X and Y. Press each switch by hand and run it again: `TRIGGERED`. |
| 4 | **Probe** | `BLTOUCH_DEBUG COMMAND=pin_down` - the pin comes out; `BLTOUCH_DEBUG COMMAND=pin_up` - it goes back in. |
| 5 | **Fans** | `M106 S128` - the part fan spins (`M107` stops it). The hotend fan starts by itself in test 6, once the hotend is above 60 °C. |
| 6 | **Heaters** | Set the bed to 40 °C: it rises within one minute. Set the hotend to 60 °C: it rises within one minute. Then set both back to 0. |
| 7 | **Motors** | Move X, Y and Z by 10 mm with Mainsail's buttons, one at a time: each moves, in the direction shown. |
| 8 | **Home** | Home all axes. |
| 9 | **Calibration** | On the screen: **Tune → Calibration → Auto Calibration → Start** ([how it goes](https://github.com/NebulaOS-KE/NebulaOS/wiki/First-Calibration)). It ends with **Done** and a Z offset. Keep the load cell on **Automatic** (the default). |
| 10 | **Print** | A small first print with the slicer profile below. |

Heaters that do not rise: Klipper's own heater check stops the printer by itself after a short
while. That is the safety net, not a failure of yours - stop and tell us.

## Step 6 - Slicer

Import `orcaslicer/Creality Ender-3 V3 SE 0.4 nozzle NebulaOS.orca_printer` in OrcaSlicer
(**File → Import → Import Configs**). See [Set up your slicer](https://github.com/NebulaOS-KE/NebulaOS/wiki/Slicer-Setup).

## Tell us how it went

- **It works?** [**It works on my printer**](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-works.yml) -
  a few clicks: your chip, which pad file, how far you got.
- **Something is wrong, or you fixed something?**
  [**I found a fix**](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-fix.yml) -
  just tell us what you changed; pasting the changed lines is enough.

Both need a free GitHub account. No logs needed.

## Good to know

- **Updating NebulaOS:** the mainboard firmware has to match the NebulaOS on the pad. When a
  release's notes say the community firmwares changed, flash the new `.bin` from that release as
  in step 3 (with a new short name). If Mainsail does not show **Ready** after an update, this
  is the first thing to do. NebulaOS never flashes the SE board itself.
- **Load cell:** keep it on **Automatic** (Tune → Calibration → Load Cell Calibration). It works on the SE; the
  water-bottle calibration is not needed. On Hazok652's printer the bed does not come back exactly
  to its zero after a load, so the bottle calibration's "back to zero" check may complain. The
  Z-offset calibration is not affected: it re-zeroes before every touch.
- **"The printer's mainboard is not answering"** at a start: NebulaOS's board check only knows the
  KE board. Since NebulaOS 1.0.3 it appears only when Klipper cannot reach the board either.
- **Back to stock:** flash `NEBULA_1.1.0.26.ingenic` with the cloner (a community copy:
  https://www.openk1.org/cfw/NEBULA_1.1.0.26.ingenic - not from Creality), then update the pad
  with Creality's latest [Nebula Pad firmware](https://www.crealitycloud.com/pl/downloads/box/nebula-pad).
  Put Creality's SE mainboard firmware back the same way as in step 3.

## For tinkerers

Every NebulaOS release builds the firmwares from the recipes in
[NebulaOS-klipper-mcu](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/tree/main/community),
with exactly the official Klipper that release runs (`58bd67d` today). The release's
`nebulaos-ender-3-v3-se-community-build-details.zip` (named `NebulaOS-community-firmware-details.zip`
up to 1.0.4) has, per chip, `recipe.defconfig` (the settings),
`klipper.config` (the full Klipper configuration), `build-info.txt` (Klipper commit, compiler) and
`SHA256SUMS`. To build one yourself:

```bash
git clone https://github.com/Klipper3d/klipper.git && cd klipper
git checkout 58bd67db3ce1be1951c3e4a6d1156a79903d4edc
grep -v '^#' /path/to/<chip>/recipe.defconfig > .config
make olddefconfig && make          # -> out/klipper.bin
```

| | GD32F303 | STM32F401 |
|---|---|---|
| Processor in `make menuconfig` | STM32F103, *Disable SWD at startup* on | STM32F401 |
| Bootloader offset | 28 KiB | 64 KiB |
| Clock | 8 MHz crystal | 8 MHz crystal |
| Communication | Serial on USART2 (PA3/PA2) | Serial on USART2 (PA3/PA2) |
| Baud | 230400 | 230400 |

A build with another compiler is not byte-identical, but has the same settings and commands.
Where every setting and pin comes from: [SOURCES.md](SOURCES.md).
