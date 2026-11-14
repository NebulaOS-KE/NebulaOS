# Troubleshooting

Find what you see, grouped by what you were doing: installing, connecting, calibrating,
printing, updating. If nothing here fits, [Report a problem](Report-A-Problem) - the screen saves
the logs for you.

## Start here: the printer is not working at all

| What you see | Where to go |
|---|---|
| Nothing happens when you switch it on | No lights or fans at all is a power problem, not a NebulaOS one - check the switch, the cable and the fuse. If it has lights but a dead screen, see the next row. |
| The printer powers on but the screen stays black | Wait two full minutes first - a first start takes about a minute. Then [Recovery](Recovery): if the printer answers on the network the screen alone has failed, and if it does not, use the boot-slot or USB routes. |
| The screen works but nothing responds to touch | See **Screen and touch** below - most often the touch calibration. |
| The screen is fine but Mainsail will not open | See **Network** below, and [First start](First-Time-Setup#open-mainsail). |
| It worked before an update and not after | Wait five minutes: a system image that does not come up properly is undone automatically. See [Recovery](Recovery#1-automatic-the-trial-start). |
| The printer restarted by itself, and the screen says *"The printer restarted by itself because its system stopped responding"* | The touchscreen computer froze and its watchdog restarted it. If a print was running, see whether the screen offers to resume it ([Power-loss recovery](Power-Loss-Recovery)). Then please send us the logs: the printer kept what happened just before the freeze. See [After the printer restarted by itself](Report-A-Problem#after-the-printer-restarted-by-itself). |
| You just installed NebulaOS and nothing works | [Installing NebulaOS](Installing-NebulaOS), then [Recovery](Recovery). Your old system is still in the other slot. |

---

## Installing

| Symptom | Fix |
|---|---|
| Creality's updater stops with `failed to get .../ota_config.in` | The `.img` was renamed. Download it again or give it back its release name. Nothing was installed. |
| Creality's touchscreen does not offer the NebulaOS file on the USB stick | Use the file with `ota_img` in its name, not the normal `.img`; do not rename it, and put it at the top level of the stick. See [Installing NebulaOS](Installing-NebulaOS#2b-from-stock-creality-firmware-using-the-touchscreen). |
| MCU Protocol error, or the mainboard not answering, after installing from stock | Power-cycle once: switch the printer off, wait 10 seconds, switch it on. NebulaOS then installs its mainboard firmware by itself - do not switch off while it runs. See [Installing NebulaOS](Installing-NebulaOS#3-first-start). |
| Creality's updater ends with `ota update ok`, but the printer still runs the old system | It does not restart by itself. Reboot it: `ssh root@<printer-ip> reboot`. See [Installing NebulaOS](Installing-NebulaOS). |

---

## Connecting

| Symptom | Fix |
|---|---|
| Not connected to Wi-Fi | **Settings → Connections → Wi-Fi networks**. After a clean NebulaOS reset, Wi-Fi has to be set up again here. See [First start](First-Time-Setup#connect-to-wi-fi). |
| Mainsail will not open in a browser | Check that your computer or phone is on the **same** network - not a guest network and not mobile data. Read the address again from **Settings → Connections**; your router may have given the printer a different one. See [First start](First-Time-Setup#open-mainsail). |
| `printername.local` does not work but the numbers do | Some routers and some Android versions do not support `.local` names. Use the numeric address. |
| Two printers clash on the network | Each printer names itself `nebulaos-` plus four characters from its own hardware, so this should not happen. If you renamed both the same, rename one: **Settings → Connections → Name → Change**. |
| A static IP setting does not work | NebulaOS checks a new static address (gateway reachable) and switches back automatically when it does not work; this can take a couple of minutes. The setting applies to all Wi-Fi networks. |
| Wi-Fi events | **Settings → System → Logs** shows the Wi-Fi lines of `system.log`. |

---

## Calibrating

Starting from what the print looks like is often quicker: [Improve your prints](Improve-Your-Prints).

| Symptom | Fix |
|---|---|
| First layer uneven left to right, bed mesh does not help | [Axis Twist](Calibration-Explained#axis-twist). |
| One corner of the bed high or low | [Bed tramming](Calibration-Explained#bed-tramming). |
| First layer uneven everywhere | Re-run the bed mesh: **Tune → Bed Mesh → Calibrate**. Clean the bed (IPA) and check nothing is loose. |
| First layer too high or too low everywhere | Baby-step Z offset: **Tune → Z Offset**, or tap the Z readout on the print status screen. |
| Parts not square | [Skew Correction](Calibration-Explained#skew-correction). |
| Ghosting / echoes after sharp corners | [Input shaper](Calibration-Explained#input-shaper): **Tune → Calibration → Input Shaper**. |
| Corner bulges, blobs or gaps | Pressure advance and flow: [Calibration explained](Calibration-Explained#flow-pressure-advance-and-temperature). |
| Auto Calibration says **Failed: <step>** | The page says *Why* and *What to do*; nothing was saved. Fix it and run it again. Load cell steps: **Tune → Calibration → Load Cell Calibration** shows the reason. See [Calibration explained](Calibration-Explained#load-cell-calibration). |
| A calibration row says **Redo:** | Something you changed since made it stale - run that row again. See [Calibration explained](Calibration-Explained#the-status-line-under-every-row). |
| A calibration refuses to start | A print is running, or something else is: calibration rows are locked while printing. |
| **The nozzle did not touch the bed** (new wording), or `No trigger on probe after full movement` (before the update) | The Z-offset calibration could not reach the bed. Fixed in Klipper extensions 1.0.1: **Settings → Updates**. Details, and what to do on a printer that cannot update: [The nozzle does not reach the bed](#the-nozzle-does-not-reach-the-bed-z-offset-calibration). |
| `measurement rejected - no_accepted_samples (samples: 3 taken, 0 accepted)` | The same cause, one step later: the touches were measured but rejected as implausible. Same fix, same update: [The nozzle does not reach the bed](#the-nozzle-does-not-reach-the-bed-z-offset-calibration). |

---

### The nozzle does not reach the bed (Z-offset calibration)

**Who this is for.** A small number of printers - so far the ones with **silicone bed spacers**
instead of the stock mount - fail every Auto Calibration or Z-offset calibration on NebulaOS
1.0.2, in one of two ways:

1. Right after installing, with the CR-Touch Z offset still at `0.000`, the console says
   `No trigger on probe after full movement` three times and the nozzle stops a fraction of a
   millimetre above the bed.
2. After setting a Z offset by hand:
   `NEBULAOS_Z_OFFSET_CALIBRATE: measurement rejected - no_accepted_samples (samples: 3 taken, 0 accepted)`.

If your printer calibrates normally, this does not affect you and there is nothing to change.

**Why it happens.** Two limits in the calibration were set from measurements on one printer. A
softer bed mount needs the nozzle to travel a little further down, and to press a little longer,
before the load cell reports contact - so the search stopped above the bed, and the touches that
did happen looked too far from the expected plane to be trusted.

**The fix is an update, and it is out.** Klipper extensions **1.0.1** carries it.

1. **Settings → Updates** on the printer, then **NebulaOS extensions → Update** (or **Update
   all**). Klipper stops while it installs and comes back by itself.
2. Run the calibration again: **Tune → Calibration → Auto Calibration**, or **Z Offset** on its
   own.
3. If you already added the two `printer.cfg` lines below, you can now remove the
   `[nebulaos_calibration]` block. Leave the `z_offset` line alone - a successful calibration
   overwrites it with the real value.

That is all most printers need. The rest of this section is for a printer that cannot update
yet - no network, or an update that will not install.

#### Without the update: two lines in `printer.cfg`

Open Mainsail → **Machine** → `printer.cfg`.

1. Near the bottom, in the block the printer writes for itself, change

   ```
   #*# z_offset = 0.000
   ```

   to

   ```
   #*# z_offset = 3.000
   ```

   A `0.000` there means *not calibrated yet*, and that is the case where the search floor is
   too shallow. Any credible value sends the calibration down the normal route, which reaches
   about a millimetre past where it expects the bed to be.

2. **Above** the line

   ```
   #*# <---------------------- SAVE_CONFIG ---------------------->
   ```

   add

   ```
   [nebulaos_calibration]
   max_abs_fit_delta: 0.5
   ```

   This widens the plausibility check on a touch from 0.3 mm to 0.5 mm. It must be below the
   `[include ...]` lines, which is what putting it here achieves.

3. **Save & Restart**, then run the calibration again: **Tune → Calibration → Auto Calibration**,
   or **Z Offset** on its own.

It measures the real offset and saves it over the `3.000`. **Do not print until it succeeds** -
until then the printer believes the nozzle sits 3 mm further from the bed than it does.

Both lines stay harmless after the update, so there is no hurry to remove them.

**If you would rather not touch `printer.cfg`**, the old-fashioned route still works and does not
use the load cell at all: the paper test with `PROBE_CALIBRATE`, then `SAVE_CONFIG`. See
[Calibration explained](Calibration-Explained#load-cell-calibration) for where the load cell fits
in, and [Report a problem](Report-A-Problem) if neither route gets you a first layer.

---

## Printing

| Symptom | Fix |
|---|---|
| A print will not start at all | Check the printer is idle and the file sliced correctly. See [Your first print](Printing). |
| The print stopped partway | Check for filament runout - see [Load filament](Printing#load-filament). After a power cut, see [Power-loss recovery](Power-Loss-Recovery). |
| You pressed **Stop** and now nothing works | **Stop** is an emergency stop. Power-cycle the printer, or run `FIRMWARE_RESTART` from the console. See [Your first print](Printing). |
| Adaptive mesh not used, full bed meshed instead | The print covers more than 75 % of the bed, the file has no object labels, or the start G-code passes `BED_MESH_ADAPTIVE=0` or `BED_MESH_PROFILE=`. See [Print setup NebulaOS adds](Adaptive-Print-Setup). |
| A panel says "locked during print" | Expected: calibration, homing, extruding and similar actions are blocked while printing. See [Using NebulaScreen](Screen-Reference). |
| No mesh or purge line before the print | The slicer's start G-code does not call `START_PRINT`. See [Setting up your slicer](Slicer-Setup). |
| Filament will not feed | Cut a fresh clean end, and make sure it is in the throat before tapping **Load**. |
| Nothing comes out, motor clicking | Nozzle not hot enough, or a blockage. Raise the target and try again. |

---

## Updating

| Symptom | Fix |
|---|---|
| **Online** says the clock is not set | The printer sets its clock from the internet after Wi-Fi connects. Wait a minute and try again. |
| **Online** says it could not reach the release channel | No internet, or GitHub was not reachable. Check Wi-Fi; try again later. |
| A download fails with "does not match the release record" | The file arrived damaged. It was deleted; start the download again. |
| An update says "not possible while a print is active" | Expected: updates wait until the printer is idle (no print, heaters off). |
| The new system went back to the old one by itself | The new system did not start properly (trial start). The screen showed why; the old system runs as before. See [Recovery](Recovery#1-automatic-the-trial-start). |
| After updating Klipper or the NebulaOS extensions: *"Printer is halted"* with `nebulaos_compat: compatibility manifest declares 1 module(s) with no source file present ... extras/motor_database.cfg` - and a restart or even reinstalling does not help | The update failed its check, going back to the previous version failed too, and NebulaOS 1.0.2 fell back to its built-in copy of Klipper, which lacks that file. A lock holds the printer there on purpose until someone looks at it; it lives in `/usr/data/nebulaos`, so it survives restarts and reinstalls. Over SSH, `rm -f /usr/data/nebulaos/updates/locks/klipper-stack.lock && /etc/init.d/S05nebulaos-activate start` brings it back. Then please [report it](Report-A-Problem) with the logs. From **NebulaOS 1.0.3** the built-in copy is complete: the printer comes back on it by itself, and the lock still keeps further updates on hold until it is cleared. |
| Mainsail shows `file_manager: Error adding inotify watch to root 'config', path: .../config/backups/.settings-<time>-changed.part` | Harmless. NebulaOS's settings backup (every 30 minutes when your settings changed) renamed its temporary folder before Moonraker looked at it. The backup is fine and there is nothing to delete. To clear the message, restart Moonraker (`/etc/init.d/S56moonraker restart` over SSH) or the printer. It no longer appears from **NebulaOS 1.0.3**. |

---

## Screen and touch

| Symptom | Fix |
|---|---|
| Screen upside down | **Settings → Display → Rotate screen** (NebulaOS 1.0.3). See [Screen mounted the other way round](Screen-Display#screen-mounted-the-other-way-round). |
| Taps land in the wrong place, e.g. after turning the screen | Calibration belongs to one orientation. Rotate screen asks for a new one by itself; otherwise redo it: **Settings → Reset → Reset touch calibration**. |
| A popup covers the touch calibration, and tapping it goes to the calibration | Do not tap it. Over SSH run `rm /usr/data/nebulaos/nebulascreen/nebulascreen.json`, then `reboot`: popups appear only once, so the next start shows the calibration alone. Fixed in NebulaScreen v1.0.2 and NebulaOS 1.0.3. |
| Touch calibration came out wrong and you cannot reach the button | Edit `config/nebulascreen/nebulascreen.json` in Mainsail: set `"touch_calibrated": true` and remove `touch_calibration_coeff`, then restart the screen. The wizard runs again. See [Configuration](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/blob/main/wiki/Configuration.md). |
| Sensors shown with raw names like `Heater Bed` | None of the `id`s in `monitored_sensors` matches a Klipper object, so the screen shows every heater and sensor under its Klipper name. Fix the `id`s (an empty or missing list is replaced by Extruder, Bed and MCU Temp at start). See [Configuration](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/blob/main/wiki/Configuration.md). |
| Screen seems stuck | **Settings → System → Restart GUI**, or over SSH `/etc/init.d/S58nebulascreen restart`. |
| Settings do not stick after a reboot | Check that `config/nebulascreen/nebulascreen.json` exists and is valid JSON. A file that cannot be parsed is ignored and the built-in defaults are used. |

---

## Still stuck?

[Report a problem](Report-A-Problem): the screen raises the log level, saves the logs to a USB
stick and shows where to report it. Including those logs makes a report far more likely to be
solvable. If the printer does not start at all: [Recovery](Recovery).

Developer and simulator troubleshooting lives in the component wiki:
[NebulaScreen troubleshooting](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/blob/main/wiki/Troubleshooting.md).
