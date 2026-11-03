# Status log

`STATUS.md` answers *where does this stand now*. This file keeps the parts of its history
that are still worth reading: the mistakes, and why they happened. The full narrative is in
the commit history of the `docs/agent` branch, which is a better changelog than a file that
grows by one section per batch.

Kept here because each one is a trap a later session could fall into again.

## A discovery mistake worth recording

The first attempt at NebulaScreen configuration discovery swept the UI source for every
`_json_pointer` literal and produced 104 "settings". Most were not settings at all - they
were pointers into Moonraker response and printer status objects: `/sg_result`,
`/layer_count`, `/commits_behind_count`, `/toff`. Counting those as configuration would have
inflated the inventory with roughly 85 options that do not exist, and the dashboard would
have looked busier while being less true.

Discovery is now scoped to what is actually a setting: keys the config schema itself touches
in `src/config.cpp` and `src/config.h` where defaults are applied, plus keys any panel reads
or writes through the `Config` object. That yields **20** NebulaScreen settings. The
Moonraker and status-object surface is real and still needs documenting, but it is an API
inventory and will be discovered as one.

A second correction: an earlier draft of this file claimed 42 extension modules. The real
count is **30** modules and **31** test files. Both numbers now come from the inventory.

## A second discovery bug, caught the same way

The endpoint extractor first used the character class `[a-z_/]+` for API paths. That silently
dropped `/machine/nebulaos/network/ipv4`, because `ipv4` contains a digit - the inventory
reported 55 endpoints instead of 56, and a missing endpoint is indistinguishable from an
endpoint that does not exist. Found by counting every `/machine/nebulaos/` path literal in
the file and comparing against the table, which now agrees at 56.

Two discovery bugs in two slices, both in the direction of under- or over-collecting
silently. Every extractor from here on gets a second, independent count before its output is
trusted. The build/tooling/runtime slice was checked that way and agreed exactly: 14 build
scripts, 56 overlay executables, 11 tool sets by shell count and by inventory count alike.

Worth noting that the habit cut both ways this time. It caught over-collection in the config
sweep, under-collection in the API regex, and here it prevented a wrong *exclusion* - the
five system-named shims that looked like noise and were not.

## A misleading number I introduced, and removed

Recording "what still needs writing" in the inventory's `blockers` field made the dashboard
report **57% blocked**. That reads as a stuck project. It was nothing of the kind: almost all
of those were completeness gaps - work not yet done - rather than anything unable to proceed.

Now separated. `blockers` means only what it says: something that cannot proceed without
hardware, access, or a decision this agent cannot make. Everything else is a `gaps` entry,
counted on its own line. The real split is **6 blocked (1%)** and **311 completeness gaps
(56%)**.

Two numbers, two meanings. One field holding both made the honest-looking figure the wrong one.


## Nearly repeating the overclaim, two iterations after correcting it

**2026-11-01.** After adding module-header purposes and the restart rule to `CONFIG.md`, I
marked all 152 extension configuration options `documented`. Coverage jumped from 21% to 49%
in one step.

Then I looked at what had actually changed. The per-option entries were **identical** to
before: name, type, default, constraints. What I had added was a purpose per *section* and one
global fact about restarts. Mission 6.6 asks for purpose, runtime behaviour, dependencies and
an example **per option**.

Reverted to draft. Coverage back to 21%.

The distinction that matters, and the reason the commands promotion was legitimate while this
one was not:

- **Commands:** real per-command content was added - parameters with ranges, errors, side
  effects, an example invocation. The residual gaps (expected output, safety judgement) are
  things *no amount of source reading can supply*.
- **Configuration:** nothing per-option was added. The residual gap - what each option is
  for - **can** be written by someone who reads the module. It is simply not done.

"Documented" means the work is done, not that the remaining work is hard. The warning sign was
the shape of the jump: a large promotion that followed a small amount of new writing. The same
shape as the 14%-to-49% error two iterations earlier, and I nearly made it twice.

## A hand-written data file that contributed nothing, twice over

**2026-11-01.** Wrote 45 per-option purposes into
`documentation/agent/data/extension_option_purposes.json`, wired the generator to merge them,
regenerated, and got **41 options with a purpose** - the same number as before the file
existed.

Two separate faults, each silent:

1. **The file landed in the wrong repository.** The shell's working directory had drifted into
   the extensions worktree, so `mkdir -p documentation/agent/data` created that path *inside
   the extensions repo*. The generator resolves the file relative to its own location, found
   nothing, and returned an empty dict without complaining. All 41 purposes were coming from
   source comments alone.
2. **Two keys used Python attribute names instead of config keys.**
   `max_tune_printing_seconds` for `max_tune_seconds_printing`, and `stable_drift` for
   `stable_drift_counts_per_s`. Those two purposes would never have displayed.

Both were caught only because the output count was compared against what had been written -
45 in, 41 shown. Without that arithmetic the file would have sat in the wrong repo indefinitely
while the reference looked like it had purposes.

Fixes: the file moved, the keys corrected, the stray directory removed from the extensions
worktree, and the generator now **prints a warning naming any purpose written for an option
that does not exist**. A data file that silently contributes nothing is worse than no data
file, because it looks like the work is done.

Two habits confirmed: check the output count against the input count, and check `pwd` before
creating a directory.

## I reported a documentation bug that did not exist

**2026-11-01.** While building the simulator I hit a link failure on `-lSDL2`, traced it to the
Makefile's default `LDFLAGS ?= -static ...`, and reported that NebulaScreen's
`Building-from-Source` page documents `LDFLAGS` that cannot link. I put it in `STATUS.md` and
told the foreground session.

