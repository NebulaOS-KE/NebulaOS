# NebulaOS

NebulaOS is open firmware for the **Creality Ender-3 V3 KE**: a Linux 6.6 real-time kernel,
upstream Klipper and Moonraker, Mainsail, and its own touchscreen app (NebulaScreen), with A/B
system slots, on-printer updates and USB recovery.

This repository is the front door: **releases are published here**
([Releases](https://github.com/NebulaOS-KE/NebulaOS/releases)), and this page shows how the
project's repositories fit together. The source lives in the repositories below.

## Download

Each release carries:

| File | Use it for |
|---|---|
| `NebulaOS-Ender3V3KE-<version>.img` | Installing or updating: on NebulaOS from the touchscreen (Settings > Updates > System image), on the stock firmware with Creality's own updater |
| `NebulaOS-Ender3V3KE-<version>.ingenic` | USB recovery of a printer that does not start |
| `SHA256SUMS`, `*.sha256` | Checking a download: `sha256sum -c SHA256SUMS` |
| `release-manifest.txt`, `build-manifest.txt` | The exact source of every component in the release |
| `nebulaos-release.json` | The record a NebulaOS printer reads to update itself over the internet |
| `xImage`, `rootfs.squashfs` | The kernel and root filesystem inside both packages (developers) |

A NebulaOS printer finds new releases itself (Settings > Updates > System image > Online). It
downloads only over HTTPS from github.com and keeps the image only when its size and sha256 match
the release record; installing it uses the same A/B install as a USB stick, with an automatic way
back if the new system does not start.

Every release is built on GitHub, from public source, twice on separate machines; the two builds
must be byte-identical. The `.img`, the `.ingenic` and the release record carry a GitHub build
attestation: `gh attestation verify <file> -R NebulaOS-KE/NebulaOS`.

## The project

```
                    NebulaOS-kernel ──────────┐
       Klipper3d/klipper (upstream, pinned) ──┤
NebulaOS-klipper-extensions (production) ─────┤
        Arksine/moonraker, Mainsail ──────────┼──► NebulaOS-firmware ──► NebulaOS (releases)
             NebulaOS-nebulascreen ───────────┤     pins + builds         .img / .ingenic
      NebulaOS-klipper-mcu (MCU binary) ──────┘
                                                    nebulaos-packages: Python wheels for
                                                    Moonraker/Klipper updates on the printer
```

| Repository | What it is |
|---|---|
| [NebulaOS-firmware](https://github.com/NebulaOS-KE/NebulaOS-firmware) | The integration repository: pins every input by commit or digest (`manifests/dependencies.conf`), builds the image in one pinned container, packages `.img` and `.ingenic`. Start here for building, the architecture and the docs |
| [NebulaOS-kernel](https://github.com/NebulaOS-KE/NebulaOS-kernel) | Linux 6.6 PREEMPT_RT for the Ingenic X2000 (branch `openke`) |
| [NebulaOS-klipper-extensions](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions) | NebulaOS's Klipper extras (calibration, load-cell probing, power-loss recovery, ...), composed into upstream Klipper at boot - no Klipper fork |
| [NebulaOS-nebulascreen](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen) | NebulaScreen, the touchscreen app (based on GuppyScreen); also updatable on its own from its releases |
| [NebulaOS-klipper-mcu](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu) | Klipper firmware for the mainboard's GD32F303: upstream Klipper plus an explicit patch series |
| [nebulaos-packages](https://github.com/NebulaOS-KE/nebulaos-packages) | Pre-built Python packages, so Moonraker and Klipper updates on the printer need no compiler |
| [lv_drivers](https://github.com/NebulaOS-KE/lv_drivers) | LVGL display/touch drivers used by NebulaScreen |

What ships is what `NebulaOS-firmware/manifests/dependencies.conf` pins - not the latest commit
of each repository.

## How a release is made

[`.github/workflows/release.yml`](.github/workflows/release.yml), started by hand with a
NebulaOS-firmware commit, on GitHub's free runners:

1. **build A** and **build B**: two independent release builds of that commit
2. **compare**: kernel and root filesystem must be byte-identical
3. **package**: `.img`, `.ingenic`, checksums, manifests, the release record and the attestation,
   as a **draft** release

The draft is published after the build has been tested on a printer. Printers only see
published releases.

## License

See each repository's own license.
