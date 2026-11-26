# Frequently asked questions

Short answers to the questions we get most. Each one links to the page with the details.
Not here? Ask on [Discord](https://discord.com/invite/k3HdqpdB) or see
[Troubleshooting](Troubleshooting).

## Before you start

**Will NebulaOS work on my printer?**
On the **Creality Ender-3 V3 KE**: yes, that is what it is made for. On the **Ender-3 V3 SE**
with a Nebula Pad: yes, as a community port - see [NebulaOS on the Ender-3 V3 SE](Ender-3-V3-SE).
Other printers (Ender-3 V3, V3 Plus, K1 ...): no.
[Check you have the right printer](What-NebulaOS-Is#check-you-have-the-right-printer).

**Can I go back to Creality's firmware?**
Yes. NebulaOS installs next to Creality's system, in the printer's other "slot", and you can
switch back from the screen. [Going back to stock](Going-Back).

**Which file do I download?**
It depends on what your printer runs now:

| Your printer now | File from the [latest release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest) |
|---|---|
| Creality's stock firmware on a KE | the one with `F005_ota_img` in its name |
| Already NebulaOS | none - *Settings → Updates → System image → Online* |
| A Nebula Pad bought separately | the one with `NebulaPad-NEBULA_ota_img` in its name |
| An Ender-3 V3 SE | see [the SE page](Ender-3-V3-SE) |

**Never rename the file.** Creality's updater only accepts it under its original name.
[Install NebulaOS](Installing-NebulaOS).

**Is it hard?**
Installing takes about 15 minutes with a USB stick. After that, plan an hour for the guided
first calibration and setting up your slicer. Every step is on the screen.
[New here? Start printing](Home#new-here-start-printing).

## Getting connected

**How do I open Mainsail (the web page)?**
Your printer's address is on the screen under **Settings → Connections**. Type it into a browser
on a computer or phone on the **same** Wi-Fi. [First start](First-Time-Setup).

**My Wi-Fi does not show up, or will not connect.**
The printer only uses **2.4 GHz** Wi-Fi. If your router has separate names for 2.4 and 5 GHz,
choose the 2.4 GHz one. [Troubleshooting → Connecting](Troubleshooting#connecting).

## Printing

**Do I have to change my slicer settings?**
Yes, once: two lines of start and end G-code. With OrcaSlicer, just import our profile and it
is done. [Set up your slicer](Slicer-Setup), [OrcaSlicer quickstart](Quickstart-OrcaSlicer).

**Which calibration do I do first?**
One guided run, **Tune → Calibration → Auto Calibration**, about 7 minutes.
[First calibration](First-Calibration). The rest only when you need it:
[Improve your prints](Improve-Your-Prints).

**The first layer is too high or too low.**
Adjust it live while the first layer prints, from the print screen.
[Your first print](Printing), [Improve your prints](Improve-Your-Prints).

**My bed seems hotter since NebulaOS 1.0.5.**
That is right: since 1.0.5 the bed temperature reads like on Creality's stock firmware, so a
60 °C target is about 3 °C warmer than on 1.0.4. If you raised your slicer's bed temperatures
for NebulaOS, lower them back. The highest bed target is now 111 °C, as on stock.
[The bed temperature reads like stock](Calibration-Explained#the-bed-temperature-reads-like-stock-nebulaos-105).

**My skew correction does nothing.**
Before 1.0.5 the values were never used (a bug). Update to 1.0.5, enter them once more and tap
**Apply & Save**. The page then says *Skew correction: on*.
[Skew Correction](Calibration-Explained#skew-correction).

## When something goes wrong

**The print stopped and the printer says there was a power loss, but the power never went off.**
The printer's touchscreen computer froze and restarted itself. Update to **NebulaOS 1.0.5**
(System image, not "Update all"). If it still happens, especially with a **camera** connected,
read [Powering the Nebula Pad](Nebula-Pad-Power-And-Freezes) and send us the logs.

**The power went off in the middle of a print. Can I continue?**
Usually yes. After switching on, the screen offers to **Resume**. The printer lifts the nozzle
out of the part, primes it at the side and then **waits for you** to remove the loose filament
before it continues. [Power-loss recovery](Power-Loss-Recovery).

**The screen is upside down.**
**Settings → Display → Rotate screen.** [Screen mounted the other way round](Screen-Display#screen-mounted-the-other-way-round).

**Taps land in the wrong place.**
Redo the touch calibration: **Settings → Reset → Reset touch calibration**.

**The camera colours look wrong.**
Since 1.0.5 NebulaOS sets the Nebula Camera's colours correctly by itself. Other settings:
[Camera](Camera).

**How do I report a problem?**
**Settings → System → Report a problem**: set the log level to **Debug**, make the problem happen
again, then **Save logs to USB** and attach the zip to a
[GitHub issue](https://github.com/NebulaOS-KE/NebulaOS/issues). [Report a problem](Report-A-Problem).

## Updates

**I tapped "Update all". Do I have the new NebulaOS now?**
No. **Update all** only updates the apps (Klipper, Mainsail, the screen app ...). A new NebulaOS
comes with **Settings → Updates → System image → Online**.
[Keeping NebulaOS updated](Updating-NebulaOS).

**Which version do I have?**
**Settings → System** shows the NebulaOS version.

**Do I lose my settings when I update?**
No. Settings, calibration, `printer.cfg`, your files and Wi-Fi are kept through every update.

**What if an update goes wrong?**
NebulaOS starts the new version on trial. If it does not come up properly, the printer goes back
to the previous version by itself. [Recovery](Recovery).

## Getting help

- **Discord:** [discord.com/invite/k3HdqpdB](https://discord.com/invite/k3HdqpdB) - questions,
  tips, other owners.
- **A bug or a problem:** [GitHub issues](https://github.com/NebulaOS-KE/NebulaOS/issues), with
  the logs from *Report a problem*.
- **Words you don't know:** [Words you will see](Glossary).
