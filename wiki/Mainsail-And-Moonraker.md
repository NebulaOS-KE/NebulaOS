# Mainsail and Moonraker

**Mainsail** is the printer's web page. **Moonraker** is the API underneath it: Mainsail, the
touchscreen, slicers, phone apps and home automation all talk to the printer through Moonraker.
Both are standard, so their own documentation applies as written:
[docs.mainsail.xyz](https://docs.mainsail.xyz) and
[moonraker.readthedocs.io](https://moonraker.readthedocs.io).

## Opening Mainsail

Type the printer's address into a browser on the same network - the one on **Settings →
Connections**, for example `http://192.168.1.42`, or `http://nebulaos-xxxx.local`. Step by step:
[3. First start](First-Time-Setup#open-mainsail).

The touchscreen and Mainsail show the same printer and work at the same time. The screen is
better when you are standing at the machine; Mainsail for uploading files, editing configuration,
the console, the print history and watching from elsewhere.

## Addresses and ports

| What | Where |
|---|---|
| Mainsail | `http://<printer>` - port 80 |
| Moonraker API, through the web server | `http://<printer>` - port 80 forwards `/server`, `/printer`, `/machine`, `/access`, `/api` and `/websocket` to Moonraker |
| Moonraker API, directly | `http://<printer>:7125` |
| OctoPrint-compatible upload | `http://<printer>` (`/api`) - for slicers that upload the OctoPrint way |
| Camera stream | `http://<printer>/webcam/` |

The screen's **Settings → Connections** page shows the Mainsail and Moonraker addresses of your
printer.

**Upload size:** up to 512 MB per file (Moonraker's limit; the web server sets none).

## Who may connect

Moonraker lets these clients in without a login (`[authorization]` in `moonraker.conf`):

- the printer itself (`127.0.0.1`);
- home networks in `192.168.0.0/16` and `10.0.0.0/8`.

Browser apps on other web pages may call the API from `http://*.local` and `http://*.lan`
(`cors_domains`). **A network in `172.16.0.0/12` is not in the list** - if yours is, add it to
`trusted_clients` in `moonraker.conf` and restart Moonraker.

There is no login on top of that: anything on those networks can control the printer. Keep the
printer on your home network, and do not forward its ports to the internet.

## Slicer upload

In OrcaSlicer choose the host type **Octo/Klipper** and enter `http://<printer>`; PrusaSlicer and
Cura upload through their OctoPrint option to the same address. NebulaOS answers OctoPrint-style
uploads there (`[octoprint_compat]`). Slicer setup: [5. Set up your slicer](Slicer-Setup).

## Phone apps and home automation

Anything that speaks Moonraker's API connects with the printer's address and port 80 or 7125, from
a trusted network as above. The printer also announces itself on the network as
`<name>.local` (`[zeroconf]`). There is nothing NebulaOS-specific to set up; follow the app's or the
integration's Moonraker instructions.

## Moonraker settings NebulaOS uses

| Setting | Value | Why |
|---|---|---|
| `[file_manager] enable_object_processing` | `True` | Adaptive mesh, smart park, purge line and Exclude Object need the object outlines. Keep it on |
| `[update_manager]` automatic refresh | off | Updates are checked when you ask (**Settings → Updates → Check now**, or Mainsail) |
| Update channels | Moonraker and Mainsail `stable`; Klipper `dev`; the NebulaOS extensions from their `production` branch; the screen from its releases | |
| `[timelapse]` | off by default; videos in `/opt/printer_data/timelapse/` | [Timelapse](Timelapse) |
| `[spoolman]` | written by the screen when you set a server | [Custom macros and integrations](Macros-And-Integrations#spoolman) |
| Webcam | no `[webcam]` section; the default camera is added once to Moonraker's database | so you can edit or delete it in Mainsail |

`moonraker.conf` in `config/` is yours to edit. The NebulaOS parts are in included files that the
image owns and an update replaces (`/etc/nebulaos/moonraker/`); Moonraker merges a section repeated
in your `moonraker.conf` with them.

*From `opt/printer_data/config/moonraker.conf` (lines 5-16, 36-53, 91-93, 188-206),
`etc/nebulaos/moonraker/klipper-pin.conf:26-75`, `etc/nebulaos/moonraker/nebulaos.conf:10-41` and
`etc/nginx/nginx.conf:22-110`, firmware `dc868e3`; the screen's addresses from
`src/nebulaos_settings.cpp:64-71` at screen `fd47cb6`.*

## Next

- [Custom macros and integrations](Macros-And-Integrations)
- Need help? [Troubleshooting](Troubleshooting)
