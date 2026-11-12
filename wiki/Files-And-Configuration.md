# Files, configuration and backups

Where NebulaOS keeps your settings, which files are yours to edit and which it replaces, what
survives an update or a reset, and how to keep a copy.

## The three folders that are yours

Mainsail shows them, and SFTP opens in them ([SSH, SFTP and security](SSH-And-SFTP)). On the
printer they are under `/opt/printer_data`. `config/` and `logs/` are stored in
`/usr/data/nebulaos/printer_data`; `gcodes/` is the print-file folder shared with the other
system slot (`/usr/data/printer_data/gcodes`), which is why print files survive a clean reset.

| Folder | What is in it |
|---|---|
| `config/` | The printer's settings - Klipper and Moonraker read these |
| `gcodes/` | The files you print. A USB stick shows up in `gcodes/USB/` |
| `logs/` | What the printer writes down. `nebulaos-state.txt` summarises versions and state |

Inside `config/`:

| Path | Whose | What it is |
|---|---|---|
| `printer.cfg` | **Yours** | Your Klipper settings. Calibration results are saved at the bottom, in the `SAVE_CONFIG` block |
| `moonraker.conf` | **Yours** | Moonraker's settings (Spoolman, update channels, who may connect) |
| `songs.conf` | **Yours** | Your [beeps and songs](Beeps-And-Songs) |
| `macros/` | **Yours** | Your own macros, one `.cfg` per file, loaded automatically |
| `nebulaos/` | NebulaOS | NebulaOS's own Klipper settings: `platform`, `machine`, `prtouch`, `z_offset_probe`, `calibration`, `homing`, `print`, `filament`, `camera`, `beeper` (`.cfg`). **Do not edit** - they are replaced at every update |
| `nebulascreen/` | The screen | The screen's settings |
| `backups/` | NebulaOS | Automatic copies of your settings (below) |
| `uploads/boot-logo/` | You → NebulaOS | Images for the [boot logo](Screen-Display#boot-logo-panel) (PNG, BMP, JPEG) |
| `uploads/mainboard-firmware/` | You → NebulaOS | `.bin` files for the [mainboard](Mainboard-Firmware) |
| `uploads/system-image/` | You → NebulaOS | `.img` files with a whole system ([Settings → Updates](Screen-Updates)) |

Everything else in the data folder (`comms`, `database`, `backup`, `certs`, `misc`, ...) belongs to
Klipper and Moonraker - leave it alone.

## Changing a NebulaOS setting

`printer.cfg` includes NebulaOS's files first, then your `macros/*.cfg`, and anything in
`printer.cfg` itself comes after them. Klipper merges sections with the same name, so **to change
a NebulaOS setting, put the section and the option in `printer.cfg`** (or in a file in `macros/`)
instead of editing `config/nebulaos/`. For example, to change the firmware retraction length:

```ini
[firmware_retraction]
retract_length: 0.8
```

Then restart Klipper (**Settings → Printer → Restart Klipper**). The same works for the variables of
NebulaOS's macros, such as the purge settings in `_KAMP_Settings` - see
[Print setup NebulaOS adds](Adaptive-Print-Setup#settings).

**If you did edit a file in `config/nebulaos/`,** the next update replaces it, keeps your version in
`config/backups/nebulaos-changes-<date>/`, and the screen tells you.

## What survives what

| | Your settings (`printer.cfg`, `macros/`, `moonraker.conf`, calibration) | Print files (`gcodes/`) | Wi-Fi, root password, screen settings | Statistics, Moonraker history |
|---|---|---|---|---|
| **A NebulaOS update** (system or apps) | Kept | Kept | Kept | Kept |
| **Swapping system slots** | Kept (shared data area) | Kept | Kept | Kept |
| **Free up space** (Settings → System → Storage) | Kept | Kept | Kept | Kept |
| **Clean NebulaOS reset** (Settings → Reset) | **Erased** | Kept | **Erased** | **Erased** (the *Before NebulaOS* figures come back) |
| **USB recovery: switch the boot slot** ([Recovery 4a](Recovery#4a-just-switch-the-boot-slot-back)) | Kept | Kept | Kept | Kept |
| **USB recovery: write the whole system again** (`.ingenic`, [Recovery 4b](Recovery#4b-write-the-whole-system-again)) | **Erased** | **Erased** | **Erased** | **Erased** |

An update replaces `config/nebulaos/`, and may make small, one-line migrations in your files when
an option was renamed. When an update brings different Klipper or extension versions than you
installed yourself, it switches to its own and keeps a backup under
`/usr/data/nebulaos/system/migration-backups/`.

**Free up space** removes only old logs, old update backups, unfinished update downloads, uploaded
system images and the download cache - "never print files, configuration, calibration, settings or
Creality's data". It is refused while printing or updating. Details: [Resetting](Resetting).

## Backups

NebulaOS keeps **automatic copies of your settings** in `config/backups/settings-<date>-<reason>/`:
`printer.cfg`, `moonraker.conf`, `songs.conf`, `macros/`, the screen settings and the calibration
files. Moonraker's database (Mainsail's settings, history, and also login data and API keys) is
copied too, but deliberately **not** into `config/`: it goes to the printer's system area, so
downloading `config/` does not include it. A copy is taken at the first start of every new or
rolled-back system and whenever settings change; the newest 5 are kept.

**They live on the printer, so a clean reset deletes them too.** Before a reset, or just to be
safe, download your own copy:

- **Mainsail:** its **Machine** page lists the `config` folder; select files there and download
  them.
- **SFTP:** copy `/opt/printer_data/config/` to your computer.

To restore, upload the files back into `config/` and restart Klipper. If you restored
`moonraker.conf`, restart the printer instead, so Moonraker reads it too.

*From `usr/share/nebulaos/printer_data-README.txt`, `etc/nebulaos/config-materialize.sh:7-68`,
`etc/init.d/S04nebulaos-migrate:47-70` and `1227-1238`, `etc/init.d/S01persistent-datastore:142-143` and `213-217`,
`usr/libexec/nebulaos/nebulaos-clean-reset:7-17`, `usr/lib/nebulaos/python/nebulaos_osconfig/cleanup.py:277-295`
and `snapshot.py:1-44`, `tools/recovery/nebulaos-usb.py:7-14`, firmware `4ee5147`.*

## Next

- [Mainsail and Moonraker](Mainsail-And-Moonraker)
- Need help? [Troubleshooting](Troubleshooting)
