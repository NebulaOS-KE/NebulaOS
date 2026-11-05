# Two system slots

## What this page will help you do

Understand the one rule that decides what happens to your old system, what a NebulaOS update
overwrites, and how to get back to Creality. Most questions about "will this replace my
firmware" have the same answer, and it is this page.

## The one rule

The Ender-3 V3 KE has **two system slots** on its internal storage. One is running; the other
is not. And:

> **Installing a system image always writes the slot that is _not_ running.**

That is true of NebulaOS's installer, and it is true of Creality's own updater - it is how the
printer was designed, not something NebulaOS added. Everything below follows from it.

The printer always starts one slot or the other. A marker on the storage says which, and both
systems can change that marker.

## What happens, in order

**Before you start.** One slot holds the system you bought the printer with - Creality's, or
OpenKE if you installed that. The other is empty or holds an old copy.

```
          slot 1                      slot 2
   ┌────────────────────┐      ┌────────────────────┐
   │ Creality  ◀running │      │ (empty / old)      │
   └────────────────────┘      └────────────────────┘
```

**1. You install NebulaOS.** You run Creality's own updater on the NebulaOS `.img`, from the
stock touchscreen or over SSH. It writes the slot that is not running - slot 2 - and the
printer starts it.

```
   ┌────────────────────┐      ┌────────────────────┐
   │ Creality           │      │ NebulaOS  ◀running │
   └────────────────────┘      └────────────────────┘
```

**Your old system is untouched.** *Settings → Reset → Swap boot slot* starts it again, as you
left it.

**2. You update NebulaOS with a new system image.** Same rule: it writes the slot that is not
running - which is now the one holding your old system.

```
   ┌────────────────────┐      ┌────────────────────┐
   │ NebulaOS (new) ◀run│      │ NebulaOS (previous)│
   └────────────────────┘      └────────────────────┘
```

**This is the step that removes Creality's system.** After it, *Swap boot slot* moves between
two NebulaOS versions. That is also what gives you the automatic way back from a bad update -
the previous NebulaOS is right there - but it is a real trade and it is worth knowing before
you take the first update rather than after.

**You can see it coming.** *Settings → Updates → System image* lists both slots with what each
one holds and which is running, before you confirm.

**If an install stops, nothing changed on the system you are running. Just install again.**
An install can stop by itself - for example when a print starts while it is writing. The
other slot was already being written by then, so it is cleared: **until an install completes,
you cannot switch back to the system that was in the other slot.**

## If you want to keep Creality's system

Nothing stops you taking NebulaOS updates and losing stock; most people will. If you would
rather keep it:

**Run the update while Creality's system is the one running.** The rule does the rest: the slot
that is not running is then the NebulaOS one, so that is what gets overwritten and stock stays
put. In practice this means swapping to stock, installing the NebulaOS `.img` with Creality's
own updater there, and swapping back.

That needs a way to run the updater on the stock side - its touchscreen, or SSH if your stock
side is OpenKE. **Creality's stock firmware does not normally give you SSH**, and NebulaOS does
not change its password.

## Most things update without touching a slot at all

A system image is only needed for **OS-level** parts: the kernel, drivers, Wi-Fi, the
touchscreen stack, SSH.

Everything else updates on its own, through Moonraker's update manager, with no image and no
slot written:

| Component | How it updates |
|---|---|
| Klipper | Moonraker's update manager |
| Moonraker | Moonraker's update manager |
| Mainsail | Moonraker's update manager (`type: web`, channel `stable`, from `mainsail-crew/mainsail`) |
| NebulaOS Klipper extensions | Moonraker's update manager |
| NebulaScreen | its own releases |

So a NebulaOS image that ships Mainsail **2.18.2** is not stuck on 2.18.2 - Mainsail updates
itself from its own repository. See [Updating NebulaOS](Updating-NebulaOS).

## Could a Creality update overwrite NebulaOS?

Yes, by the same rule, if you ran one from the stock side: Creality's updater would write the
slot that is not running, which would be the NebulaOS one.

## Getting back to Creality

| What you want | How |
|---|---|
| Your old system is still in the other slot | *Settings → Reset → Swap boot slot* |
| It is gone, and you want Creality back | Install Creality's official `.img` from **Settings → Updates → System image**. NebulaOS's installer reads the kernel inside an image and recognises Creality's; it goes into the slot you are not running |
| Neither works | [Recovery](Recovery) - a `.ingenic` file over micro-USB rewrites the printer completely, and erases everything |

And the other direction - you are on stock and want NebulaOS back, without reinstalling it:

Over SSH **on the stock side**, Creality's own built-in switcher flips which slot starts next:

```sh
sh -c '. /etc/ota_bin/ota_local_method.sh; local_set_next_boot_device'
```

It toggles rather than taking a target: it flips to whichever system you are not on. Then
`reboot`. Nothing is reinstalled, so nothing is recalibrated - your configuration and
calibration live on a shared data area that neither slot overwrites.

From the NebulaOS side the matching command is
`sh -c '. /etc/ota_marker.sh; write_ota_marker "ota:kernel"'` for slot 1, or `ota:kernel2` for
slot 2 - but from NebulaOS you would normally just use *Swap boot slot* on the screen.

## What survives all of this

Your `printer.cfg`, macros, calibration, print files, Wi-Fi networks and screen settings live on
a **shared data area** that is not part of either slot. Swapping slots does not touch them, and
installing an image does not touch them. That is why coming back to NebulaOS does not mean
calibrating again.

A NebulaOS update does replace its own copies of Klipper, Moonraker, Mainsail and the
extensions when the image expects newer ones, and takes a backup first, under
`/usr/data/nebulaos/system/migration-backups/`. **Your configuration is not part of that** - it
is not replaced, so it does not need restoring.

The one thing that does erase settings is a
[clean NebulaOS reset](Resetting), and it says so before it runs.

## Next step

[Installing NebulaOS](Installing-NebulaOS).

## Related

- [Installing NebulaOS](Installing-NebulaOS)
- [Updating NebulaOS](Updating-NebulaOS)
- [Going back to your old firmware](Going-Back)
- [Recovery](Recovery) - when the printer will not start
