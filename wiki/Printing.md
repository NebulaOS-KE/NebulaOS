# Printing

## What this guide will help you do

Start a print, watch it, adjust it while it runs, and stop it safely.

## What you need

- A calibrated printer - [First-time setup](First-Time-Setup).
- Filament loaded - [Filament](Filament).
- A sliced `.gcode` file.

## Before you begin

**Learn the difference between Cancel and Stop before you need it.** They sit next to each
other and they are not alternatives:

| Button | What it does | When to use it |
|---|---|---|
| **Pause** | Parks the toolhead and **holds temperatures**. **Resume** carries on. | A filament change, or a look at something |
| **Cancel** | Ends the print tidily. Asks you to confirm. | You have changed your mind |
| **Stop** | **Emergency stop.** Cuts all movement and all heaters instantly. | Something is going physically wrong |

**Stop needs a power-cycle or a firmware restart afterwards** before the printer will do
anything again. Its label is only "Stop", not "Emergency Stop", so it is easy to press
expecting a gentler Cancel. Use **Cancel** unless something is actually wrong.

## Getting a file onto the printer

Three ways, all equivalent:

- **Mainsail** - drag the file into the file list in your browser. Easiest from a computer.
- **USB stick** - plug it in; the printer's file browser reads it directly.
- **Your slicer** - if it can upload to Moonraker, point it at the printer's address.

## Starting a print

1. On the screen, open the **Files** tab (or **Home → Files**).
2. Find your file. Files on a USB stick appear alongside the ones stored on the printer.
3. Tap it, then confirm.

![The file browser](images/m09-files.png)

The printer heats up, may run a bed soak and a purge line, and begins.

### What happens before the first layer

Depending on your configuration, NebulaOS may probe only the area the print actually covers
rather than the whole bed, and may purge next to the print instead of on it. Both are normal
and both save time.

## Watching a print

The print status screen appears by itself the moment a print starts, whatever you were looking
at.

![The print status screen during a print](images/m60-print-status.png)

On the left: the thumbnail, the file name and a progress bar. On the right, ten readouts:

| | |
|---|---|
| **Extruder** temperature, current or `current / target` | **Bed** temperature, same format |
| **Chamber** temperature - always shown here | **Speed** in mm/s |
| **Z-offset** - tap it to adjust live | **Flow** in mm³/s |
| **Layers**, as `current / total` | **Elapsed** time |
| **Fan speed** | **Time left**, an estimate |

If you navigate back to the **Home** tab mid-print, a compact progress widget replaces the
usual buttons there - tap it to return to the full screen. That shortcut is only on the Home
tab.

## Fixing the first layer while it prints

This is the single most useful thing on this screen, and it is meant to be used.

Tap the **Z-offset** readout to get step buttons: ±0.001, ±0.005, ±0.01, ±0.025 and ±0.05 mm.
Watch the first layer and nudge:

| What you see | What to do |
|---|---|
| Lines not fusing, gaps between them | Nozzle too high - press **−** |
| Lines translucent or completely flat | Nozzle too low - press **+** |
| Lines squished together and fused, no gaps | Correct - leave it |

Move in small steps and give the printer a few seconds to show the result.

![The Z offset screen](images/m16-zoffset-saved.png)

## Adjusting speed, flow and pressure advance

**Tune → Fine Tune**, or the **Fine Tune** button on the print status screen.

![The Fine Tune panel during a print](images/m61-finetune-printing.png)

Speed and flow here are **percentages** of what the file asked for. The flow figure on the
print status screen is a different thing - a volumetric rate in mm³/s.

Pressure advance can also be adjusted live from Fine Tune. It is not shown on the print status
screen.

## Temperatures and fans

From the **Home** tab:

- **Tap any temperature** to set a target. A numpad opens - type the exact value. The reading
  shows `current / target`, so `45 / 210` means 45 °C now, heating toward 210.
- **Tap the target** to clear it and cool down.
- There are **no material presets** - no PLA or PETG buttons. Type the number.
- Chamber and MCU readings are display-only.
- **Fans** opens the fan controls. Fans the printer manages itself are shown read-only.

## Cancelling one object out of several

If your file was sliced with object labels, the **Objects** button on the print status screen
lets you cancel a single object while the rest carries on - useful when one part of a plate
has failed.

Cancelling the last remaining object asks whether you meant to cancel the whole print.

## When the print finishes

The printer stops heating and the status screen shows the print as complete. Let the bed cool
before removing the part - parts release far more easily cool, and a warm bed with a stuck
part invites force you will regret.

The job is added to the printer's record. **Settings → Printer → Statistics** shows the last
four prints with their result and print time, along with the totals for the printer's whole
life - see [Statistics](Screen-Reference#statistics-panel). The full list, with filament use
and thumbnails, is Mainsail's **History** page
([Opening Mainsail](Opening-Mainsail)).

## Troubleshooting

| What happens | What to do |
|---|---|
| The print will not start | Check the printer is not already busy, and that the file sliced correctly. |
| First layer is poor | Adjust Z offset live, as above. If one side is consistently worse, you need [Axis Twist](Calibration-Explained). |
| The print stops partway | Check for filament runout. After a power cut, see [Power-loss recovery](Power-Loss-Recovery). |
| You pressed Stop | Power-cycle the printer, or run `FIRMWARE_RESTART` from the console. |
| Time remaining looks wrong | It is an estimate, and it improves as the print proceeds. |
| The part will not come off | Let the bed cool completely first. |

## Recovery and reversal

- **Pause** is fully reversible with **Resume**.
- **Cancel** ends the print; the file stays, so you can start again.
- **Stop** requires a power-cycle or `FIRMWARE_RESTART`.
- A power cut may be recoverable - [Power-loss recovery](Power-Loss-Recovery).

## Related

- [Filament](Filament)
- [Calibration guide](Calibration-Guide)
- [Power-loss recovery](Power-Loss-Recovery)
