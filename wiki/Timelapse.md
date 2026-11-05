# Timelapse

## What this page will help you do

Record a video of a print - one picture per layer, turned into a film when the print finishes -
and understand the two settings that decide whether the result looks good.

## What you need

- A camera that works in Mainsail. Any USB webcam, or Creality's Nebula Camera. If you can see
  the live picture in Mainsail, timelapse can use it. See [Camera](Camera).
- [Mainsail open in a browser](Opening-Mainsail). **Everything on this page is done in
  Mainsail.** There is no timelapse control on the printer's own touchscreen.

## Before you begin

**Timelapse is switched off when NebulaOS is installed.** That is deliberate: recording costs
storage and, with head parking on, print time. You switch it on once and it stays on.

You do **not** need to change anything in your slicer. NebulaOS watches the nozzle height and
takes the pictures itself - see *How the pictures are taken* below.

## Step-by-step: switch it on

1. Open Mainsail and go to **Settings → Timelapse**.
2. Turn **Enabled** on.
3. Leave **Mode** on the layer setting (the default). The other mode, *hyperlapse*, takes a
   picture every so many seconds instead of every layer - useful for a print with very few,
   very long layers.
4. Decide about **park head** - the one setting that changes how the video looks. See the next
   section. It is **off** when NebulaOS is installed.
5. Start a print as usual.

## Expected result

While the print runs, pictures pile up invisibly. When the print finishes, the printer renders
them into an MP4 by itself and the video appears in Mainsail's **Timelapse** list, where you can
play it, download it or delete it.

**A cancelled print is different, and this one catches people out.** Recording stops, but no
video is made automatically - only a print that runs to the end renders by itself. The pictures
are still there, and they stay there until the next print starts, which clears them. So if you
want the film of a print you cancelled, run `TIMELAPSE_RENDER` from the console
(**Home → Console**) *before* you start anything else.

## Park head: the one setting worth understanding

| | Off (how NebulaOS ships) | On |
|---|---|---|
| What happens per layer | The picture is taken wherever the nozzle happens to be | The print pauses, the filament is retracted a little, the nozzle moves out of shot, the picture is taken, and printing resumes |
| The video | The nozzle moves around in frame | The object appears to grow on its own, with nothing else moving |
| The print | Not affected | Slower, and every pause is a chance for a blob or a string |

Neither is wrong. *Off* is the safe default and still gives a perfectly watchable video; *on* is
what produces the clean "it built itself" look, at a cost to the print.

If you turn park head on, use a tall-ish test print first rather than a part you care about.

## How the pictures are taken

Normally, a timelapse needs you to add a line to your slicer's layer-change script. NebulaOS does
it for you instead.

A small watcher starts with the print (after the purge line) and stops when the print ends or is
cancelled. Once a second it looks at the nozzle height; a height that is *higher than the last
picture's and has held still for a second* counts as a new layer and triggers one picture. A
Z-hop does not hold still for a second, so it does not produce a picture, and dropping back down
is recognised as the end of a long hop rather than a new layer.

**If your slicer already sends `TIMELAPSE_TAKE_FRAME`, remove that line** - otherwise you get two
pictures per layer.

*From the NebulaOS image: `/etc/nebulaos/klipper/camera.cfg` (`_NEBULAOS_TIMELAPSE`), started and
stopped by `START_PRINT`, `END_PRINT` and `CANCEL_PRINT` in `print.cfg`, firmware `3bd9675`.*

## A power cut does not cost you the video

If the power goes out and you [resume the print](Power-Loss-Recovery), the pictures taken before
the cut are kept and put back in front of the ones taken after it. The finished video covers the
whole print, not just the part after the resume.

Nothing to switch on - it is set up in the shipped configuration.

## Storage

Videos live on the printer until you delete them, and they are **not** removed by
**Settings → System → Storage → Free up space** ([Resetting](Resetting#freeing-up-space)), which
only clears NebulaOS's own leftovers. Delete videos you no longer want from Mainsail's Timelapse
list.

The half-finished pictures of a print in progress are temporary and are cleared as each new print
starts.

## Troubleshooting

| What happens | What to do |
|---|---|
| No video after a print | Check **Settings → Timelapse → Enabled** is on. It is off until you turn it on. |
| No video, and timelapse is on | The print has to be started with NebulaOS's own `START_PRINT` for the watcher to run. Printing a file whose start G-code replaces it will not record. |
| Two pictures per layer, and a jerky video | Your slicer is also sending `TIMELAPSE_TAKE_FRAME`. Remove it from the slicer's layer-change script. |
| The nozzle is visible in every frame | That is park head being off. Turn it on if you want it out of shot, and read the table above first. |
| Blobs or strings since turning park head on | The pause at each layer is doing it. Turn park head off, or raise the retraction a little. |
| The console says *"minimum extruder temperature not reached"* | A picture was requested before the nozzle was hot. Harmless. |
| The video is there but very short | Few layers means few pictures. Hyperlapse mode suits that kind of print better. |
| A print was cancelled and there is no video | Cancelling does not render. Run `TIMELAPSE_RENDER` before starting the next print - starting one discards the pictures. |

## Recovery and reversal

Turning **Enabled** off in Mainsail stops all recording. Existing videos are untouched; delete
them from the Timelapse list when you want the space back.

## For advanced users

Timelapse is upstream [moonraker-timelapse](https://github.com/mainsail-crew/moonraker-timelapse),
shipped unmodified. NebulaOS adds the layer watcher, keeps the frames across a power loss, and
changes three defaults when the printer is first set up:

| Default | NebulaOS | Upstream |
|---|---|---|
| Enabled | off | on |
| Park head | off | off |
| Render options | `-preset ultrafast` | none |

The render preset is not a quality preference: the printer has 256 MB of RAM, and the lightest
x264 preset is what renders reliably on it. These three are written once, through the same
settings interface Mainsail uses, so anything you change afterwards stays changed.

Macros you can run from the console: `GET_TIMELAPSE_SETUP` prints the current setup,
`TIMELAPSE_RENDER` renders what has been recorded so far, and
`HYPERLAPSE ACTION=START [CYCLE=<seconds>]` / `HYPERLAPSE ACTION=STOP` drives the other mode by
hand (the cycle defaults to 30 seconds).

*From firmware `3bd9675`: `manifests/dependencies.conf` (upstream pinned at `c7fff11`),
`/usr/libexec/nebulaos-seed-timelapse`, `etc/nebulaos/moonraker/nebulaos.conf`
(`[timelapse]`), and `etc/nebulaos/klipper/camera.cfg`.*

## Related

- [Camera](Camera) - the live picture, and the Nebula Camera's own settings
- [Printing](Printing) - starting and watching a print
- [Power-loss recovery](Power-Loss-Recovery) - what happens to a recording when the power goes
- [Opening Mainsail](Opening-Mainsail) - reaching Mainsail from your computer or phone
