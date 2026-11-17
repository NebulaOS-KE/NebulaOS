# Other printers (community boards)

NebulaOS is made for the **Creality Ender-3 V3 KE**. Underneath it runs ordinary upstream Klipper,
so other printers of the **Ender-3 V3 family** can run it too, on a **Nebula Pad** connected to
their mainboard. We call these **community boards**.

> **Community boards are not supported by NebulaOS.** They're built from published, working
> recipes so you can try them easily. There is no guarantee and no support. If you get one
> working, or find something wrong in a recipe, tell us so everyone else gets the fix.

## The boards

| Printer | Mainboard chip | Status | Everything you need |
|---|---|---|---|
| Ender-3 V3 SE | **GD32F303** (every C13 board, some C14) | **Community proven** | [`community/ender-3-v3-se`](https://github.com/NebulaOS-KE/NebulaOS/tree/main/community/ender-3-v3-se) |
| Ender-3 V3 SE | **STM32F401** (some C14) | **Untested with NebulaOS** - first testers wanted | [`community/ender-3-v3-se`](https://github.com/NebulaOS-KE/NebulaOS/tree/main/community/ender-3-v3-se) |

**Community proven** means: people run NebulaOS on it every day and told us. **Untested** means:
built from a recipe that works with another Nebula Pad system, but nobody has told us yet that it
works with NebulaOS.

Each board's folder has a step-by-step how-to, the printer configuration, a slicer profile, a
test list and where every setting comes from. The ready-made mainboard firmwares are in every
[NebulaOS release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest), built from the
Klipper that release runs.

## C13 or C14: look at the chip

The Ender-3 V3 SE was sold with **two different mainboard chips**, and each needs its own
firmware. The wrong one can brick the board.

- **C13** on the board: the chip is a **GD32F303**.
- **C14** on the board: it can be **either** a **GD32F303** **or** an **STM32F401** - the same
  board name exists with both. **Look at the large square chip** and use the firmware for what it
  says.

## In short

How it goes on an Ender-3 V3 SE (the [folder's how-to](https://github.com/NebulaOS-KE/NebulaOS/tree/main/community/ender-3-v3-se)
has every detail):

1. **Find your chip** (above).
2. **NebulaOS on the pad:** a Nebula Pad bought separately takes
   `NebulaOS-NebulaPad-NEBULA_ota_img_V9.<version>.img` from the
   [latest release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest) (from NebulaOS 1.0.4),
   on a USB stick, not renamed. A pad that has Creality's KE software takes the `F005` file.
3. **Mainboard firmware:** the file for your chip from the same release, on the SD card - top level for GD32F303, folder
   `STM32F4_UPDATE` for STM32F401 - with a new short name.
4. **Printer configuration:** two files into Mainsail, one include block in `printer.cfg`. The
   same for both chips.
5. **Test** in the order of the folder's test list, before homing or printing.

## Never use the KE's firmware tools on another board

- **Settings → Printer → MCU firmware** and **Reinstall NebulaOS firmware** are for the KE only.
  They check for the KE's special image format and must not be used for any other board.
- Flash a community board **the way it is normally flashed**: an SD card in the mainboard.
- At every start NebulaOS checks which mainboard firmware is running. On another board it does not
  recognise it, and lets Klipper start. It **never** writes firmware to a board it does not
  recognise as a KE.

## Tell us

- [**It works on my printer**](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-works.yml) -
  a few clicks. Two of these move a board to *community proven*.
- [**I found a fix**](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-fix.yml) -
  what was wrong and what you changed, in your own words.

Both need a free GitHub account. No logs needed.

## Your printer is not listed

Only the Ender-3 V3 family is covered here. The Ender-3 V3 and V3 Plus are a different design
and are not covered.

If you have an Ender-3 V3 family printer with a mainboard that is not listed and want to try:

- The firmware has to be built from the **same Klipper as NebulaOS runs**:
  `58bd67db3ce1be1951c3e4a6d1156a79903d4edc`.
- It has to talk to the Nebula Pad on the **display cable's serial port** at **230400** baud. On
  the SE boards that is USART2 (PA3/PA2). Guides written for a Raspberry Pi on USB use **USART1**:
  that firmware flashes fine but cannot talk to a Nebula Pad.
- Do **not** copy the KE's settings: the KE needs a special header no other board has.
- The SE recipes in
  [NebulaOS-klipper-mcu](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/tree/main/community)
  show what a complete recipe looks like. A recipe added there is built into every NebulaOS
  release from then on.

Got one working? Use [I found a fix](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-fix.yml)
and tell us what you did - then it can become a community board for everyone.
