# How NebulaOS works

NebulaOS is more than a new touchscreen interface for the **Creality Ender-3 V3 KE**. It is a
rebuilt Linux operating system, developed specifically for the printer's hardware.

A lot of the work happens where you cannot see it: inside the Linux kernel, hardware drivers,
memory management, and the services that keep Klipper running.

Here is what is different, and why it matters. The two system slots and how updates use them
have their own page: [Two system slots](Two-System-Slots).

## What is inside the KE

| | |
|---|---|
| Processor | Ingenic X2000, a MIPS chip. Not ARM, not x86 |
| Touchscreen | 480 x 272 pixels, resistive touch |
| Mainboard | Creality's own, with a separate microcontroller (GD32F303) driving the motors |
| Storage | Internal eMMC with **two system slots**, plus a shared data area |
| Network | 2.4 GHz Wi-Fi |

The 480 x 272 screen is small, which is why NebulaScreen's layout is dense - and why every
screenshot in this manual is that size.

---

## A newer Linux, built for the KE

The original Ender-3 V3 KE uses an older Linux 4.4 kernel. NebulaOS replaces it with
**Linux 6.6**, adapted for the printer's Ingenic X2000 processor.

The operating system is built with Buildroot rather than installing a general-purpose Linux
distribution. It contains the software and drivers this printer needs, without the overhead of
a desktop environment.

This also means NebulaOS controls the entire software stack, not just the applications running
on top of Creality's original firmware.

**Why it matters:** the kernel, hardware drivers and applications can be maintained and improved
together, rather than being limited by the original operating system.

## Scheduling — keeping important tasks on time

NebulaOS uses a Linux 6.6 kernel with **preemption** (`CONFIG_PREEMPT`): a time-sensitive task can
interrupt less important work instead of waiting for it to finish. Up to 1.0.1 it used the
**PREEMPT_RT** real-time variant; 1.0.2 went back to standard preemption, the usual setup for a
Klipper host.

NebulaOS also gives priority to critical hardware communication and timing tasks over background
activity. The link to the mainboard has the highest priority, the printer's Linux-side MCU
process runs at a real-time priority just below it, and ordinary background work sits below
both.

For example, the printer might be running Klipper, showing a live camera feed, updating the
touchscreen and talking over Wi-Fi at the same time.

The KE also has an **ADXL345 accelerometer wired to its Linux processor**, not to the mainboard.
Klipper reaches it through a second, Linux-side MCU process (`klipper_mcu`, Klipper's own
`MACH_LINUX` build, connected over a local socket) — which is why predictable scheduling matters
during Input Shaper calibration in particular.

**Why it matters:** the link to the mainboard and Klipper's Linux-side work stay ahead of the
camera, the screen and Wi-Fi when several things happen at once.

> **Does this make printing faster?** Not directly. The separate **GD32F303** microcontroller on
> the mainboard still handles precise stepper timing. The kernel's scheduling only affects the
> Linux side, not the accuracy of individual motor pulses.
>
> If you ever see the printer described as an `stm32f103xe`, that is not a mistake: the GD32F303
> is register-compatible with that STM32 part, and Klipper is built for it through its STM32
> port. The chip is a GD32F303.

## Hardware drivers made for this printer

Getting a newer Linux kernel to run on the KE needed more than changing a version number.

NebulaOS carries hardware-specific work for the printer's:

- touchscreen and touch controller
- display timing, framebuffer and backlight
- Wi-Fi and SDIO communication
- USB controller and camera support
- GPIO, PWM and other board-specific functions

Some of this is small and very specific. The buzzer is exposed as a standard kernel PWM channel
so Klipper can drive it. The console framebuffer uses deferred takeover so the boot picture is
not replaced by a blank console. The screen application maps the framebuffer without blanking
it, so the boot image stays on the glass until the first real frame is drawn over it, instead
of flashing black for about half a second.

**Why it matters:** the newer operating system can use the printer's existing hardware without
needing a replacement screen or control board.

