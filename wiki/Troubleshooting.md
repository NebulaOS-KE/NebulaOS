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

---

## Screen and touch

| Symptom | Fix |
|---|---|
| Screen upside down or rotated | Set `display_rotate` to `2` in `nebulascreen.json` (the KE default). See [Configuration](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/blob/main/wiki/Configuration.md). |
| Taps land in the wrong place, e.g. after changing `display_rotate` | Calibration is rotation-specific. Redo it: **Settings → Reset → Reset touch calibration**. |
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
