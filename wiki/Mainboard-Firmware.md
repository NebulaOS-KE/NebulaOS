# Mainboard firmware

## What this page will help you do

Understand the small piece of firmware on the printer's mainboard, why it changes by itself when
you switch systems, and how to install a different one if you need to.

## What you need

Nothing for the normal case - NebulaOS manages this on its own. For installing a specific
firmware file: a `.bin` file, and either a USB stick or Mainsail.

## The short version

The mainboard has its own firmware, separate from the system NebulaOS replaces. Each system
needs its own version, and **each system puts its own version back automatically**:

- Creality's system installs its firmware when it starts from cold.
- NebulaOS checks the board at every boot and reinstalls its own if it finds a known Creality
  version there.

So switching between systems is safe and self-correcting. You do not need to do anything, and
you cannot get stuck by using the power switch.

**Firmware you installed yourself is left alone.** NebulaOS only replaces what it recognises as
a known Creality version. If you deliberately installed something else, it stays.

## The one thing worth waiting for

**Do not switch the printer off while firmware is being installed.** The screen tells you when
that is happening - it says not to switch off, and that Klipper is stopped. It takes a short
time. Wait for it.

**If it does get interrupted, the printer fixes it.** The board keeps Creality's small built-in
loader in a place firmware installs never write; only the firmware on top of it is replaced. An
interrupted install therefore leaves the loader intact and the firmware incomplete, which means
the printer will not print until the firmware is written again - and writing it again is
something this printer can do on its own.

The screen notices and offers it: *"The firmware was written, but Klipper does not reach the
mainboard. Reinstall the built-in MCU firmware?"* You can also start it yourself at any time
with **Reinstall built-in firmware** below.

No computer, no cable, no disassembly.

## Where the controls are

**Settings → Printer → MCU firmware.**

| Option | What it does |
|---|---|
| **Built-in MCU firmware** | Reinstalls the version that came with your NebulaOS image |
| **Install MCU firmware** | Installs a `.bin` file you provide |

To provide a file, put it either on a USB stick, or upload it in Mainsail to **Machine →
config → uploads → mainboard-firmware**. The screen lists what it finds.

*No screenshot yet: the MCU firmware page is not reached by the simulator's capture tour. This
one needs a photograph of a real printer.*

## Step-by-step: reinstalling the built-in firmware

Worth doing if the screen reports it cannot reach the board, or after you have been running
another system.

1. **Settings → Printer → MCU firmware**.
2. Tap **Built-in MCU firmware**.
3. Confirm.
4. **Wait.** Klipper stops, the board is reflashed, and Klipper restarts. The screen says not to
   switch off while this runs.
5. The screen reports the firmware it now finds on the board.

## Step-by-step: installing your own firmware file

1. Put the `.bin` on a FAT32 USB stick, **or** upload it in Mainsail to **Machine → config →
   uploads → mainboard-firmware**.
2. **Settings → Printer → MCU firmware → Install MCU firmware**.
3. Pick your file from the list.
4. Confirm, and wait as above.

Once you have installed your own firmware, NebulaOS will not replace it at boot - it only
reinstalls over a version it recognises as Creality's.

## Expected result

The screen reports the board running the firmware you installed, and Klipper connects.

## Troubleshooting

| What happens | What to do |
|---|---|
| "Klipper can't reach the board" | Reinstall the built-in firmware, as above. |
| No files are listed | Check the USB stick is FAT32, or that the upload went to **uploads → mainboard-firmware**. |
| You switched off during a flash | The board may need recovery from a computer. See [Recovery](Recovery). |
| The firmware changed by itself after switching systems | Expected - each system reinstalls its own. See the short version above. |

## Recovery and reversal

**Built-in MCU firmware** is the way back from any firmware you installed. It is always
available and does not need a file.

## Related

- [Safety first](Safety-First)
- [Going back to your old firmware](Going-Back)
- [Recovery](Recovery)
