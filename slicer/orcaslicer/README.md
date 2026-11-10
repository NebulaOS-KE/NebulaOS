# NebulaOS OrcaSlicer profiles (Ender-3 V3 KE, 0.4 mm nozzle)

> **A starting point, not a perfect tune.** These are the profiles we print with on our own KE.
> They work well for us, but every printer and every spool is a little different. Use them as a
> good starting point, then calibrate flow and pressure advance for your own filament and adjust
> from there.

Two bundles, for OrcaSlicer 2.5.0 or newer (**File → Import → Import Configs…**):

| Bundle | Printer it adds | Retraction |
|---|---|---|
| `NebulaOS-Ender3V3KE-OrcaSlicer.orca_printer` | Creality Ender-3 V3 KE 0.4 nozzle - NebulaOS (**simple**, the default) | done by OrcaSlicer, with wipe |
| `NebulaOS-Ender3V3KE-OrcaSlicer-firmware-retraction.orca_printer` | Creality Ender-3 V3 KE 0.4 nozzle - NebulaOS (firmware retraction) (**advanced**) | done by the printer (G10/G11), tunable on its screen |

Both contain the same 4 filaments (PLA, PETG, PETG-CF, TPU @NebulaOS) and 16 processes
(0.12 Fine, 0.16 Optimal, 0.20 Standard, 0.24 Draft for each material). `profiles/` holds them
unpacked, so changes can be reviewed. They build on Creality's own Ender-3 V3 KE presets in
OrcaSlicer, which must be installed.

Step by step: [Quickstart: OrcaSlicer profiles](https://github.com/NebulaOS-KE/NebulaOS/wiki/Quickstart-OrcaSlicer).
