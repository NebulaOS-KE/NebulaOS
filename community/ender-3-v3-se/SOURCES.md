# Ender-3 V3 SE - where every setting comes from

These are other people's findings and our own checks, collected 2026-11-16. "Proven" means
running NebulaOS; everything else is a published recipe that works elsewhere.

## Mainboard firmware

| Chip | Setting | Evidence |
|---|---|---|
| GD32F303 | STM32F103, Disable SWD on, 28 KiB, 8 MHz, USART2, 230400 | **Proven on NebulaOS** (Hazok652, C13, issue #8). The CI recipe expands to exactly that build's `.config`. Same settings: SimpleAF's Nebula Pad C13 firmware (`.config.e3v3se` [S2]), a Sonic Pad C13 build [S7]. |
| STM32F401 | STM32F401, 64 KiB, 8 MHz, USART2, 230400 | SimpleAF's Nebula Pad C14 firmware (`.config.e3v3se-c14` [S2]); its maintainer, who owns a C13 and a C14, confirmed on 2026-11-13 that it "works correctly for Nebula and RPI" [S3]. Not yet run with NebulaOS. |

SimpleAF's builds come from Kalico, a Klipper fork, and also switch on two Kalico-only options
(`NEED_LOAD_CELL_PROBE`, `WANT_HX711S`). Our builds are official Klipper `58bd67d`, like the
proven GD32F303 build; NebulaOS reads the load cell without those options.

Do not confuse with a **Raspberry Pi** build: guides for a Pi on the board's USB port use
**USART1** (and often 250000 baud) - for example the C14 load-cell build in [S3]'s first comment.
That firmware flashes fine but cannot talk to a Nebula Pad over the display cable.

## The C14 label has two chips

The same board name, `CR4NS200320C14`, appears with a **GD32F303** [S5] and with an
**STM32F401** [S4]. So the chip, not the label, decides the firmware. Every C13 source names a
GD32F303.

## Printer configuration (pins) - same for both chips

`config/Ender3V3SE/machine.cfg` (proven on a GD32F303 board) and SimpleAF's single SE config,
which SimpleAF uses for both chips [S1], have the same pins for everything NebulaOS uses:

| Function | Pin | Also in |
|---|---|---|
| X / Y / Z / E step, dir | PC2 !PB9 / PB8 PB7 / PB6 !PB5 / PB4 PB3 | S1, S4 (STM32F401), S5 (GD32F303) |
| Stepper enable | !PC3 | S1, S4, S5 |
| TMC2208 UART X / Y / Z | PB12 / PB13 / PB14 | S1, S4, S5 |
| Endstops X / Y | !PA5 / !PA6 | S1, S4, S5 |
| Hotend heater / thermistor | PA1 / PC5 | S1, S4 |
| Bed heater / thermistor | **PB2** / PC4 | S1, S4 - see below |
| Part fan | PA0 | S1, S4 |
| Hotend fan | PC1 | S1 only |
| Mainboard fan | PB1 (ours: `!PB1`, proven on GD32F303) | S1 only (`PB1`, always on) |
| CR Touch control / sensor | PC13 / PC14 | S1, S4, S5 |
| Load cell HX711 SCLK / DOUT | PA4 / PC6 (NebulaOS `z_offset_probe.cfg`) | S4, SimpleAF's SE load-cell config [S6] |

### Disputed: bed heater PB2 or PA7

- **PB2:** SimpleAF's SE config, which runs on a C14 with a Nebula Pad [S1][S3], and Revoxxi's
  STM32F401 C14 pin file [S4]. **We use PB2.**
- **PA7:** only navaismo's STM32F401 pin file [S8]. That file is visibly carried over from
  another board: it gives the hotend fan the hotend heater's pin (PA1), and its pin list names
  ports (PD, PE) the 64-pin STM32F401 does not have.
- Safe check: test 6 of the README (bed to 40 °C, must rise within a minute). A wrong heater pin
  heats nothing, and Klipper's heater check then stops the printer.

### Weaker evidence

- Hotend fan PC1 and the mainboard fan's polarity come from SimpleAF's config only [S1]. A wrong
  fan pin is low risk; test 5 and 6 of the README check both.

## Flashing

| Chip | How | Evidence |
|---|---|---|
| GD32F303 | `.bin` in the root of the SD card, new short name | Creality [S9], proven |
| STM32F401 | `.bin` in `STM32F4_UPDATE/` on the SD card, new short name | SimpleAF [S10], Creality's C14 guide [S11] |

SimpleAF warns that the C14 firmware on a C13 board, or the reverse, will very likely brick it
(different bootloader offsets) [S10]. Both chips keep their SD-card bootloader, which a `.bin`
never overwrites (GD32F303 app at 0x7000, STM32F401 at 0x10000), so a wrong flash is fixed by
flashing the right file with a new name. Not tested by us yet.

## Sources

| Ref | Source |
|---|---|
| S1 | [SimpleAF: Ender-3 V3 SE Nebula Pad config](https://github.com/pellcorp/creality/blob/main/k1/nebula/creality-ender3-v3-se.cfg) |
| S2 | [SimpleAF firmware recipes: `.config.e3v3se`, `.config.e3v3se-c14`](https://github.com/pellcorp/kalico/tree/aug2026) |
| S3 | [SimpleAF issue #1702: C14 firmware confirmed with a Nebula Pad](https://github.com/pellcorp/creality/issues/1702) |
| S4 | [Revoxxi: Marlin pins for the STM32F401 C14 board (`CR4NS200320C14`)](https://github.com/Revoxxi/Marlin_2.1.2_E3V3SE_STM32F401_C14HARDWARE/blob/main/Marlin/src/pins/stm32f4/pins_CREALITY_F401.h) |
| S5 | [jobe1022: C14-labelled board with a GD32F303](https://github.com/jobe1022/ender3-v3se-klipper-config/blob/main/mcu.cfg) |
| S6 | [SimpleAF: SE load-cell config](https://github.com/pellcorp/creality/blob/main/k1/patches/loadcells_zoffset.cfg.e3v3se) |
| S7 | [Klipper Discourse: C13 GD32F303 build](https://klipper.discourse.group/t/another-mcu-not-connecting-post/25693) |
| S8 | [navaismo: Marlin pins (bed heater PA7)](https://github.com/navaismo/Marlin_bugfix_2.1_E3V3SE/blob/c14_sd/Marlin/src/pins/stm32f4/pins_CREALITY_F401.h) |
| S9 | [Creality: V3 SE firmware update](https://store.creality.com/blogs/all/ender-3-v3-se-firmware-update) |
| S10 | [SimpleAF: retail Nebula Pad guide](https://pellcorp.github.io/creality-wiki/nebula_pad/) |
| S11 | [Creality: C14 + Nebula Pad firmware guide](https://wiki.creality.com/en/3d-printer-accessories/ender-3v3-se-c14-nebula-screen-firmware-upgrade) |
