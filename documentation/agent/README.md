# documentation/agent

Working records of the `nebulaos-docs` agent - a long-running background session that
writes and verifies the NebulaOS documentation from current source.

These files are deliberately **not** part of the published wiki navigation. They are the
agent's own bookkeeping, kept in Git so that a fresh session can pick the work up without
rediscovering anything.

| File | What it is |
|---|---|
| `MISSION.md` | The full assignment, stored verbatim so it survives any context loss |
| `RULES.md` | Workspace rules and the project owner's decisions; these win over `MISSION.md` |
| `STATUS.md` | Where the work stands right now. Its figures block is generated - do not hand-edit it, and do not append batch notes to this file |
| `STATUS-LOG.md` | Mistakes worth remembering, kept out of `STATUS.md` so it stays a status file |
| `COVERAGE.md` | The coverage dashboard, generated from `coverage.jsonl` |
| `coverage.jsonl` | Machine-readable inventory, one record per documentation item |
| `QUEUE.md` | Pending work in priority order |
| `BLOCKERS.md` | Things that cannot be finished, and why |
| `VERIFICATION.md` | What each verification state means and what evidence it needs |
| `SCREENSHOTS.md` | Screenshot inventory and capture method |
| `DECISIONS.md` | Documentation decisions worth remembering |
| `HANDOFF.md` | Resume point for the next session |
| `tools/` | The two scripts that keep the inventory and dashboard honest |

## Regenerating the dashboard

```sh
python3 documentation/agent/tools/seed_inventory.py \
        /home/tim/workspace/NebulaOS documentation/agent/coverage.jsonl
python3 documentation/agent/tools/render_dashboard.py \
        documentation/agent/coverage.jsonl documentation/agent/COVERAGE.md
```

`seed_inventory.py` re-reads the source trees and adds newly discovered items. It never
changes a status that is already recorded, so re-running it cannot erase progress.
