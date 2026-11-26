# NebulaOS on the Ender-3 V3 SE

**Yes, you can run NebulaOS on an Ender-3 V3 SE** - on a Nebula Pad connected to the SE's
mainboard. NebulaOS is made and tested for the Ender-3 V3 KE; the SE is a **community port**,
built and used every day by SE owners, and you are very welcome to join them.

What that means for you:

- **The files are ready-made.** Every NebulaOS release contains the SE mainboard firmwares,
  built from the same Klipper as that release. You do not compile anything.
- **The community helps each other.** There is no guarantee, and we can't test every SE board
  ourselves. SE owners share what works on [Discord](https://discord.com/invite/k3HdqpdB) and in
  [issues](https://github.com/NebulaOS-KE/NebulaOS/issues) - every report makes it better for the
  next person.
- **You can go back to stock.** See [Back to stock](#back-to-stock) below.

Thank you **Hazok652**, who made the first SE setup and runs it every day, and everyone who
tested and shared fixes.

## Which SE mainboard do I have?

The SE was sold with **two different mainboard chips**, and each needs its own firmware.
Check first: switch off and unplug the printer, open the cover underneath, and look at the
mainboard. The wrong firmware won't harm the board, but it won't work either: the printer stays *not ready*. Flash the right file again, with a new name.

| Label on the board ends in | Chip | Firmware file | Status |
|---|---|---|---|
| **C13** | GD32F303 | `nebulaos-ender-3-v3-se-gd32f303.bin` | **Tested by the community**, in daily use |
| **C14** | look at the large square chip: **GD32F303** | `nebulaos-ender-3-v3-se-gd32f303.bin` | Same chip and firmware as the C13: **tested by the community** |
| **C14** | look at the large square chip: **STM32F401** | `nebulaos-ender-3-v3-se-stm32f401.bin` | **Not tried yet** - first testers welcome! |

A C14 board exists with **either** chip, so on a C14 the chip decides, not the label.

## What you need

- An Ender-3 V3 SE and a **Nebula Pad** (Creality's *Nebula Smart Kit*), connected with the
  display cable.
- A micro SD card (FAT32) for the mainboard, and a USB stick (FAT32) for the pad.
- A computer with a browser on the same network as the printer.
- About an hour.

## The steps

The full step-by-step guide, with every detail, is the
**[Ender-3 V3 SE guide](https://github.com/NebulaOS-KE/NebulaOS/tree/main/community/ender-3-v3-se)**.
In short:

1. **Find your chip** (table above).
2. **NebulaOS on the pad.** From the
   [latest release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest), copy
   `NebulaOS-NebulaPad-NEBULA_ota_img_V9.<version>.img` to a USB stick (**do not rename it**) and
   install it from the pad's touchscreen. A pad that had Creality's **KE** software takes the
   `F005` file instead. Then switch the printer off and on once.
3. **Flash the mainboard.** Download the `.bin` for your chip from the same release, give it a
   new short name (for example `fw1126.bin`), and put it on the SD card: the top level for
   GD32F303, a folder `STM32F4_UPDATE` for STM32F401. Card in, printer on, wait a minute.
4. **Printer configuration.** Upload the two SE configuration files in Mainsail and add one
   block to `printer.cfg` - the guide shows exactly what. These files are yours: NebulaOS updates
   never change them.
5. **Test step by step** with the guide's test list - connection, temperatures, endstops,
   probe, fans, heaters, motors - before you home or print.
6. **Slicer:** import the SE OrcaSlicer profile from the guide's `orcaslicer` folder.

From there, the rest of this manual applies: [First calibration](First-Calibration),
[Your first print](Printing), and so on.

## Good to know

- **Updating NebulaOS:** the mainboard firmware must match the NebulaOS on the pad. When a
  release says the community firmwares changed, flash the new `.bin` from that release (with a
  new short name). If Mainsail does not show *Ready* after an update, do this first.
- **Never use NebulaOS's own mainboard tools on the SE** (**Settings → Printer → MCU firmware**,
  *Reinstall NebulaOS firmware*). They are for the KE's board only. NebulaOS never flashes the SE
  board by itself.
- **New in November 2026:** an updated SE configuration with values from the SE's Marlin
  firmware - probe offsets, speeds, motor currents and the bed sensor
  ([#36](https://github.com/NebulaOS-KE/NebulaOS/pull/36), thanks Hazok652). Already set up?
  Compare your `Ender3V3SE/machine.cfg` with the
  [new one](https://github.com/NebulaOS-KE/NebulaOS/blob/main/community/ender-3-v3-se/config/Ender3V3SE/machine.cfg).
- **Camera and power:** the Nebula Pad takes its 5 V from the printer's mainboard, on the SE as
  on the KE. If the printer freezes with a camera connected:
  [Powering the Nebula Pad](Nebula-Pad-Power-And-Freezes).

## Back to stock

Flash `NEBULA_1.1.0.26.ingenic` with Creality's cloner (a community copy:
[openk1.org](https://www.openk1.org/cfw/NEBULA_1.1.0.26.ingenic) - not from Creality), then update
the pad with Creality's latest
[Nebula Pad firmware](https://www.crealitycloud.com/pl/downloads/box/nebula-pad). Put Creality's
SE mainboard firmware back the same way as in step 3.

## Join us

- **Discord:** [discord.com/invite/k3HdqpdB](https://discord.com/invite/k3HdqpdB) - ask, share,
  help other SE owners.
- **It works on your printer?** Tell us in a few clicks:
  [It works on my printer](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-works.yml).
  Especially if you have a **C14 with an STM32F401** - you would be the first.
- **Found a fix?** [I found a fix](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-fix.yml) -
  what was wrong and what you changed, in your own words.

Other printers of the Ender-3 V3 family: [Other printers](Other-Printers-Experimental).
