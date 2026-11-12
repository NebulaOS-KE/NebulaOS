# Other printers (experimental, untested)

NebulaOS is made for the **Creality Ender-3 V3 KE**. Underneath it runs **ordinary upstream
Klipper**, so on paper other Creality printers driven by a Nebula Pad could use it too, with a
mainboard firmware you build yourself. This page collects what is known about that, for people who
want to try.

> **Experimental, untested, unsupported.** We do not have these printers and have not tested any
> of them with NebulaOS. Nothing on this page is a promise that it works. If you try it, you do it
> at your own risk, and you need a way back (your printer's stock firmware and its own recovery
> method). If you get one working, please share how - see [Tell us](#tell-us-what-worked).

## Before you start: what has to be true

Four separate things all have to work. A firmware that builds and flashes is only the first:

1. **NebulaOS has to run on your Nebula Pad.** NebulaOS installs on the touchscreen computer built
   into the KE. Whether it installs and runs on a separately sold (retail) Nebula Pad is **not
   known** - nobody has tried it yet.
2. **Your mainboard needs a Klipper firmware built for it** - the rest of this page.
3. **Klipper needs a configuration for your printer.** NebulaOS's own configuration describes the
   KE: its pins, motors, bed size and load-cell probe. You have to replace that with your printer's
   (see [The printer configuration](#the-printer-configuration)).
4. **NebulaOS's own features assume a KE.** The print start, the calibration menu, Auto Calibration
   and the Z offset use the KE's load-cell probe. On another printer, expect parts of them not to
   work until they are adapted.

## Never use the KE's firmware tools on another board

- **Settings → Printer → MCU firmware** and **Reinstall NebulaOS firmware** are for the KE only.
  They check for the KE's special image format and must not be used for any other board.
- Build the firmware on a PC and flash it **the way your board is normally flashed**: almost always
  an SD card in the mainboard, or another method the board's maker supports.
- At every start NebulaOS checks which mainboard firmware is running. On another board it does not
  recognise it: normally it reports a warning and lets Klipper start. It **never** writes firmware
  to a board it does not recognise as a KE. If it ever stops Klipper with an *unsupported mainboard*
  message instead, please report it - see [Tell us](#tell-us-what-worked).

## Mainboard overview

Look at the **chip printed on the processor** of your mainboard, not only the board's label: a
board marked C14 can carry either an STM32F401 or a GD32F303.

| Printer / board | Chip on the board | Processor in `make menuconfig` | Bootloader offset | Serial to the Nebula Pad | Baud | How sure |
|---|---|---|---|---|---|---|
| Ender-3 V3 SE, C13 | GD32F303 | STM32F103 | 28 KiB | USART2 (PA3/PA2) | 230400 | Community-reproduced (with a Sonic Pad) [S5] |
| Ender-3 V3 SE, C14 | STM32F401 | STM32F401 | 64 KiB | USART2 (PA3/PA2) | 230400 | **Candidate only** - the serial setting is not confirmed [S8][S9] |
| Ender-3 V3 SE, marked C14 | GD32F303 | STM32F103 | 28 KiB | USART2 (PA3/PA2) | 230400 | **Candidate only** [S11][S12][S13] |
| Creality 4.2.2 | STM32F103 | STM32F103 | 28 KiB | USART3 (PB11/PB10) | 230400 | Upstream Klipper settings; baud from SimpleAF's Nebula Pad setup [S6][S4] |
| Creality 4.2.2 | GD32F103 | STM32F103, **Disable SWD at startup** on | 28 KiB | USART3 (PB11/PB10) | 230400 | Upstream Klipper settings [S6][S4] |
| Creality 4.2.2 | GD32F303 | STM32F103 | 28 KiB | USART3 (PB11/PB10) | 230400 | Community starting point; not every board may boot [S3][S6] |
| Creality 4.2.7 | STM32F103 | STM32F103 | 28 KiB | USART3 (PB11/PB10) | 230400 | Upstream Klipper settings; SimpleAF marks these Nebula Pad setups untested [S7][S3] |
| Creality 4.2.7 | GD32 | STM32F103 | 28 KiB | USART3 (PB11/PB10) | 230400 | **Candidate only** [S3][S7] |

None of these has been tested with NebulaOS. The Ender-3 V3 and V3 Plus are left out: they are a
different design.

**Why "serial to the Nebula Pad" matters:** most Klipper guides for these boards are written for a
Raspberry Pi on USB and use **USART1 (PA10/PA9)**. That firmware flashes fine but cannot talk to a
Nebula Pad over the display cable. You choose the serial port in `make menuconfig`, by the name in
the table - you never need to rewire anything.

For comparison, the KE itself: GD32F303, 12 KiB bootloader, USART2 at 230400, plus a Creality
header that only the KE needs. **Do not copy the KE's settings to another board**
([how the KE firmware is built](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/blob/main/docs/BUILDING_YOUR_OWN_FIRMWARE.md)).

## Build the firmware

On a Linux PC (or WSL), with Klipper's build tools installed ([Klipper's install guide](https://www.klipper3d.org/Installation.html#building-and-flashing-the-micro-controller)):

```bash
git clone https://github.com/Klipper3d/klipper.git
cd klipper
git checkout 58bd67db3ce1be1951c3e4a6d1156a79903d4edc   # the Klipper NebulaOS 1.0.2 runs
make menuconfig
make
```

The firmware is `out/klipper.bin`. Build from the **same Klipper version as the printer runs**
(the commit above is NebulaOS 1.0.2's); a firmware from a very different Klipper version may refuse
to connect. Before building for a different board, run `make clean` and check every setting again.

### Example: Ender-3 V3 SE with a C13 board (GD32F303)

The most complete known recipe, reproduced by a community member with a Sonic Pad [S5]:

```text
Enable extra low-level configuration options: on
Micro-controller architecture: STMicroelectronics STM32
Processor model: STM32F103
Disable SWD at startup: on
Bootloader offset: 28KiB bootloader
Clock reference: 8 MHz crystal
Communication interface: Serial (on USART2 PA3/PA2)
Baud rate for serial port: 230400
```

If your Klipper version offers *Optimize stepper code for 'step on both edges'*, turn it on.
Leave everything else at its default.

## Flash it

| Board | How |
|---|---|
| V3 SE C13 (GD32F303) | The `.bin` in the **root** of the SD card [S16] |
| V3 SE C14 (STM32F401) | `STM32F4_UPDATE/firmware.bin` on the SD card [S9][S10] |
| V3 SE marked C14 with a GD32F303 | Some owners succeeded with the root of the SD card, like the C13; not all [S12][S13] |
| Creality 4.2.2 / 4.2.7 | The `.bin` in the **root** of the SD card [S6][S7] |

Use a small FAT32 card, give the file a **new, short name** each time (many Creality bootloaders
skip a name they have seen before), and insert the card with the printer switched **off**.

## The printer configuration

The Nebula Pad talks to the mainboard on this serial port:

```ini
[mcu]
serial: /dev/ttyS1
baud: 230400
restart_method: command
```

NebulaOS's `printer.cfg` includes the KE's hardware files (`machine.cfg`, `prtouch.cfg`,
`z_offset_probe.cfg` from `/etc/nebulaos/klipper/`). For another printer, replace those includes
with a configuration for **your** printer. Good starting points:

- SimpleAF's Nebula Pad configs for the [V3 SE](https://github.com/pellcorp/creality/blob/main/k1/nebula/creality-ender3-v3-se.cfg),
  [4.2.2](https://github.com/pellcorp/creality/blob/main/k1/nebula/creality-ender3-v12-422.cfg) and
  [4.2.7](https://github.com/pellcorp/creality/blob/main/k1/nebula/creality-ender3-v12-427.cfg) [S4]
- [A community V3 SE Klipper config](https://github.com/0xD34D/ender3-v3-se-klipper-config) [S15]
- Upstream Klipper's [Creality 4.2.2](https://github.com/Klipper3d/klipper/blob/master/config/printer-creality-ender3pro-2020.cfg)
  and [4.2.7](https://github.com/Klipper3d/klipper/blob/master/config/generic-creality-v4.2.7.cfg) examples

These are references, not drop-in files: pins, motor directions, thermistors, endstops, the probe
and the bed size must match your printer. SimpleAF's files also use SimpleAF-only parts. On the V3
SE, the stock load-cell automatic Z offset does not work with plain Klipper [S15].

**Stepper drivers:** a different driver chip (TMC2208, TMC2209, A4988 ...) does not need a different
firmware. It is part of the printer configuration. Many Creality boards run TMC drivers without a
UART connection; then leave out any `[tmc...]` section. Never copy motor currents from another
printer [S18][S19].

## First start: check in this order

1. Klipper connects to the mainboard.
2. Temperatures read sensible room values.
3. Endstops and the probe change state when triggered (`QUERY_ENDSTOPS`, `QUERY_PROBE`).
4. Fans run.
5. Each motor moves the right way, a small step at a time.
6. Heaters heat and the safety limits are right.
7. Only then home, and only then calibrate.

## Tell us what worked

If you get a printer working, please open an issue on
[NebulaOS](https://github.com/NebulaOS-KE/NebulaOS/issues) titled *Community build: &lt;printer&gt;*,
so the next person can use it:

```text
Printer model:
Mainboard label / revision:
Chip printed on the processor:
Nebula Pad (retail or other) and NebulaOS version:
Klipper commit used for the firmware:
make menuconfig: processor / bootloader / clock / serial / baud / other options:
How you flashed it (SD folder, file name):
[mcu] serial and baud:
Stepper drivers (chip, UART or standalone):
Printer config source and what you changed:
klippy.log (remove IP addresses, user names and serial numbers):
What works (connect, temperatures, endstops, movement, probe, heating, homing, a print):
How you would get back to stock:
```

## Sources

These are other people's findings, not NebulaOS tests.

| Ref | Source | What it shows |
|---|---|---|
| S1 | [NebulaOS: building your own KE firmware](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/blob/main/docs/BUILDING_YOUR_OWN_FIRMWARE.md) | The KE's settings and why its tools are KE-only |
| S2 | [NebulaOS MCU architecture](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/blob/main/docs/ARCHITECTURE.md) | Upstream Klipper on the printer, the KE patch set |
| S3 | [SimpleAF: retail Nebula Pad guide](https://pellcorp.github.io/creality-wiki/nebula_pad/) | Printers SimpleAF runs on a retail Nebula Pad, untested ones, SD flashing |
| S4 | [SimpleAF Nebula Pad configs](https://github.com/pellcorp/creality/tree/main/k1/nebula) | `[mcu]` serial `/dev/ttyS1` at 230400, pin maps |
| S5 | [Klipper Discourse: C13 GD32F303 build](https://klipper.discourse.group/t/another-mcu-not-connecting-post/25693) | The C13 `make menuconfig` settings that worked (Sonic Pad) |
| S6 | [Klipper: Creality 4.2.2 config](https://github.com/Klipper3d/klipper/blob/master/config/printer-creality-ender3pro-2020.cfg) | 4.2.2 build settings, GD32F103 note, USART3, SD file names |
| S7 | [Klipper: Creality 4.2.7 config](https://github.com/Klipper3d/klipper/blob/master/config/generic-creality-v4.2.7.cfg) | 4.2.7 build settings, USART3, SD flashing |
| S8 | [Community V3 SE Klipper build guide](https://github.com/athem1s/athem1s.github.io/blob/main/_projects/klipper_guide.md) | C13 vs C14 targets for a USB host |
| S9 | [Creality: C14 + Nebula Pad firmware guide](https://wiki.creality.com/en/3d-printer-accessories/ender-3v3-se-c14-nebula-screen-firmware-upgrade) | Creality's own C14 procedure |
| S10 | [Nebula Pad C14 community guide](https://github.com/LukosiuPro/Ender3-v3-SE-Nebula-Pad-Wiki/blob/main/docs/setup-nebula-pad/index.md) | `STM32F4_UPDATE` SD method |
| S11 | [C14-marked board with a GD32F303](https://github.com/jobe1022/ender3-v3se-klipper-config/blob/main/mcu.cfg) | That this variant exists; a USB-host build |
| S12 | [Reddit: C14 label, GD32 chip](https://www.reddit.com/r/Ender3V3SE/comments/1w38m12/mainboard_labeled_c14_but_chip_is_physically/) | Flashing trouble and how one owner solved it |
| S13 | [Reddit: C14/GD32 with a Nebula Pad](https://www.reddit.com/r/Ender3V3SE/comments/1sskgjd/probleme_mit_nebula_pad_firmware_c13_oder_c14/) | One owner using the C13-style SD path |
| S14 | [Klipper: building the firmware](https://www.klipper3d.org/Installation.html#building-and-flashing-the-micro-controller) | `make menuconfig`, `make` |
| S15 | [Community V3 SE config](https://github.com/0xD34D/ender3-v3-se-klipper-config) | Pins and probe; the stock auto Z offset does not work in plain Klipper |
| S16 | [Creality: V3 SE firmware update](https://store.creality.com/blogs/all/ender-3-v3-se-firmware-update) | C13 SD root, new short file names |
| S18 | [TH3D: Creality 4.2.x driver codes](https://tickets.th3dstudio.com/help-guides/article/creality-v4-2-x-board-driver-codes) | Stepper driver letters on 4.2.x boards |
| S19 | [Klipper: TMC drivers](https://www.klipper3d.org/TMC_Drivers.html) | UART vs standalone drivers |
| S20 | [Reddit: C14 STM32F401 with a retail Nebula Pad](https://www.reddit.com/r/Ender3V3SE/comments/1q6eilp/official_firmware_for_ender_3_v3_se_with_c14/) | Creality's own C14 firmware working with a retail Pad |
| S21 | [Reddit: C14 flashing trouble](https://www.reddit.com/r/Ender3V3SE/comments/1tyk01c/ender_3_v3_se_c14f401_wont_flash_klipper/) | SD folder and file-name pitfalls |

*Research collected 2026-11-06. NebulaOS facts from `NebulaOS-klipper-mcu/docs/BUILDING_YOUR_OWN_FIRMWARE.md`,
`etc/nebulaos/klipper/machine.cfg` and `etc/init.d/S50nebulaos-mcu-guard` (`mcu_lifecycle.py`), firmware `3bdf3ff`.*
