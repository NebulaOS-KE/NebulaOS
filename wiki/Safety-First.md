# Safety first

## What this page will help you do

Understand the few things that can actually hurt you or permanently damage your printer, so
that nothing in this manual takes you by surprise. Please read it before you install NebulaOS.

## The one that can break your printer for good

**Never switch the printer off and on again while it is running Creality's original
software.** Use a soft restart instead - the printer restarting itself from a command or a
menu, not the power switch.

Here is why this matters. Creality's system checks the printer's mainboard when it starts up
from a cold power-on, and it can write old mainboard firmware back onto it. If that happens
after you have installed NebulaOS, the mainboard and the system stop matching, and getting
the printer working again needs a USB recovery procedure from a computer.

In practice this affects you in two situations:

- While you are installing NebulaOS from the stock Creality system.
- Any time you switch back to a Creality or OpenKE slot later.

Once NebulaOS is the system that starts, ordinary power switching is fine.

## Hot and moving parts

- The **nozzle** reaches 300 °C and the **bed** 100 °C. Both stay dangerously hot for several
  minutes after a print ends, and neither looks hot.
- Several calibrations move the printhead and the bed **without warning you first**. Keep
  hands, hair, cables and tools out of the way before you start one, and do not reach in to
  tidy something while a calibration is running.
- A few calibrations do not move or heat anything at all. Each calibration page says which
  kind it is, at the top.

## Electrical

- Unplug the printer at the wall before opening any cover or touching wiring.
- The printer's power supply holds a charge after it is unplugged. If you are not comfortable
  working inside mains equipment, do not.

## Fire

Never leave a print running in a room you are not in, or overnight. A 3D printer is a heater
with moving parts, and a working smoke alarm in the same room is a sensible precaution.

## Before you install anything

- **You can go back.** NebulaOS installs into the printer's second system slot and leaves your
  current system in the first one. [Going back to your old firmware](Going-Back) explains how
  to return.
- **Your print files and settings survive a slot switch.** They live on a separate data area
  that both systems share.
- **A full USB recovery does not.** That procedure rewrites the printer from scratch and
  erases your settings, prints and calibration. It is the last resort, not a routine step.

## What this manual promises you

- No step asks you to do something without saying what it will do.
- Anything that can lose data says so before you do it, not after.
- Where a procedure has not been tested on a real printer, the page says so. Those notes are
  not disclaimers to skim past - they tell you exactly how much confidence to place in the
  instructions you are about to follow.
