# Installing NebulaOS

## What this guide will help you do

Put NebulaOS onto your Creality Ender-3 V3 KE. When you are done, the printer starts into
NebulaOS, and your old system is still there in the other slot in case you want it back.

## What you need

- A Creality Ender-3 V3 KE. Nothing else is supported - see
  [Supported hardware](Supported-Hardware).
- The NebulaOS image file and its checksum file, from
  [NebulaOS releases](https://github.com/NebulaOS-KE/NebulaOS/releases):
  `NebulaOS-Ender3V3KE-<version>.img` and `NebulaOS-Ender3V3KE-<version>.sha256`.
- **If you are coming from stock Creality firmware:** a USB stick formatted as FAT32.
- **If you are coming from OpenKE:** a computer that can use SSH, and your printer's root
  password.
- About 15 minutes, and a printer you do not need to use during them.

## Before you begin

- Read [Safety first](Safety-First). The point that applies here: switching between systems is
  safe, but **do not switch the printer off while mainboard firmware is being installed** - the
  screen tells you when that is happening.
- Make sure no print is running.
- **Do not rename the image file.** Creality's updater finds the parts inside the file by its
  name. A renamed file stops with `failed to get .../ota_config.in` and installs nothing.
- Check your download if you can. On Linux or macOS, in the folder with both files:

  ```
  sha256sum -c NebulaOS-Ender3V3KE-<version>.img.sha256
  ```

  You want to see `OK`. If it says `FAILED`, download the file again - do not install it.

## 1. Which route are you on?

| Your printer right now | Go to |
|---|---|
| Stock Creality firmware, with Creality's touchscreen | Section 2b |
| OpenKE, usually with no Creality touchscreen | Section 2a |

If you are not sure, you are almost certainly on stock Creality firmware: section 2b.

## 2a. From OpenKE, over SSH

Replace `<printer-ip>` with your printer's address and `<version>` with the version you
downloaded.

1. Copy the image to the printer:

   ```
   scp NebulaOS-Ender3V3KE-<version>.img root@<printer-ip>:/usr/data/
   ```

   It will ask for your printer's root password - the password of the system running on it
   **now** (OpenKE), not NebulaOS's. The file is about 133 MB, so this takes a minute or two.

2. Start the installation:

   ```
   ssh root@<printer-ip> /etc/ota_bin/local_ota_update.sh /usr/data/NebulaOS-Ender3V3KE-<version>.img
   ```

   The updater unpacks the file, checks every part, then writes the kernel, the system and the
   power-on logo, printing percentages as it goes. It finishes with `ota update ok`.

   **One normal-looking error:** a line reading `sh: 1.1.0.15: bad number` is harmless. It
   comes from the updater's own version check and stops nothing. Keep going.

3. Restart the printer with a soft reboot:

   ```
   ssh root@<printer-ip> reboot
   ```

   The updater does not restart the printer by itself, so this step is required. A soft reboot
   is the tidy way to do it: it lets the system shut down cleanly rather than being cut off.

Now go to section 3.

## 2b. From stock Creality firmware, using the touchscreen

This is the usual route if your printer still has Creality's software on it.

1. Copy `NebulaOS-Ender3V3KE-<version>.img` to the top level of a FAT32 USB stick. Do not put
   it in a folder, and do not rename it.
2. Plug the USB stick into the printer.
3. Start the update from Creality's own screen, the same way you would install a Creality
   firmware update.

Creality's screen uses the same updater as section 2a, and it restarts the printer itself when
it finishes.

Now go to section 3.

## 3. First start

The first start of NebulaOS takes about a minute. Later starts take about 15 seconds. Do not
switch the printer off while you wait.

When it comes up:

1. Connect to Wi-Fi: **Settings → Connections → Wi-Fi networks**. Step-by-step in
   [Connecting to Wi-Fi](Connecting-To-WiFi).

   ![The Wi-Fi networks panel](images/03-wifi.png)
2. Calibrate the printer once before printing - the calibrations from your old system do not
   carry over. [Calibration guide](Calibration-Guide).
3. If you used SSH, delete the copied image to free 133 MB:

   ```
   ssh root@<printer-ip> rm /usr/data/NebulaOS-Ender3V3KE-<version>.img
   ```

Mainsail is now at `http://<printer-ip>` in a web browser, or
`http://<printer-name>.local`. See [Opening Mainsail](Opening-Mainsail).

Your printer has given itself a name like `nebulaos-4f2a` - four characters derived from its
own hardware, so that two printers on one network do not collide. You can change it on
**Settings → Connections → Name → Change**.

**If you ever need SSH**, the root password on a newly installed NebulaOS is `NebulaOS`. You do
not need SSH for normal use, and you should change that password if your printer is reachable
from beyond your own network. A printer that already ran an earlier NebulaOS keeps whatever
password it had.

*One screenshot is still missing here: the NebulaOS screen as it looks on the very first
start. The simulator's screenshot tour does not cover the boot and init screens, so this one
needs a photograph of a real printer starting up.*

## Expected result

- The printer starts into NebulaOS, showing the NebulaScreen interface rather than Creality's.
- **Settings → System** reports a NebulaOS version.
- Mainsail opens in a browser on the same network.
- Your old system is still installed in the other slot.

## If it stops

Every check runs **before** anything is written. If the updater prints `ota: error` before it
prints `ota: started`, then nothing was changed and your printer is still running its old
system exactly as before.

| What you see | What it means |
|---|---|
| `failed to get .../ota_config.in` | The file was renamed. Download it again and keep the original name. |
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
