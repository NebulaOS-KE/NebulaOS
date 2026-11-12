# Thank you

NebulaOS is built on other people's work. Some of it we use as it is, some we changed, some we
ported, and some only showed us how something works. This page tries to name all of them - not
only the famous projects, but also the people whose driver, macro, protocol notes or recovery tool
quietly made this possible.

The list is built from our own source code: every name here appears in a file header, a commit, a
pinned dependency or our own research notes. If we used your work and you are missing, or
something here is wrong, please [open an issue](https://github.com/NebulaOS-KE/NebulaOS/issues) and
we will fix it.

## The foundations

- **[Klipper](https://github.com/Klipper3d/klipper)** - Kevin O'Connor and every Klipper
  contributor. NebulaOS runs official, unmodified Klipper on the printer, and builds the mainboard
  firmware from the same Klipper with one small patch for the KE's chip.
- **[Moonraker](https://github.com/Arksine/moonraker)** - Eric Callahan (Arksine) and contributors:
  the printer's API, which the screen, Mainsail and your slicer all talk to.
- **[Mainsail](https://github.com/mainsail-crew/mainsail)** - the mainsail-crew: the web interface.
  The screen's print time estimates are also ported from Mainsail's own calculations.
- **[Buildroot](https://buildroot.org/)** - the system NebulaOS is built with, and every open-source
  package it brings: nginx, FFmpeg and x264 (timelapse videos), Python, dropbear (SSH),
  wpa_supplicant (Wi-Fi), git and many more.
- **[Linux](https://kernel.org/)** - and the stable and real-time kernel maintainers.

## The people who really made this happen

- **[Jason Pell (pellcorp)](https://github.com/pellcorp)** - more than anyone else's. His
  [SimpleAF](https://github.com/pellcorp/creality) project is where our print start, end, pause,
  filament and homing macros and our cleanup design come from; his
  [k1-ustreamer](https://github.com/pellcorp/k1-ustreamer) build is our camera;
  [creality-firmware](https://github.com/pellcorp/creality-firmware) showed how to replace the boot
  logo; his Klipper fork was where NebulaOS's Klipper extensions started; and his research on the
  install package and on emulating these boards saved us from dead ends.
- **[ballaswag](https://github.com/ballaswag)** - [GuppyScreen](https://github.com/ballaswag/guppyscreen),
  the touchscreen app NebulaScreen grew from (thousands of its lines are still in it), the
  input-shaper save and TMC status Klipper modules, and
  [ingenic-usbboot](https://github.com/ballaswag/ingenic-usbboot), the USB recovery tool that makes
  it possible to rescue a printer that will not start.
- **[Llixuma](https://github.com/Llixuma/ingenic-linux-kernel6.6-x2000-v1.0-20250221)** - published
  Ingenic's Linux 6.6 SDK for the X2000 chip. Our whole kernel started from it.
- **[Gareth Farrington (garethky)](https://github.com/garethky)** - Klipper's load-cell support.
  NebulaOS's nozzle-touch Z offset and probing are built directly on it.
- **[CryoZ](https://github.com/pellcorp/creality/blob/main/k1/mcu_util.py)** - worked out the
  protocol of Creality's mainboard bootloader. Our mainboard firmware installer speaks it.
- **[OpenKlipperEdition](https://github.com/OpenKlipperEdition/Recovery)** - their Recovery
  project's image builder is the model for our `.ingenic` recovery image, and its template comes
  from there.
- **[Icenowy Zheng](https://github.com/icenowy)** - wrote the Linux driver for the NS2009 touch
  controller. Every touch on the screen goes through it.

## Kernel and hardware

- **Ingenic Semiconductor** - the X2000 SDK: board support, the display driver and the board's
  device tree.
- **Kernel fixes we took early** from the Linux stable trees, with thanks to their authors:
  Minas Harutyunyan (USB host, the camera's connection), Thomas Gleixner (real-time locking),
  Benoit Sevens (USB video), Kairui Song (swap), and Greg Kroah-Hartman and Sasha Levin, who
  carried them into the stable kernels.
- **[Infineon](https://github.com/Infineon/ifx-linux-firmware)** - the firmware for the Wi-Fi
  chip.
- **[wireless-regdb](https://git.kernel.org/pub/scm/linux/kernel/git/wens/wireless-regdb.git/)** -
  the Wi-Fi rules for every country.
- **[Bootlin](https://toolchains.bootlin.com)** and **[Arm](https://developer.arm.com)** - the
  compilers that build the screen app and the mainboard firmware.
- **Creality** - the printer, and the stock firmware we studied to get the display timings, the
  Wi-Fi settings and the recovery image right.

## Printing, calibration and macros

- **[kyleisah - KAMP](https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging)** - the purge
  line next to the print and the smart park (`_KAMP_Settings` still carries its name).
- **[Andrew McGregor and contributors - klipper_tmc_autotune](https://github.com/andrewmcgr/klipper_tmc_autotune)** -
  TMC motor autotune and its motor database, including the KE's motors.
- **Alex Zellner - [fluidd-config](https://github.com/fluidd-core/fluidd-config)** - the pause,
  resume and cancel macros.
- **"Zero"** - the bed-warp soak macro, as credited in SimpleAF.
- **The "Ellis" convention** - the way the heat-and-wait commands work, as named in SimpleAF.
- **[Pedro Lamas](https://github.com/pedrolamas)** - `virtual_pins`, which the bed soak uses.
- **Eric Callahan** - `gcode_shell_command`, which lets macros run system commands.
- **Klipper module authors** whose work our calibration menu sits on: Dmitry Butyugin (input
  shaper), Jeremy Tan (axis twist compensation), Rui Caridade and Matthew Lloyd (bed tramming),
  Florian Heilmann (safe Z homing), Len Trigg (firmware retraction), Alec Plumb (`RESPOND`), and
  the Marlin project, whose skew correction Klipper's is ported from.
- **[moonraker-timelapse](https://github.com/mainsail-crew/moonraker-timelapse)** - the
  mainsail-crew's timelapse.
- **[kageurufu - preprocess_cancellation](https://github.com/kageurufu/cancelobject-preprocessor)** -
  cancelling single objects in files sliced without object labels.
- **[KIAUH](https://github.com/dw-0/kiauh)** - the web server setup we started from.
- **[Guilouz - Creality Helper Script](https://github.com/Guilouz/Creality-Helper-Script)** - its
  Z offset saving was the idea behind ours.

## The touchscreen app

NebulaScreen grew from [GuppyScreen](https://github.com/ballaswag/guppyscreen) (ballaswag, see
above). Code from these people is still in it today:

- **[Praise Obielodan (probielodan)](https://github.com/probielodan/guppyscreen)** - the KE-focused
  rework of GuppyScreen: homing, print status, files and sensors.
- **[Preston Brown](https://github.com/prestonbrown/guppyscreen)** - the interactive 3D bed mesh.
- **kevdliu** (power devices), **consp** (Klipper prompts), **Tristan** (Wi-Fi), **ajs123** (Z icons)
  and **Lars** - GuppyScreen contributors whose code survives, and **Jason Pell**'s fixes to it.
- **Ideas from** [KlipperScreen](https://github.com/KlipperScreen/KlipperScreen),
  [Fluidd](https://github.com/fluidd-core/fluidd) and Frix-x's
  [Klippain Shake&Tune](https://github.com/Frix-x/klippain-shaketune), which GuppyScreen credited.

Libraries and art inside it:

- **[LVGL](https://github.com/lvgl/lvgl)** and **lv_drivers** - the graphics library everything is
  drawn with.
- **[libhv](https://github.com/ithewei/libhv)** (ithewei) - the connection to Moonraker, with the
  libraries it brings: **[nlohmann/json](https://github.com/nlohmann/json)** (Niels Lohmann),
  http_parser (Joyent and Node.js contributors), multipart_parser (Igor Afonov) and SHA-1 (Steve Reid).
- **[spdlog](https://github.com/gabime/spdlog)** (Gabi Melman) and **[{fmt}](https://github.com/fmtlib/fmt)**
  (Victor Zverovich) - logging.
- **[cpp-subprocess](https://github.com/arun11299/cpp-subprocess)** (Arun Muralidharan).
- **[Material Design Icons](https://pictogrammers.com/library/mdi/)** (Pictogrammers) - most of the
  icons.
- **Montserrat** (Julieta Ulanovsky and contributors), **Font Awesome** symbols and **DejaVu Sans
  Mono** - the fonts.
- **[DylanUnofficial](https://www.printables.com/model/1770386)** - a screen mount design.

## Camera

- **[µStreamer](https://github.com/pikvm/ustreamer)** - Maxim Devaev and PiKVM: the camera stream,
  built from Jason Pell's K1 version.
- **The Independent JPEG Group**, **libevent**, **libmd** and **libbsd** - built into it.
- **[v4l-utils](https://git.linuxtv.org/v4l-utils.git)** - the LinuxTV project: camera controls.

## Research we learned from

No code from these, but they answered questions we could not have answered alone:

- **[Jubian540](https://github.com/Jubian540/x2000_kernel)**, **[bakueikozo](https://github.com/bakueikozo/atomkernel4)**,
  **[Ingenic-community](https://github.com/Ingenic-community/linux)** and
  **[lone0](https://github.com/lone0/buildroot-x2000)** - their X2000 kernel and Buildroot trees
  showed us what the KE runs and where to start.
- **[zerg32](https://github.com/zerg32/k1-firmware-scripts)** - showed that recovery images need no
  signature.
- **[pellcorp/k1-qemu](https://github.com/pellcorp/k1-qemu)** - showed that emulating the board is a
  dead end, before we spent time on it.
- **Creality's open-source releases** of their Klipper - to understand the stock printer.

---

The licences of everything NebulaOS ships are in each repository's `LICENSES` folder and in the
file headers. This page is a thank-you, not a licence.