It was false. That page documents **exactly** the override I ended up using, and the line
immediately below the code block says: *"The `LDFLAGS` override drops the Makefile's default
`-static`, which a desktop SDL2 build cannot use."* It also warns about
`-Wno-incompatible-pointer-types` on GCC 14+. The page is correct and more complete than my
report of it.

What went wrong: I read the **Makefile's** default and attributed it to the **documentation**,
without opening the page's build section. I had read that page earlier for the submodule steps
and assumed I knew what else it said.

Two things worth keeping:

- **A tool's failure is not evidence about the docs.** The build failed, so I reasoned the
  instructions must be wrong - when in fact I had not followed them. The instructions were
  sitting four lines below the command I had copied.
- **Reporting a doc bug is a claim like any other.** This project's whole stance is that
  nothing goes in without checking the source; I applied that to the code and not to my own
  bug report. Worse, a false bug report costs someone else time, and I had already sent it to
  the foreground session.

Corrected in `STATUS.md`, and the foreground was told.

The one real bug in the same area was genuine: three wiki pages pointed at the retired
`coreflake1/NebulaOS-guppyscreen` repository. Fixed.

## Resetting my own branch while picking up new code

**2026-11-01.** To regenerate the references against a new extensions tip I ran:

```
git checkout -B docs/extensions origin/main
```

`-B` **resets** the named branch to the given commit. It moved `docs/extensions` off my five
doc commits and onto `origin/main`, and the working tree lost `docs/reference/` entirely - the
next command failed with "No such file or directory", which is how I noticed.

Nothing was lost, because every batch had been pushed: `origin/docs/extensions` still pointed at
`06c84e4`. The recovery was to restore the branch from the remote and merge `origin/main` into
it, which is what should have happened in the first place.

Two things to keep:

- **To pick up new upstream code on a working branch, merge it.** Do not re-point the branch at
  it. `-B` is for creating a branch, not updating one.
- **Pushing after every batch turned a destructive mistake into an annoyance.** That habit was
  adopted for durability across sessions; it paid off for a reason I had not anticipated.

## The inventory cited my own documentation as the source of code facts

**2026-11-01.** `seed_inventory.py` recorded each worktree's `HEAD` as an item's
`source_commit`. That was right while the worktrees sat on plain upstream checkouts. Once they
moved onto this agent's own `docs/*` branches - with documentation commits and merges on top -
every item started citing a *documentation* commit as the source of a *code* fact.

The dashboard showed `ddb14e669d78` as the commit 194 firmware items were discovered at.
`ddb14e6` is a page of prose. Anyone following that SHA to check the API surface would find
documentation, not implementation.

Fixed by recording `origin/<default-branch>` - the tip of the code the documentation describes -
falling back to HEAD only where no such ref exists.

Why this one is worth recording: **nothing failed.** No script errored, no count moved, every
item carried a plausible 40-character SHA. The whole value of an evidence trail is that a reader
can follow it, and a trail pointing at the wrong artefact is indistinguishable from a correct one
until somebody does. It was caught by reading the dashboard's own table and recognising the
SHAs as mine.

## I published a false safety warning, derived from a true code comment

**2026-11-01.** The end-user manual's most prominent warning - `Safety-First` led with *"The one
that can break your printer for good"* - told readers never to power-cycle a printer running
Creality's system, because a stock cold boot reflashes the MCU and would leave it mismatched
until a USB recovery from a computer. It appeared on six pages.

It was wrong. `S50nebulaos-mcu-guard` → `mcu_lifecycle.py` classifies the running MCU
application, and `KNOWN_STOCK` authorises `mcu_restore.py` to reinstall the native firmware
automatically. Each system restores its own MCU firmware at boot; switching is self-correcting
in both directions.

**Where it came from.** `S00revert-safety`'s header explains that automatic rollback was removed
because a stock boot reflashes the MCU, "destroying the qualified native GD32F303 MCU build".
That sentence is accurate about the reflash. I turned it into *therefore permanent damage needing
USB recovery*, and never looked for code that restores it.

Three things worth keeping:

- **A code comment is prose.** The rule in this project is to derive behaviour from code, and I
  had already written it down three times. A comment is the most trustworthy-looking prose in a
  repository, which makes it the easiest to mistake for the thing itself.
- **I extrapolated a consequence the comment did not claim.** It said a reflash happens and that
  this was reason enough to remove an automatic path into stock. It did not say the reflash was
  unrecoverable. The inference felt so natural that I never identified it as an inference.
- **The scariest claim deserves the most checking, and got the least.** It was the one sentence
  in the manual most likely to change a reader's behaviour. "Never do X or you will destroy your
  printer" should have triggered a search for the recovery path before it was ever written.

Corrected across six user pages, the firmware architecture guide, and three of the firmware's own
documents which carried the same stale framing because they predate `mcu_restore.py`. A new page,
`wiki/Mainboard-Firmware.md`, documents what the screen's MCU page actually does - it had none.

Caught by the project owner, not by me.

## 2026-11-04 - an observation on one route attributed to another

Writing up why 1.0.0 was rebuilt, I recorded the out-of-memory failure as *"the first concrete
evidence about [the stock-touchscreen route]... found by someone running it rather than by
reading the code."*

It was found on the **online update** path. That the stock route fails the same way is an
inference from the same file, the same RAM and Creality's updater also having to unpack it -
reasonable, and not evidence. The sentence moved an observation from the route where it
happened to the route this project has been careful to call unverified for days, and it did so
inside `VERIFICATION.md`, the file whose entire job is keeping those apart.

Nothing in the manual was affected; the fault is in the image, not the procedure. B-003 stays
unverified rather than becoming *observed failing*.

Caught by the main session on review, not here. The tell was available: I knew the report came
from an online update and wrote "someone running it" about a different route in the next
clause.
