# Power-loss recovery

## What this page will help you do

Understand what happens when the power goes out during a print, and how to continue the print
instead of starting over.

You do not have to set anything up. NebulaOS does this by itself.

## What you need

Nothing. Power-loss recovery is part of NebulaOS and is always running during a print.

## How it works, briefly

While a print runs, NebulaOS keeps saving a checkpoint of where the print is - the position in
the file, the nozzle and bed temperatures, the bed mesh in use, and which objects you have
cancelled if you are using Cancel Object.

The checkpoint is stored in two places: a tiny record on a memory chip on the printer's board
that survives losing power, and a larger file on the printer's storage. The chip record is
written **last**, and only once the file is safely on disk, so the printer never trusts a
checkpoint that did not completely land. That ordering is the whole reason a power cut at the
wrong moment does not leave you with a corrupt recovery.

You do not need to know any of this to use it. It matters only because it explains why the
printer sometimes says there is nothing to recover: if the checkpoint did not fully land, it
is not offered, rather than being offered and then failing.

## Step-by-step: after the power comes back

1. Switch the printer on as usual.
2. Wait for it to start up - about a minute.
3. If a recoverable print was interrupted, the screen offers it to you, naming the file.
4. Choose:
   - **Resume** - carry on from the checkpoint.
   - **Discard** - forget the checkpoint and start fresh.

Look at the part before you choose. Resuming only makes sense if the print is still stuck to
the bed in the position it was in. If it came loose, or you have moved the bed or the part,
discard it.

*No screenshot yet: the recovery offer appears as a prompt during startup, which the
simulator's screenshot tour does not reach. This one needs a photograph of a real printer
after a power cut.*

## Expected result

After choosing **Resume**, the printer works through a deliberate order:

1. **The bed heats first, with the nozzle off.**
2. **Z lifts and X and Y home**, so the toolhead is away from your part.
3. **Only then does the nozzle heat**, at the park position.
4. The bed mesh from the interrupted print is reloaded, the printer returns to the position it
   had reached, and printing continues from the same point in the file.

Objects you had cancelled stay cancelled, and if you were part-way through one, that object is
started again rather than skipped.

**A timelapse keeps its earlier frames.** If you were recording a timelapse, the frames taken
before the power cut are put back in front of the new ones when the print ends, so the finished
video covers the whole print instead of only the part after the resume. Nothing to switch on -
it is set up in the shipped configuration (`machine.cfg`, `timelapse_frame_path`).

**Why the order matters.** It would be simpler to heat everything at once, and a power-cut test
on a real printer showed why that is wrong: the nozzle heated *while still sitting over the
part*, which risks melting into the print you are trying to save. Heating the nozzle only once
it has moved away costs a little time and removes that risk entirely.

*The order comes from extensions `f498796`, the version NebulaOS 1.0.0 ships.*

## If a resume fails partway

Worth knowing, because the printer's behaviour here is deliberate and might otherwise look
like a malfunction.

If a resume starts but cannot complete, NebulaOS cleans up rather than leaving things half
done:

- **The nozzle heater is switched off,** so a hot nozzle is not left parked over your part.
- **The file is unloaded,** so the screen and Mainsail do not show a print that is not actually
  running.
- **The bed heater stays on.** This is on purpose: a warm bed keeps the part stuck down, which
  is exactly what you need in order to try again.
- **The checkpoint is kept,** so **Resume** is offered again.

So a failed resume leaves you able to retry, with the part still attached. If you would rather
not retry, choose **Discard** and turn the bed off yourself.

*From extensions `f498796`, the 1.0.0 release pin (`nebulaos_power_loss_recovery.py`,
`_undo_failed_resume`).*

## Troubleshooting

| What happens | What it means |
|---|---|
| No recovery is offered after a power cut | No complete checkpoint landed, so there is nothing to recover. Start the print again. |
| Recovery is offered but the part came loose | Choose **Discard**. Resuming onto a moved part will fail, or drive the nozzle into it. |
| Resume heats up, then stops | A step was refused. The nozzle is turned off, the bed left on, and **Resume** is offered again. |
| The print resumes in the wrong place | Report it with the logs: **Settings → System → Report a problem**. |
| You want the offer to go away | Choose **Discard**. |

## For advanced users: the commands behind it

The screen uses macros that call these. You can also run them from the console
(**Home → Console**) or from Mainsail:

| Command | What it does |
|---|---|
| `NEBULAOS_PLR_STATUS` | Reports the current power-loss-recovery status |
| `NEBULAOS_PLR_RESUME` | Resumes from the checkpoint |
| `NEBULAOS_PLR_DISCARD` | Discards any checkpoint |

Two further commands exist, `_NEBULAOS_PLR_LOAD_MESH` and `_NEBULAOS_PLR_SET_Z`. The leading
underscore marks them internal: they are steps of `NEBULAOS_PLR_RESUME` and are not meant to
be run on their own.

## Recovery and reversal

**Discard** is how you undo a pending offer, and it cannot be undone itself - the checkpoint is
gone afterwards. It does not touch the G-code file, so you can always start the print again
from the beginning.

## Related

- [Printing](Printing) - pausing, resuming and cancelling a print normally
- [Recovery](Recovery) - recovering the printer itself, which is a different thing
