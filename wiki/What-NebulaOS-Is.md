# 1. What is NebulaOS

## In one paragraph

NebulaOS is replacement software for the **Creality Ender-3 V3 KE** 3D printer. It replaces
everything Creality installed - the operating system, the printing software and the touchscreen
app - with an open system built around Klipper. It installs next to the software you have now,
so you can go back.

## What it replaces, and with what

| What you have now | What NebulaOS uses |
|---|---|
| Creality's printing firmware | **Klipper** - open-source printer firmware, widely used, with far more tuning available |
| Creality's touchscreen app | **NebulaScreen** - NebulaOS's own touchscreen app |
| Creality's web interface | **Mainsail** - a browser interface for uploading files and controlling the printer |
| Creality's cloud | Nothing. NebulaOS talks to your printer over your own network |

Some words you will meet constantly, explained once:

- **Klipper** does the actual printing - it reads the G-code and drives the motors and heaters.
- **Moonraker** sits between Klipper and everything else, so the screen and your browser can
  both talk to the printer at once.
- **Mainsail** is the web page you open in a browser to control the printer.
- **NebulaScreen** is the app on the printer's own display.

[Words you will see](Glossary) has the rest.

## What you get

- **Guided calibration.** One menu that walks through each calibration in the order a new
  printer needs them, remembers which ones you have done, and tells you when one needs redoing
  because of something else you changed.
- **Live first-layer adjustment.** Nudge the nozzle height while watching the first layer
  print, in steps as small as 0.001 mm.
- **Control from anywhere on your network.** Upload from your computer, watch from your phone.
- **A camera**, if you have one, including the settings of Creality's own Nebula Camera.
- **Power-loss recovery** that can continue a print after the power goes out.
- **Updates that undo themselves if they fail.**
- **No cloud account.** Nothing is required to leave your network.

## Is it for you?

**Probably yes if** you want better print quality than the stock firmware gives you, you like
the idea of controlling the printer from a browser, and you are willing to spend a little time
calibrating.

**Probably not if** you need the printer working reliably tomorrow with no time to set it up.

Being straight about the costs:

- **It is not Creality's software and Creality will not support it.** Installing it is your
  decision.
- **You have to calibrate.** Your existing calibration does not carry over.
- **This is version 1.0.2.** It is actively developed, so expect it to keep changing.

## Check you have the right printer

NebulaOS supports the **Creality Ender-3 V3 KE** and nothing else. Its siblings are different
machines:

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
stock screen says anything other than "Ender-3 V3 KE", stop here. **Do not try to install it on
another printer.** The image is built for this machine's processor, display and mainboard.

## What you need

To install:

- A FAT32 USB stick, if you are coming from stock Creality firmware.
- A computer with SSH, if you are coming from OpenKE.
- Your **2.4 GHz** Wi-Fi name and password. If your router publishes separate names for its
  2.4 and 5 GHz networks, use the 2.4 GHz one.

To calibrate and print:

- An empty, clean bed and filament.
- Later, for some calibrations: a sheet of paper, a ruler or caliper, and for skew correction a
  printed test part.

Optional: a USB webcam or Creality's **Nebula Camera** ([Camera](Camera)), and a screen mount -
the KE's display is not positioned for comfortable use; community mounts exist on Thingiverse
and Printables.

## Safety first

**Hot and moving parts.**

- The **nozzle** reaches 300 °C and the **bed** 100 °C. Both stay dangerously hot for several
  minutes after a print ends, and neither looks hot.
- Several calibrations move the printhead and the bed **without warning you first**. Keep
  hands, hair, cables and tools out of the way before you start one, and do not reach in while
  one is running.

**Fire.** Never leave a print running in a room you are not in, or overnight. A 3D printer is a
heater with moving parts, and a working smoke alarm in the same room is a sensible precaution.

**Electrical.** Unplug the printer at the wall before opening any cover or touching wiring. The
power supply holds a charge after it is unplugged.

**Switching systems is safe.** You cannot permanently break the printer by installing NebulaOS
or by going back. Three things to know:

- **Do not switch the printer off while mainboard firmware is being installed.** The screen says
  when that is happening - it tells you not to switch off, and that Klipper is stopped. It takes
  a short time. If power is cut anyway, the printer can be recovered:
  [Mainboard firmware](Mainboard-Firmware).
- **After installing from stock Creality firmware, switch the printer off and on once** - the
  install page says exactly when.
- **Your print files and settings survive** going back and forth. Only a full USB recovery, the
  last resort, erases them, and it says so first.

## Built on

NebulaOS runs **unmodified upstream Klipper** and adds its own features as separate modules that
load alongside it, so upstream improvements and documentation keep applying. NebulaScreen is
based on **GuppyScreen** by ballaswag, under GPL-3. NebulaOS is open source, at
[github.com/NebulaOS-KE](https://github.com/NebulaOS-KE). More: [How NebulaOS works](Under-the-Hood).

## Next step

[2. Install NebulaOS](Installing-NebulaOS).

Need help? [Troubleshooting](Troubleshooting)
