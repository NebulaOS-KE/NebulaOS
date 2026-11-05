# NebulaOS

**A new operating system for the Creality Ender-3 V3 KE.**

NebulaOS replaces all of the KE's software: a new Linux kernel, current upstream Klipper, its own
touchscreen app with guided calibration, and Mainsail in your browser. It updates itself from the
touchscreen, and if an update fails to start, the printer goes back to the version that worked.

**Supported: the Ender-3 V3 KE only** (not the V3 SE).

## Get started

1. **Download** the latest release: [Releases](https://github.com/NebulaOS-KE/NebulaOS/releases/latest)
2. **Install** it: [Installing NebulaOS](https://github.com/NebulaOS-KE/NebulaOS/wiki/Installing-NebulaOS)
3. **Print**: the [NebulaOS manual](https://github.com/NebulaOS-KE/NebulaOS/wiki) takes you from
   the first start through calibration and your slicer to your first print.

### Which file do I need?

| You are on | Download |
|---|---|
| Creality's stock firmware | `NebulaOS-Ender3V3KE-F005_ota_img_V9.<version>.img`. Put it on a USB stick **without renaming it** and install it from the stock touchscreen. When NebulaOS is up, switch the printer off and on once. |
| OpenKE | `NebulaOS-Ender3V3KE-<version>.img`, installed with Creality's updater over SSH |
| NebulaOS already | Nothing: **Settings → Updates** finds new versions by itself |
| A printer that no longer starts | `NebulaOS-Ender3V3KE-<version>.ingenic`, the USB recovery image. It **erases the whole printer**, so use it only when nothing else works: [Recovery](https://github.com/NebulaOS-KE/NebulaOS/wiki/Recovery) |

Want to go back? [Going back to your old firmware](https://github.com/NebulaOS-KE/NebulaOS/wiki/Going-Back).

## Help

- [Troubleshooting](https://github.com/NebulaOS-KE/NebulaOS/wiki/Troubleshooting)
- Found a bug? [Open an issue](https://github.com/NebulaOS-KE/NebulaOS/issues). The touchscreen's
  **Settings → System → Report a problem** collects the logs to attach.

NebulaOS is community software, not made or supported by Creality.

## For developers

NebulaOS is open source. Everything is built and put together in
**[NebulaOS-firmware](https://github.com/NebulaOS-KE/NebulaOS-firmware)**: the architecture, the
other repositories, how to build an image and how a release is made all start there.

## License

See each repository's own license.
