# Recovery

## What this page will help you do

Get your printer working again when something has gone wrong - from "I want the other system
back" to "it will not switch on at all".

NebulaOS has four ways back. They are listed from least drastic to most. **Use the first one
that fits your situation**, and only move down the list if it does not apply.

| What is happening | What to do |
|---|---|
| A new system image did not come up properly | Nothing - NebulaOS goes back by itself. See 1. |
| NebulaOS runs, but you want the other slot | **Settings → Reset → Swap boot slot**. See 2. |
| The screen is dead, but the printer is on your network | SSH, then switch the slot. See 3. |
| Nothing starts at all | USB recovery from a computer. See 4. |

## Before you begin

Options 1 to 3 do not erase anything. Your `printer.cfg`, macros, `moonraker.conf`, Wi-Fi
networks, uploaded files and screen settings live on a shared data area and survive all three.

Option 4 has two forms, and **one of them erases everything**. That is called out where it
applies. Do not jump to option 4 because it sounds thorough.

## 1. Automatic: the trial start

You do not have to do anything for this one. It is worth understanding, because it explains a
printer that appears to undo an update on its own.

After you install a system image **from the screen**, the new slot starts on trial. NebulaOS
waits for Klipper and the screen to come up, and:

- if they do not come up within **5 minutes**, or
- if the new system restarts **3 times** without ever being confirmed - a watchdog restart
  after a freeze counts,

then NebulaOS switches back to the previous slot, once, by itself. The screen tells you what
happened when it comes up.

A screen shed by the memory guard counts as a successful start, and a power cut during the
trial makes the trial run again on the next start.

**This does not cover:** an install done through Creality's updater, which has no trial at all,
or a kernel that does not start.

*Verified in the implementation at firmware commit `82e1320`
(`nebulaos_osconfig/image.py`: `TRIAL_SECONDS = 300`, `TRIAL_ATTEMPTS = 3`). Not observed on a
printer by the author of this page.*

## 2. Swap the boot slot from the screen

**The easy one.** Use this whenever NebulaOS still starts.

1. On the printer, go to **Settings → Reset → Swap boot slot**.
2. The confirmation tells you what is installed in the other slot. Read it - this is how you
   check you are about to start the thing you expect.
3. Confirm. The printer restarts into the other slot.

This button is blocked while a print is running.

**One-way warning.** If the other slot holds a stock Creality or OpenKE system, those have no
NebulaOS swap button, so coming back needs option 3 or 4. Know that before you press it.

**Do not power-cycle a printer running the stock system.** A stock power-on can write old
firmware into the mainboard. Use a soft restart. See [Safety first](Safety-First).

## 3. Over SSH

Use this when the screen is dead or unresponsive but the printer is still on your network.

Both NebulaOS and stock/OpenKE systems accept SSH as `root`. Which slot starts is decided by a
marker file, and the exact steps are maintained with the firmware:

- [How to switch between stock and custom](https://github.com/NebulaOS-KE/NebulaOS-firmware/blob/main/docs/HOW_TO_SWITCH_STOCK_AND_CUSTOM.md)

If SSH does not answer either, go to option 4.

## 4. USB recovery from a computer

**The last resort,** for a printer that does not start at all.

The printer's board has a USB recovery mode built into its silicon, called mask ROM. It works
even when no system on the printer starts.

To enter it:

1. Power the printer off.
2. Hold **both** small buttons next to the screen's micro-USB port for 3 seconds.
3. Release the **reset** button first.
4. Connect the printer to a computer with a USB cable.

Then choose one of two things to do - they are very different:

### 4a. Just switch the boot slot back

Nothing is erased. This only rewrites the marker that chooses the slot.

Use NebulaOS-firmware's `tools/recovery/usb-set-boot-slot.sh A` (or `B`) with the pinned
`usbboot` tool. Steps:
[Developer recovery](https://github.com/NebulaOS-KE/NebulaOS-firmware/blob/main/docs/DEVELOPER_RECOVERY.md#3-usb-recovery--the-panic-button).

Tested on Linux on 2026-10-14.

### 4b. Write the whole system again

**This erases your settings, your print files and your calibration.** Only the printer's
factory serial number and network address are kept.

Each release includes an `.ingenic` file for the Ingenic USB Cloner. It rewrites the printer
from scratch: NebulaOS in slot 2, Creality's stock system in slot 1.

**This has not been tested on a printer by the NebulaOS project.** Use it only when nothing
else has worked, and expect to set the printer up from nothing afterwards.

## What survives

| | Survives a slot switch? |
|---|---|
| `printer.cfg` and macros | Yes |
| `moonraker.conf` | Yes |
| Saved Wi-Fi networks | Yes |
| Uploaded print files | Yes |
| Screen settings | Yes |
| Calibration results | Yes |
| Anything at all, after a full USB rewrite (4b) | **No** |

The two systems keep their own settings separate from each other.

## When to ask for help

If you have worked down this list and the printer still does not start, please open an issue
with what you tried and what you saw:
[github.com/NebulaOS-KE/NebulaOS/issues](https://github.com/NebulaOS-KE/NebulaOS/issues).
A printer in USB recovery mode is not bricked - it is recoverable, and worth asking about
before doing anything irreversible.
