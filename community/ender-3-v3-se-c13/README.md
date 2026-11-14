# Ender-3 V3 SE (C13 mainboard) on NebulaOS - community build

**Experimental, community-made, not tested by NebulaOS.** NebulaOS is made for the
Creality Ender-3 V3 KE. This setup was made and is used by **Hazok652**
([NebulaOS issue #8](https://github.com/NebulaOS-KE/NebulaOS/issues/8)) on a stock
Ender-3 V3 SE with a C13 mainboard (GD32F303) and a retail Nebula Pad. Thank you!
Use it at your own risk, and keep a way back to stock (below).

## What is here

| File | What it is |
|---|---|
| `config/Ender3V3SE/machine.cfg` | The SE's own hardware configuration (travel, motors, currents, probe offset, hotend limit 250 °C, bed mesh area). Replaces NebulaOS's KE `machine.cfg`. |
| `config/Ender3V3SE/overrides.cfg` | The few values that differ from NebulaOS's KE files: purge line, homing point, bed screw positions, probe offset. Everything else keeps coming from NebulaOS, including its later fixes. |
| `config/printer.cfg.includes` | The include block for your `printer.cfg`. |
| `mcu/ender3v3se-c13-klipper-58bd67d.bin` | Klipper firmware for the C13 mainboard, built by NebulaOS from upstream Klipper `58bd67d` (the Klipper NebulaOS runs) with the settings in `mcu/klipper.config`. |
| `orcaslicer/Creality Ender-3 V3 SE 0.4 nozzle NebulaOS.orca_printer` | OrcaSlicer printer profile (with `START_PRINT` / `END_PRINT`) plus two filament and one process profile. |

`sha256` of the firmware:
`82bb409ef12ab699351f6e383cd862c7992219b5915eeb6ecb29925b9e4ff7f7  ender3v3se-c13-klipper-58bd67d.bin`

## Steps

1. **Retail Nebula Pad only - put Creality's KE firmware on it first.** Installing
   NebulaOS's `.ingenic` directly on a retail pad currently stops at the boot screen (we
   are looking into it). Flash Creality's Ender-3 V3 KE firmware with Creality's cloner
   tool over the pad's micro-USB port (behind the back cover):
   - KE firmware `V1.1.0.12`: https://github.com/CrealityOfficial/Ender-3_V3_KE_Klipper/releases/tag/V1.1.0.12
   - Cloner: https://github.com/CrealityOfficial/Ender-3_V3_KE_Annex/tree/main/firmware%20recovery%20tool
2. **Install NebulaOS** from there, as on a KE:
   [Installing NebulaOS](https://github.com/NebulaOS-KE/NebulaOS/wiki/Installing-NebulaOS).
3. **Flash the mainboard** with the `.bin` from `mcu/`: copy it to the **root** of a small
   FAT32 SD card and **give it a new, short name** each time (letters and numbers only,
   under 12 characters, e.g. `fw1114.bin`) - the SE's bootloader skips a file name it has
   seen before. Insert the card with the printer switched off, switch it on, wait a
   minute. Never use NebulaOS's own mainboard tools (Settings → Printer → MCU firmware) on
   the SE: they are for the KE's board only.
4. **Configuration:** in Mainsail (Machine), create the folder `Ender3V3SE` next to
   `printer.cfg` and upload `machine.cfg` and `overrides.cfg` into it. In `printer.cfg`,
   replace the include lines at the top with the block from `config/printer.cfg.includes`
   (leave everything from the `SAVE_CONFIG` block down as it is). Save & Restart.
5. **First start:** check in the order on
   [Other printers (experimental)](https://github.com/NebulaOS-KE/NebulaOS/wiki/Other-Printers-Experimental#first-start-check-in-this-order):
   connection, temperatures, endstops and probe, fans, each motor, heaters - only then home
   and calibrate.
6. **Slicer:** import the `.orca_printer` file in OrcaSlicer (File → Import → Import
   Configs). See [Set up your slicer](https://github.com/NebulaOS-KE/NebulaOS/wiki/Slicer-Setup).

Your files in `Ender3V3SE/` and your `printer.cfg` are yours: NebulaOS updates do not
change them.

## Good to know

- **Load cell: keep it on Automatic** (NebulaOS's default, Calibration → Load Cell). It
  works on the SE; the water-bottle calibration is not needed. The SE's load cell sits
  under the bed like the KE's, but on Hazok652's printer the bed does not come back exactly
  to its zero after a load (30-120 g), so the bottle calibration's "back to zero" check may
  complain. The Z-offset calibration is not affected either way: it re-zeroes before every
  touch (two runs gave 1.701 and 1.694 mm).
- **"The printer's mainboard is not answering"** at every start: NebulaOS's board check only
  knows the KE board. From NebulaOS 1.0.3 this message appears only when Klipper cannot
  reach the board either.
- **Back to stock:** flash `NEBULA_1.1.0.26.ingenic` with the cloner (a community copy:
  https://www.openk1.org/cfw/NEBULA_1.1.0.26.ingenic - not from Creality), then update the
  pad with Creality's latest Nebula Pad firmware:
  https://www.crealitycloud.com/pl/downloads/box/nebula-pad. Put Creality's SE mainboard
  firmware back on the board the same way as in step 3.

## Rebuilding the firmware yourself

```bash
git clone https://github.com/Klipper3d/klipper.git && cd klipper
git checkout 58bd67db3ce1be1951c3e4a6d1156a79903d4edc
cp /path/to/mcu/klipper.config .config
make olddefconfig && make          # -> out/klipper.bin
```

Settings (`make menuconfig`): extra low-level options on, STM32, STM32F103, disable SWD at
startup on, 28 KiB bootloader, 8 MHz crystal, serial on USART2 (PA3/PA2), 230400 baud.
A build with another compiler is not byte-identical, but has the same settings and
commands.
