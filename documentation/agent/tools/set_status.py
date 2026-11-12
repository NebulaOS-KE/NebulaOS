#!/usr/bin/env python3
"""Set fields on coverage.jsonl entries by id.

Exists so that statuses are changed deliberately and visibly, one id at a time,
rather than by hand-editing JSONL where a typo is invisible.

Usage:  set_status.py <coverage.jsonl> <id> key=value [key=value ...]
"""
import json, sys

def main():
    path, ident = sys.argv[1], sys.argv[2]
    updates = {}
    for arg in sys.argv[3:]:
        k, v = arg.split("=", 1)
        if v in ("true", "false"):
            v = v == "true"
        elif v.isdigit():
            v = int(v)
        elif v.startswith("[") and v.endswith("]"):
            v = [x for x in v[1:-1].split("|") if x]
        updates[k] = v
    rows = [json.loads(l) for l in open(path) if l.strip()]
    hit = 0
    for r in rows:
        if r["id"] == ident:
            r.update(updates)
            hit += 1
    if not hit:
        print(f"ERROR: no entry with id {ident!r}")
        return 1
    with open(path, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(f"updated {ident}: {updates}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
