# 2. Install NebulaOS

## What this guide will help you do

Put NebulaOS onto your Creality Ender-3 V3 KE. When you are done, the printer starts into
NebulaOS, and your old system is still there in the other slot in case you want it back.

## What you need

- A Creality Ender-3 V3 KE. Nothing else is supported - see
  [Check you have the right printer](What-NebulaOS-Is#check-you-have-the-right-printer).
- The right NebulaOS image file, from
  [NebulaOS releases](https://github.com/NebulaOS-KE/NebulaOS/releases). **Which one depends on
  the route** (section 1 below). For 1.0.2 the files are:

  | File | What it is |
  |---|---|
  | `NebulaOS-Ender3V3KE-F005_ota_img_V9.1.0.2.img` | **From stock Creality firmware, with the touchscreen (section 2b).** The file with `ota_img` in its name - Creality's touchscreen updater offers only a file named like this |
  | `NebulaOS-Ender3V3KE-1.0.2.img` | **From OpenKE, over SSH (section 2a).** The printer also uses this one for online updates. Creality's touchscreen ignores it |
  | `NebulaOS-Ender3V3KE-1.0.2.img.sha256` | Its checksum, for the optional download check below |
  | `NebulaOS-Ender3V3KE-1.0.2.ingenic` | Only for USB recovery on a printer that will not start - see [Recovery](Recovery). **Not** for a normal install |
  | `NebulaOS-Ender3V3KE-1.0.2.ingenic.sha256` | Its checksum |
  | `nebulaos-release.json` | Machine-readable release details; the printer uses it for online updates |

  The file with `ota_img` in its name exists from 1.0.1 on. 1.0.0 has only the normal `.img`,
  so for the touchscreen route use 1.0.1 or newer. The examples on this page use 1.0.2; if you
  downloaded a different version, use its number.
- **If you are coming from stock Creality firmware:** a USB stick formatted as FAT32.
- **If you are coming from OpenKE:** your usual SFTP and SSH tools, and OpenKE's root
  password.
- About 15 minutes, and a printer you do not need to use during them.

## Before you begin

- Read [Safety first](What-NebulaOS-Is#safety-first). The point that applies here: switching between systems is
  safe, but **do not switch the printer off while mainboard firmware is being installed** - the
  screen tells you when that is happening.
- **Coming from stock Creality firmware?** Plan for one power cycle after the install - see
  section 3. It is part of the route, not a fault.
- Make sure no print is running.
- **Do not rename either image file.** Creality's updater finds the parts inside the file by its
  name. A renamed file stops with `failed to get .../ota_config.in` and installs nothing. The
  `ota_img` file in particular only works under its original name.
- Check your download if you can. On Linux or macOS, in the folder with both files:

  ```
  sha256sum -c NebulaOS-Ender3V3KE-1.0.2.img.sha256
  ```

  You want to see `OK`. If it says `FAILED`, download the file again - do not install it.

## 1. Which route are you on?

| Your printer right now | Go to |
|---|---|
| Stock Creality firmware, with Creality's touchscreen | Section 2b |
| OpenKE, usually with no Creality touchscreen | Section 2a |

If you are not sure, you are almost certainly on stock Creality firmware: section 2b.

## 2a. From OpenKE, over SSH

You need the SFTP and SSH tools you already use with OpenKE - for example WinSCP, FileZilla or
`scp` for copying, and PuTTY or a terminal for the shell. Log in as `root` with **OpenKE's**
password (the system running on the printer now, not NebulaOS's). This route uses the
**normal** `.img`, the one without `ota_img` in its name.

1. Copy `NebulaOS-Ender3V3KE-1.0.2.img` to `/usr/data/` on the printer. Do not rename it.
2. In an SSH session on the printer, run:

   ```
   /etc/ota_bin/local_ota_update.sh /usr/data/NebulaOS-Ender3V3KE-1.0.2.img
   ```

   Wait for `ota update ok`. A line `sh: 1.1.0.15: bad number` on the way is harmless - it
   comes from the updater's own version check and stops nothing.
3. Then, in the same session:

   ```
   reboot
   ```

   The updater does not restart the printer by itself, so this step is required. Use `reboot`,
   not the power switch: a stock-based system that starts from power-on can install its own
   firmware into the mainboard again.

Now go to section 3.

## 2b. From stock Creality firmware, using the touchscreen

This is the usual route if your printer still has Creality's software on it.

1. Copy the file with `ota_img` in its name - for 1.0.2,
   `NebulaOS-Ender3V3KE-F005_ota_img_V9.1.0.2.img` - to the top level of a FAT32 USB stick.
   Do not put it in a folder, and do not rename it. The normal `NebulaOS-Ender3V3KE-1.0.2.img`
   does not work here: Creality's screen does not offer it.
2. Plug the USB stick into the printer.
3. Start the update from Creality's own screen, the same way you would install a Creality
   firmware update.

Creality's screen uses the same updater as section 2a, and it restarts the printer itself when
it finishes. **After that, one power cycle is needed** - section 3 says when.

Now go to section 3.

## 3. First start

The first start of NebulaOS takes about a minute. Later starts take about 15 seconds. Do not
switch the printer off while you wait.

**If you came from stock Creality firmware (section 2b): switch the printer off once.** When
the printer restarts by software from Creality's system into NebulaOS - which is what
Creality's updater does - the mainboard does not accept new firmware until its power has been
cut. So on this first start NebulaOS cannot install its mainboard firmware yet, and Klipper
reports an MCU error. That is expected. There is no way to do this from software: nothing in
the printer can reset the mainboard except its power.

1. Wait until NebulaOS is up and its screen is showing.
2. Switch the printer off with its power switch, wait **10 seconds**, and switch it on again.
3. On this start NebulaOS installs its mainboard firmware by itself. **Do not switch off while
   it runs** - the screen tells you when it is happening. Klipper then connects.

From 1.0.1 the screen shows a notice telling you to do this: *"The mainboard firmware could not
be installed. Switch the printer off, wait 10 seconds and switch it on again - NebulaOS installs it
when it starts."*

**If you came from OpenKE (section 2a):** the `reboot` is a software restart too, and the same
rule applies. Whether NebulaOS has to install its mainboard firmware at all depends on what OpenKE
left on the board, so on some printers nothing is needed. If the screen shows that notice, or
*"The printer's mainboard is not answering. Switch the printer off, wait 10 seconds and switch it
on again."*, do exactly that, once.

If you came from OpenKE, delete the copied image afterwards to free the space it used - in an SSH
session on the printer:

```
rm /usr/data/NebulaOS-Ender3V3KE-1.0.2.img
```

**SSH on NebulaOS:** user `root`, password `NebulaOS` on a new install. Change it, and never make
SSH reachable from the internet: [SSH, SFTP and security](SSH-And-SFTP).

*The notices are from `etc/init.d/S50nebulaos-mcu-guard:98-132`, firmware `dc868e3`.*

*One screenshot is still missing here: the NebulaOS screen as it looks on the very first
start. The simulator's screenshot tour does not cover the boot and init screens, so this one
needs a photograph of a real printer starting up.*

## Expected result

- The printer starts into NebulaOS, showing the NebulaScreen interface rather than Creality's.
- **Settings → System** reports a NebulaOS version.
- Your old system is still installed in the other slot.

## If it stops

Every check runs **before** anything is written. If the updater prints `ota: error` before it
prints `ota: started`, then nothing was changed and your printer is still running its old
system exactly as before.

| What you see | What it means |
|---|---|
| `failed to get .../ota_config.in` | The file was renamed. Download it again and keep the original name. |
| Creality's touchscreen does not offer the file | It is the wrong file, or it was renamed or put in a folder. Use the file with `ota_img` in its name, unrenamed, at the top level of the stick. |
| An MCU error, or the mainboard not answering, right after installing from stock | Expected until the power has been cut once. Switch the printer off, wait 10 seconds, switch it on - see section 3. |
| `sh: 1.1.0.15: bad number` | Harmless. Not an error you need to act on. |
| `ota: error` before `ota: started` | Nothing was written. The old system is intact. |
| `FAILED` from the checksum command | The download is damaged. Download it again. |
| Nothing on the screen after the restart | Go to [Recovery](Recovery). |

If something else happens, please report it with the output you saw:
[Troubleshooting](Troubleshooting).

## Going back

Your old system is still in the first slot. [Going Back](Going-Back) covers the options:
the swap-boot-slot button on the NebulaOS screen, SSH, and USB recovery for a printer that
will not start at all.

Worth knowing now, so it is not a surprise later: your `printer.cfg`, macros, Wi-Fi networks,
uploaded files and screen settings live on a shared data area and **survive** a slot switch in
either direction.

## Later updates

Once NebulaOS is running, it updates itself from the screen - no USB stick and no SSH. See
[Updating NebulaOS](Updating-NebulaOS).

## Next step

[3. First start](First-Time-Setup) - Wi-Fi, the printer's address, and Mainsail.

Need help? [Troubleshooting](Troubleshooting) · How this works: [Two system slots](Two-System-Slots)
