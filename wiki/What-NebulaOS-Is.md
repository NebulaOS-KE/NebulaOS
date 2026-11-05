# What NebulaOS is

## In one paragraph

NebulaOS is replacement software for the **Creality Ender-3 V3 KE** 3D printer. It replaces
everything Creality installed - the operating system, the printing software and the touchscreen
app - with an open system built around Klipper. You install it onto the printer's second system
slot, so the software you have now stays where it is and you can go back.

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

- **Real calibration.** A guided menu that walks through each calibration in the order a new
  printer needs them, remembers which ones you have done, and tells you when one needs redoing
  because of something else you changed.
- **Live first-layer adjustment.** Nudge the nozzle height while watching the first layer
  print, in steps as small as 0.001 mm.
- **Control from anywhere on your network.** Upload from your computer, watch from your phone.
- **A camera**, if you have one, including the settings of Creality's own Nebula Camera.
- **Power-loss recovery** that can continue a print after the power goes out.
- **Two system slots**, so a bad update can be undone by starting the other one.
- **No cloud account.** Nothing is required to leave your network.

## What it costs you

Being straight about this matters more than selling it:

- **It is not Creality's software and Creality will not support it.** Installing it is your
  decision.
- **You have to calibrate.** Your existing calibration does not carry over, and skipping it
  means chasing first-layer problems that an hour of calibration would have fixed.
- **This is version 1.0.1.** It is actively developed, so expect it to
  keep changing.
- **Only the Ender-3 V3 KE.** See [Supported hardware](Supported-Hardware).
- **Some things need a computer.** Not many, and not for ordinary printing.

## What it is built on

NebulaOS is not a fork of Klipper. It runs **unmodified upstream Klipper** and adds its own
features as separate modules that load alongside it. That is a deliberate choice: upstream
improvements and upstream documentation keep applying, and NebulaOS's own additions are clearly
separable from them.

NebulaScreen is based on **GuppyScreen** by ballaswag, under GPL-3. NebulaOS is open source, and
the repositories are at [github.com/NebulaOS-KE](https://github.com/NebulaOS-KE).

## Is it for you?

**Probably yes if** you want better print quality than the stock firmware gives you, you like
the idea of controlling the printer from a browser, and you are willing to spend an hour
calibrating.

**Probably not if** you need the printer working reliably tomorrow with no time to set it up,
or you are not comfortable that going back involves a menu rather than a button.

## Next step

[Supported hardware](Supported-Hardware) - check your printer, and what else you need.