## Memory management — making the most of limited RAM

The printer's board has **about 250 MB of RAM available to Linux**, and roughly **140 MB of that
is free once everything is running**. That is not much for Klipper, Moonraker, a touchscreen
interface, camera streaming and system services together.

NebulaOS has several safeguards for it.

**Compressed memory (zram)** gives a 128 MB compressed swap area in RAM, so less-used pages are
compressed rather than the system simply running out.

**A disk-backed swap file** adds another 128 MB of headroom — but only while heavier maintenance
work is running, such as seeding or updating applications. The rest of the time it is switched
off on purpose, because using it routinely meant writing to the eMMC on every boot for no gain.

NebulaOS also watches memory pressure and protects printer-critical processes more than optional
ones: Klipper and its Linux-side MCU process are **never** acted on, while background work such
as camera streaming and update jobs is treated as more expendable.

**Why it matters:** when memory runs low the system protects printing, instead of treating every
process as equally important.

## Wi-Fi, USB and camera

NebulaOS uses Linux's in-kernel `brcmfmac` Wi-Fi driver rather than the original out-of-tree
one, while keeping the firmware the wireless chip itself needs.

One fix is worth singling out: the printer now keeps a **stable Wi-Fi MAC address** across
restarts. The Wi-Fi data shipped with the board carries a placeholder address that mainline
`brcmfmac` recognises as a known-bad template - and when it sees it, it invents a random address
on **every boot**. That is a real, traceable cause of a printer whose IP address kept changing.
NebulaOS derives one stable address per device instead.

The camera is handled by its own streaming service, which can stop unnecessary work when nobody
is watching and pick it up again when someone is. USB has had kernel-level attention too,
including how the controller handles frequent interrupts.

**Why it matters:** more predictable networking and less pointless background work on hardware
that does not have much to spare. None of it adds capabilities the Wi-Fi chip does not have -
there is still no 5 GHz.

## Official Klipper, with NebulaOS extensions

NebulaOS runs **official upstream Klipper**, and does not modify any of Klipper's own files.

The printer-specific parts live in a separate
[NebulaOS Klipper extensions](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions)
repository and are composed in when the system starts: each module is **symlinked** into
Klipper's `extras/` directory and listed in that checkout's own private ignore list. Both
checkouts stay content-pristine, which is exactly what lets Moonraker's update manager keep
treating Klipper as an untouched repository.

**If you see `-dirty` after Klipper's version** (in `klippy.log`, for example): Klipper's files
are not modified. Klipper itself adds `-dirty` to its version whenever extra modules are present
in its extras folder, which is where NebulaOS's extensions are linked. Its log lists them as
*Untracked files*; a real change to Klipper would appear as *Modified files* instead.

Those extensions provide automatic Z-offset calibration, load-cell probing, the guided
calibration workflows, stepper-driver tuning and power-loss recovery.

The system also checks, at every Klipper start, that the Klipper it is running still provides
everything the extensions need, and refuses to start rather than fail in the middle of a print.
Klipper and the extensions are updated and rolled back **as a pair** - a printer must never run
new Klipper against old extensions, or the reverse.

**Why it matters:** upstream Klipper development stays available, without maintaining a separate
Klipper fork.

See [Calibration explained](Calibration-Explained) for what these features do day to day.

## Built-in safeguards and recovery

NebulaOS feeds the SoC's **hardware watchdog**, so a frozen printer resets itself instead of
hanging until you pull the power. The chip's timeout is 60 seconds and it is fed every 10. The
feeder deliberately runs at ordinary priority rather than a real-time one, so that it starves at
exactly the moment ordinary software starves - which is when you want the reset to happen.

