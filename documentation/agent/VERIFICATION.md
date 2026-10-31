# Verification policy

Documentation in this project is only as good as the evidence behind it. This file defines
what each state in `coverage.jsonl` means, and what it takes to claim it. Nothing here is
decorative: a status is a promise, and promoting one without the evidence is the single
worst thing this agent could do.

## The states

| State | Meaning | Evidence required |
|---|---|---|
| `verified` | Confirmed against the applicable code, and against tests or runtime evidence | Source read at a recorded commit **and** a passing test or observed runtime behaviour |
| `partial` | Some of the claim is proven, some is not | Recorded per item in `evidence`, with the gap named |
| `unknown` | Not investigated yet | - |
| `blocked` | Cannot be verified with the access available | A named missing dependency in `BLOCKERS.md` |
| `n/a` | The check does not apply to this kind of item | A reason, when it is not obvious |

Documentation status is tracked separately from verification:

| `doc_status` | Meaning |
|---|---|
| `missing` | No page covers this item |
| `draft` | A page exists but has not passed the quality checks in `MISSION.md` Part 10 |
| `documented` | A page exists and covers the item completely |
| `verified` | Documented, and every technical claim on the page is backed by recorded evidence |

The mission also asks for these dispositions where they apply; they are recorded in
`release_applicability` or in the page text itself:

- **Development only** - implemented, but not part of the supported release.
- **Historical** - was true once, or belongs to retired functionality.
- **Planned** - proposed, not implemented.

## What this agent can and cannot prove

**Can prove:** that code exists, what it does, how it is registered, what its defaults
are, which configuration keys it reads, which tests cover it, and which commit each claim
comes from. The repositories' own test suites are available and can be run.

**Cannot prove:** that any of it works on a real printer. This agent has no printer
access by design - no SSH, no hardware launcher, no Moonraker calls to a machine. So
`verify_hardware` stays `n/a` or `blocked`, and any page describing hardware behaviour
says plainly that the behaviour is established from the implementation and has not been
observed on hardware by the author of the page.

Implementation is evidence of *intended and implemented* behaviour. It is not evidence of
successful hardware operation, and this agent will not blur the two.

## Recording evidence

Every technical claim carries a reference in the item's `evidence` list, in the form
`<repo>@<commit>:<path>#<symbol>`, for example:

```
NebulaOS-klipper-extensions@8e3447a:extras/nebulaos_beeper.py#cmd_NEBULAOS_BEEP
```

Pages cite the same references, pinned to the exact commit, so a reader can check any
sentence against the source it came from.

## Source revisions

Documentation describes the **newest** code: the tip of each repository's default branch.
The firmware's `manifests/dependencies.conf` says which commit of each component the
firmware build actually ships. Where a default branch is ahead of its shipping pin, the
page documents the newest code and names the pin, so nobody mistakes development work for
released behaviour. `REPOSITORY_HEAD` is not `SHIPPING_PIN`, and the dashboard records
both.
