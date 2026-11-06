# SSH, SFTP and security

You do not need SSH to print. It is for looking at files, editing configuration by hand and running
commands on the printer. Everything on this page assumes the printer is on your network -
[3. First start](First-Time-Setup).

## Logging in

| | |
|---|---|
| **Address** | The printer's address from **Settings → Connections** (for example `192.168.1.42`), or its name, `nebulaos-xxxx.local` |
| **User** | `root` |
| **Password on a new install** | `NebulaOS` |
| **Port** | 22, the SSH default |

**Change that password straight away:** log in and type `passwd`. NebulaOS keeps the new one
across reboots, updates and slot switches - it says *"root password changed (kept across reboots
and updates)"*.

**Never make SSH reachable from the internet.** No port forwarding on your router to the printer.
Anyone who can reach port 22 can try passwords, and `root` can change everything. For remote
access, use a VPN to your home network.

Any SSH and SFTP client works - for example PuTTY and WinSCP on Windows, or `ssh` and `sftp` in a
terminal on Linux and macOS:

```
ssh root@192.168.1.42
```

Commands on this page are typed in that shell, on the printer. The prompt shows the printer's
name, like `root@nebulaos-4f2a:~#` - the quickest way to be sure which printer you are typing into.

**SFTP** opens in the printer's data folder, `/opt/printer_data`, with `config/`, `gcodes/` and
`logs/` - the same folders Mainsail shows. What they hold: [Files, configuration and
backups](Files-And-Configuration).

## Which password applies

| Your situation | The root password |
|---|---|
| A new NebulaOS install | `NebulaOS` |
| You ran `passwd` | Yours - kept through every update |
| The printer ran an earlier NebulaOS test build first, and you never changed it | The old default, `openke`: the printer keeps the password it was first given, and updates do not change it |
| After a [clean NebulaOS reset](Resetting) | `NebulaOS` again - the reset erases the saved password |
| Installed over OpenKE | NebulaOS does not read OpenKE's password. On a printer that never ran NebulaOS before, it starts with `NebulaOS`. OpenKE's own slot keeps OpenKE's password |

## What you can and cannot do

- **You are root.** There is no general `sudo`: the `sudo` on the printer is a small adapter that
  only lets Moonraker reboot or shut the printer down, and refuses everything else. As root you do
  not need it.
- **The system itself is read-only.** `/etc`, `/usr` and the programs are part of the image and
  are replaced by the next update. Your files live in `/usr/data` (configuration, prints, logs).
  To change printer behaviour, edit the files in `config/` - see
  [Files, configuration and backups](Files-And-Configuration).
- **SSH starts early.** It comes up even when something later in the start fails, which is what
  makes it useful for [Recovery](Recovery).
- **Klipper can run shell commands** from G-code with `RUN_SHELL_COMMAND` - see
  [Custom macros and integrations](Macros-And-Integrations).

## Useful commands

| Command | What it does |
|---|---|
| `passwd` | Change the root password |
| `cat /opt/printer_data/logs/nebulaos-state.txt` | Versions and state, in one file |
| `reboot` | Restart the printer cleanly |
| `poweroff` | Shut down; switch off at the power switch afterwards |

*From `scripts/build/nebulaos-post-build.sh:32-53`, `etc/nebulaos-shadow.sh:3-64`,
`usr/bin/passwd`, `usr/bin/sudo`, `usr/libexec/sftp-server`,
`etc/init.d/S02nebulaos-early-ssh`, `etc/init.d/S46nebulaos-dropbear-keys` and `usr/libexec/nebulaos/nebulaos-clean-reset:7-32`,
firmware `dc868e3`. The SSH server is Dropbear (`br2-external/configs/nebulaos_x2000_defconfig:70`).*

## Next

- [Files, configuration and backups](Files-And-Configuration)
- Need help? [Troubleshooting](Troubleshooting)