From 1.0.2, a frozen system also explains itself. After 40 seconds without the watchdog being fed,
the kernel writes down what both processor cores and the waiting programs were doing, keeps it in
memory that survives the restart, and then restarts. A processor core that stops completely is
noticed by the other one within about 20 seconds. See
[After the printer restarted by itself](Report-A-Problem#after-the-printer-restarted-by-itself).

The printer never sleeps either: from 1.0.2 the link to the Wi-Fi chip and the USB devices (the
hub and the camera) stay awake when idle instead of powering down between uses. That costs a
fraction of a watt and removes a set of wake-up paths that are hard to get right.

*From `etc/udev/rules.d/60-nebulaos-no-sleep.rules` and `etc/sysctl.d/91-nebulaos-freeze.conf`,
firmware `eec579c`, and kernel `95d0321e`.*

The operating system itself is on a **read-only filesystem**. Your settings, calibration, G-code
files and other personal data live separately, on writable storage, which is why replacing the
operating system does not normally erase them.

### Two system slots (A/B)

The KE has two boot slots, each able to hold an operating system. A system update is written to
the slot that is **not** running - see [Two system slots](Two-System-Slots), which explains what
that means for the system you had before.

The printer then starts the new slot **on trial**. If it does not confirm itself as healthy
within **5 minutes**, or fails to confirm across **3 restarts**, NebulaOS goes back to the
previous slot by itself.

This covers many failed updates. It cannot cover every possible boot failure: the part that
chooses a slot at power-on is Creality's own bootloader, which NebulaOS does not replace and
which has no fallback of its own. For the rest there is [Recovery](Recovery), including USB
recovery.

**Why it matters:** updating the operating system is less risky, and there is a way back when
something goes wrong.

## System updates and app updates are separate

NebulaOS does not need a whole operating system replacement every time Klipper or another
application changes.

| System image | App updates |
|---|---|
| Linux kernel, drivers and base operating system | Klipper, Moonraker, Mainsail, the NebulaOS extensions and NebulaScreen |
| Uses the A/B boot slots | Managed through Moonraker's update manager and the components' own releases |
| Restarts the printer into the other slot | Restarts only the affected services |

Updates are refused while the printer is busy with something that must not be interrupted.

The printer also installs **prebuilt Python packages** made for its MIPS processor, from the
project's own index, so Klipper and Moonraker can update themselves without a compiler on the
printer - and without reaching out to PyPI, which has never heard of this combination of CPU,
C library and floating-point ABI.

See [Updating NebulaOS](Updating-NebulaOS).

## Open development, from kernel to touchscreen

NebulaOS is developed in public repositories. The kernel, the operating system build, the
Klipper extensions, the touchscreen application and the update tooling can all be read.

Each system image records the exact source revision of every component it was built from.
Releases carry checksums and build information, and are built twice on separate machines with
the two results required to be byte-identical.

NebulaOS does **not** replace every binary in the printer. Creality's boot components stay as
they are - the SPL and U-Boot, the partition table, the per-SoC firmware and memory
descriptors - and so does the small loader on the mainboard. It is a new operating system on
the printer's existing foundations, not a from-scratch replacement of the whole machine.

The main components are:

- [NebulaOS](https://github.com/NebulaOS-KE/NebulaOS) — releases and downloads
- [NebulaOS-firmware](https://github.com/NebulaOS-KE/NebulaOS-firmware) — the complete operating system build
- [NebulaOS-kernel](https://github.com/NebulaOS-KE/NebulaOS-kernel) — Linux kernel and hardware support
- [NebulaOS-klipper-extensions](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions) — printer-specific Klipper functionality
- [NebulaOS-nebulascreen](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen) — the touchscreen application
- [NebulaOS-klipper-mcu](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu) — the mainboard firmware

Builds and developer internals are documented in those repositories, not in this manual.

## What does all this mean for your prints?

Most of this is not something you will meet as a new button or setting.

It is about building a stronger foundation underneath Klipper: predictable scheduling, better
use of limited memory, drivers that fit this hardware, and software maintenance you can undo.

It does not remove the printer's physical limits, and it does not by itself make printing faster
or parts better.

**The goal is straightforward: make better use of the hardware the Ender-3 V3 KE already has,
while keeping the software open, maintainable and recoverable.**
