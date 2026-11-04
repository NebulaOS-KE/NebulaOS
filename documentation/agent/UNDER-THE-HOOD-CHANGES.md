# What changed in Tim's "Under the hood" mockup, and why

**Date:** 2026-11-04
**Mockup:** `_scratch/docs-agent/inbox/2026-11-04-under-the-hood-mockup.md` (verbatim, unverified)
**Checked against:** firmware `ba98eec` (tag `v1.0.0`), the NebulaOS kernel `openke`, the MCU
repository, and `manifests/dependencies.conf`. Read-only; component worktrees stay removed.

Tim's structure, headings, tone and "Why it matters" pattern are kept throughout. Most of the
mockup was accurate. Below is every place the page differs from it.

## Corrected — the claim was wrong

### "about 200 MB of usable RAM" → about 250 MB, ~140 MB free in use

Two different numbers were being conflated. Linux is given roughly **248 MB**; what is actually
**free once everything is running is about 140 MB**. "200 MB of usable RAM" matches neither, and
the gap matters because the memory-pressure section only makes sense against the free figure.
The page now gives both.

### The display: "synchronise frame updates with the screen's refresh timing"

**Could not be verified and is not claimed.** Nothing in the kernel's `openke` history is a
vsync or tear-free change. What is there, and what the page says instead, is specific and
checkable: the console framebuffer uses deferred takeover so the boot image is not wiped, and
the screen application maps the framebuffer without blanking it so the boot picture stays until
the first real frame replaces it - which is what removes the half-second of black.

If there is a vsync change, it is somewhere this check did not reach; it should not go back on
the page without a source.

## Sharpened — right, but vaguer than the source

### "a separate disk-backed swap file ... during heavier maintenance operations"

Correct, and the page now says the part that surprises people: **it is off the rest of the
time**, deliberately. Turning it on every boot meant eMMC writes for no benefit. Sizes added:
128 MB zram, 128 MB disk.

### "without modifying Klipper's core host files"

True, and weaker than what the code guarantees. The modules are **symlinked** into Klipper's
`extras/` and listed in that checkout's private ignore list, so both checkouts stay
content-pristine - which is the reason Moonraker's update manager still sees an untouched
repository. The page explains the mechanism rather than asserting the outcome.

### "rollback handling if validation fails"

Correct and now specific: Klipper and the extensions are updated and rolled back **as a pair**,
because a printer must never run new Klipper against old extensions or the reverse. Also added:
the compatibility check runs at **every Klipper start**, and refuses to start rather than fail
mid-print.

### The watchdog

Correct. Added the numbers (60 s hardware timeout, fed every 10 s) and the non-obvious design
point: the feeder runs at **ordinary** priority on purpose, so that it starves exactly when
ordinary software starves - which is when the reset is wanted.

### The trial boot and automatic switch-back

Correct, and the conditions were missing: **5 minutes** to confirm, or **3 restarts** without
confirming. Also made the limit concrete - the thing that picks a slot at power-on is Creality's
bootloader, which NebulaOS does not replace and which has no fallback of its own. That is *why*
it "cannot recover automatically from every possible boot failure".

### "prebuilt software packages tailored to its MIPS hardware"

Correct. Added the reason it exists: PyPI has never heard of this combination of CPU, C library
and floating-point ABI, so the printer installs from the project's own index and never reaches
out to PyPI.

### "NebulaOS still relies on ... Creality boot components"

Correct, and now named: the SPL and U-Boot, the partition table, the per-SoC firmware and memory
descriptors, plus the small loader on the mainboard.

## Added — a question the mockup invites

### GD32F303 vs `stm32f103xe`

The mockup names the GD32F303, correctly. But a user who looks will see the printer report an
`stm32f103xe`, and conclude the documentation is wrong. The page now says why: the GD32F303 is
register-compatible with that STM32 part and Klipper builds for it through its STM32 port.

## Confirmed as written

- **Linux 6.6 on the Ingenic X2000, built with Buildroot** rather than a general-purpose distro.
- **PREEMPT_RT**, and "the actual improvement has not been quantified" - kept, because it is
  true and because it is the honest sentence in the section.
- **The ADXL345 is wired to the Linux processor**, and Klipper reaches it through a Linux-side
  MCU process. Exactly right; the page adds that this is Klipper's own `MACH_LINUX` build over a
  local socket.
- **`brcmfmac` in place of the out-of-tree driver**, keeping the chip's own firmware.
- **The stable Wi-Fi MAC fix**, including the cause - the shipped Wi-Fi data carries a
  placeholder address that mainline `brcmfmac` recognises as a known-bad template and replaces
  with a random one on every boot.
- **The camera service idling when nobody is watching**, and the USB interrupt work.
- **Read-only operating system, separate writable storage.**
- **Two update types, A/B for the image, update manager for the apps.**
- **Reproducible builds and recorded source revisions** - added that releases are built twice on
  separate machines and must match byte for byte.
- **No 5 GHz**, and the closing "this does not make your prints faster" framing.

## One discrepancy to resolve on hardware

The main session reported that `klippy.log`'s git information shows **`-dirty`**, with the
extension files linked in as untracked.

**The source says that should not happen.** `nebulaos-klipper-compose.sh` states the mechanism's
purpose outright - `git status --porcelain` empty, `git describe --dirty` with no `-dirty` - and
writes the ignore entries **before** the symlinks they cover, specifically so the checkout is
never dirty, "not even transiently".

So either the observation is from an older build, or something regressed, or the `-dirty` comes
from a different repository than the one assumed. This page therefore describes the **mechanism**
and makes no claim about what the version string shows. Worth one look at a real `klippy.log`;
if it really is dirty on a 1.0.0 printer, that is a firmware bug rather than a documentation
one.

## Scope

Everything above is read from source. **No claim on this page was verified on a printer by this
agent**, and the page states nothing about what has been tested, per decision D-011.
