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

