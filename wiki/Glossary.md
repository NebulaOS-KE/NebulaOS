# Words you will see

Every term this manual cannot avoid, in plain language. If a page uses a word that is not here
and not explained where it appears, that is a bug in the manual - please report it.

## The software

**Klipper** - the software that does the actual printing. It reads your G-code file and drives
the motors and heaters. Open source, widely used, and the reason NebulaOS can tune things the
stock firmware cannot. NebulaOS runs unmodified upstream Klipper.

**Moonraker** - sits between Klipper and everything that wants to talk to it, so the printer's
screen and your web browser can both control the printer at the same time. You never interact
with it directly.

**Mainsail** - the web page you open in a browser to control the printer. Served by the printer
itself; no account, no internet needed.

**NebulaScreen** - the app on the printer's own touchscreen.

**Firmware** - software that lives inside a device rather than being installed like an app. The
printer has two kinds: the system NebulaOS replaces, and a smaller piece on the mainboard that
drives the motors.

**G-code** - the file your slicer produces. A long list of instructions: move here, extrude
this much, heat to this temperature. The `.gcode` file you print.

**Slicer** - the program on your computer that turns a 3D model into G-code. Orca, PrusaSlicer,
Cura and others.

## Printing

**First layer** - the first layer of plastic. It matters more than any other, because nothing
above it can be better than the layer it sits on.

**Z offset** - how far the nozzle sits above the bed when printing the first layer. Too high and
the lines do not stick together; too low and they smear. Adjustable live while printing.

**Baby-stepping** - nudging the Z offset in very small steps during a print, while watching the
result. The normal way to get a first layer right.

**Bed mesh** - a map of how flat your bed actually is. The printer probes a grid of points and
then compensates while printing. No bed is perfectly flat.

**Tramming** - making the four corners of the bed the same height, by adjusting them physically.
Done before meshing, because a mesh correcting a big tilt works harder than it should.

**Extrude** - push filament out. **Retract** - pull it back.

**Flow** - how much plastic comes out. Shown two ways: as a percentage in Fine Tune, and as a
volumetric rate in mm³/s on the print status screen. They are different numbers.

**Pressure advance** - compensates for plastic lagging behind the motor when the printhead
changes speed. Fixes bulging corners.

**Input shaper** - cancels vibration so sharp corners do not leave ripples ("ghosting") in the
surface.

**Skew** - when the printer's axes are not quite at right angles, so square parts come out as
slight parallelograms.

**E-steps** - how far the motor turns to feed a given length of filament. Wrong E-steps mean
every print is slightly over- or under-extruded.

**Purge line** - a short line of plastic printed before the model, to get extrusion flowing
cleanly first.

**Bed soak** - holding the bed at temperature for a while before printing, so the whole machine
reaches a stable temperature.

## The printer's hardware

**Nozzle** - the brass tip the plastic comes out of. Reaches 300 °C and does not look hot.

**Hotend** - the whole heated assembly the nozzle screws into.

**Bed** - the heated plate you print on. Reaches 100 °C.

**Load cell** - a sensor under the front-left bed screw that feels the nozzle touching the bed.
How the printer measures Z offset automatically.

**Accelerometer** - a sensor that measures vibration, used by input shaper. Already built in.

**MCU** - microcontroller unit. The small chip on the mainboard that drives the motors and
heaters, taking orders from Klipper. It has its own firmware.

**TMC** - the type of motor driver the KE uses. Tunable for quieter running - see
[TMC Autotune](TMC-Autotune).

## The system

**Boot slot** - one of the printer's two system storage areas, A and B. NebulaOS installs into
the one you are not using, which is how going back works.

**System image** - a complete NebulaOS, in one file. Installing one replaces the contents of the
other boot slot.

**OTA** - "over the air". An update downloaded by the printer itself rather than copied from a
USB stick.

**Trial start** - after a system update, the new slot has to prove it works. If it does not come
up within about 5 minutes, or restarts 3 times without confirming, the printer goes back by
itself.

**Clean reset** - erases NebulaOS's settings and calibration and starts as if newly installed.
Your print files survive.

**Persistent / data area** - the part of the printer's storage that is not part of either
system, where your files, configuration and calibration live. It survives switching systems and
reinstalling.

**SSH** - a way to type commands directly into the printer from a computer. You do not need it
for ordinary printing.

**IP address** - the printer's number on your network, like `192.168.1.42`. How you reach
Mainsail.

**`.local` name** - a friendlier way to reach the printer, like `nebulaos-4f2a.local`. Works on
most home networks, not all.

**DHCP** - your router handing out addresses automatically. The default, and usually what you
want. A **static IP** is one you set by hand instead.

## Other things you may see

**Spoolman** - optional software that tracks how much filament you have left on each spool.

**Exclude Object / Cancel Object** - cancelling one failed part from a plate of several while
the rest carries on.

**Adaptive meshing** - probing only the part of the bed the print actually covers, instead of
all of it. Faster.

**OpenKE** - another community firmware for this printer. Some people install NebulaOS from it.

**GuppyScreen** - the touchscreen app NebulaScreen is based on, by ballaswag.

**Buildroot** - the toolkit used to build the NebulaOS system image. Only relevant if you build
NebulaOS yourself.

**Macro** - a named sequence of G-code commands you can trigger as one action.

**Console** - a screen where you can type Klipper commands directly. Powerful and easy to
misuse; nothing in this manual requires it.
