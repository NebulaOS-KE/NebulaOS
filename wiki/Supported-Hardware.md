# Supported hardware

## The short answer

NebulaOS supports the **Creality Ender-3 V3 KE**. That is the only printer it supports.

## Check you have the right printer

The Ender-3 V3 KE is easy to confuse with its siblings. They are different machines and
NebulaOS is **not** for them:

| Printer | Supported? |
|---|---|
| Ender-3 V3 **KE** | **Yes** |
| Ender-3 V3 | No |
| Ender-3 V3 SE | No |
| Ender-3 V3 Plus | No |
| Ender-3 S1 / S1 Pro / V2 / Neo | No |
| K1, K1C, K1 Max, K2 | No |
| Anything not a Creality Ender-3 V3 KE | No |

The model name is printed on the box and usually on a label on the machine. If your printer's
stock screen says anything other than "Ender-3 V3 KE", stop here.

**Do not try to install it on another printer.** The image is built for this machine's specific
processor, display and mainboard. It will not simply refuse politely.

## What is inside the KE

Useful to know, because it explains some things elsewhere in this manual:

| | |
|---|---|
| Processor | Ingenic X2000, a MIPS chip. Not ARM, not x86 |
| Touchscreen | 480 x 272 pixels, resistive touch |
| Mainboard | Creality's own, with a separate microcontroller driving the motors |
| Storage | Internal eMMC with **two system slots**, plus a shared data area |
| Network | 2.4 GHz Wi-Fi |

The 480 x 272 screen is small, which is why NebulaScreen's layout is dense - and why every
screenshot in this manual is that size.

**2.4 GHz only.** If your router publishes separate names for its 2.4 and 5 GHz networks, use
the 2.4 GHz one. See [Connecting to Wi-Fi](Connecting-To-WiFi).

## Two system slots

The printer has room for two complete systems, and this is the single most reassuring fact in
this manual. NebulaOS installs into the slot you are **not** using, so:

- Your existing system stays installed.
- Going back is a menu item, not a reinstall.
- A system update goes into the other slot and is undone automatically if it fails.

Your print files, configuration and calibration live in a third, shared area and survive
switching between systems.

## Accessories

- **Camera:** any USB webcam works for watching prints. Creality's **Nebula Camera** also gets
  its own settings - night mode, anti-flicker and picture controls. See [Camera](Camera).
- **USB storage:** FAT32-formatted sticks, for print files and for installing system images.
- **A screen mount:** the KE's display is not positioned for comfortable use. Community mounts
  exist on Thingiverse and Printables.

## What you need besides the printer

To install:

- A FAT32 USB stick, if you are coming from stock Creality firmware.
- A computer with SSH, if you are coming from OpenKE.

To calibrate:

- A sheet of paper.
- A ruler or caliper.
- For skew correction only, a printed test part.

## Next

- [Safety first](Safety-First)
- [Installing NebulaOS](Installing-NebulaOS)
