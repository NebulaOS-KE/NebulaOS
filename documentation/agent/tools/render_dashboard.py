#!/usr/bin/env python3
"""Render COVERAGE.md from coverage.jsonl.

Every number below is counted from the inventory.  Nothing is estimated.
Code, test, hardware and screenshot verification are reported separately on
purpose - they must never be blended into one flattering percentage.

Usage:  render_dashboard.py <coverage.jsonl> <COVERAGE.md>
"""
import json, sys, collections, datetime

DOC_DONE = ("documented", "verified")


def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def tally(items, field):
    c = collections.Counter(i.get(field) or "unset" for i in items)
    return c


def main():
    src, out = sys.argv[1], sys.argv[2]
    items = load(src)
    n = len(items)
    ds = tally(items, "doc_status")
    L = []
    A = L.append
    A("# NebulaOS documentation coverage dashboard")
    A("")
    A(f"Generated {datetime.date.today().isoformat()} by "
      "`documentation/agent/tools/render_dashboard.py` from "
      "`documentation/agent/coverage.jsonl`.")
    A("")
    A("**Read this first.** Coverage is relative to the *discovered* inventory, "
      "not to some imagined complete list of everything NebulaOS does. Each "
      "entry records the exact source commit it was discovered at. A rise in "
      "the total item count is normal and healthy: it means discovery found "
      "more real functionality, not that documentation regressed.")
    A("")
    A("Verification is reported in four separate columns because they prove "
      "different things. *Code verified* means the implementation was read. "
      "*Test verified* means a test in the repository covers it. *Hardware "
      "verified* means it was observed on a real printer - this agent has no "
      "printer access, so that column is expected to stay low and is honest "
      "about it. *Screenshot* tracks real captured images only.")
    A("")

    # ---- overall -----------------------------------------------------------
    A("## Overall")
    A("")
    A(table(["Measure", "Items", "Share"], [
        ["Discovered documentation items", n, "100%"],
        ["Documented (page exists and covers the item)",
         sum(1 for i in items if i["doc_status"] in DOC_DONE),
         f"{100*sum(1 for i in items if i['doc_status'] in DOC_DONE)//max(n,1)}%"],
        ["Draft", ds.get("draft", 0), f"{100*ds.get('draft',0)//max(n,1)}%"],
        ["Missing", ds.get("missing", 0), f"{100*ds.get('missing',0)//max(n,1)}%"],
        ["Blocked", sum(1 for i in items if i.get("blockers")),
         f"{100*sum(1 for i in items if i.get('blockers'))//max(n,1)}%"],
    ]))
    A("")

    # ---- verification ------------------------------------------------------
    A("## Verification (counted separately, never combined)")
    A("")
    rows = []
    for field, label in [("verify_code", "Code verified"),
                         ("verify_test", "Test verified"),
                         ("verify_hardware", "Hardware verified")]:
        c = tally(items, field)
        rows.append([label, c.get("verified", 0), c.get("partial", 0),
                     c.get("unknown", 0) + c.get("unset", 0),
                     c.get("blocked", 0), c.get("n/a", 0)])
    A(table(["Kind", "Verified", "Partial", "Unknown", "Blocked", "N/A"], rows))
    A("")

    # ---- screenshots -------------------------------------------------------
    need = [i for i in items if i.get("screenshot_required")]
    sc = tally(need, "screenshot_status")
    A("## Screenshots")
    A("")
    A(table(["Measure", "Items"], [
        ["Required", len(need)],
        ["Captured", sc.get("captured", 0)],
        ["Verified against the running UI", sc.get("verified", 0)],
        ["Missing", sc.get("missing", 0)],
        ["Outdated", sc.get("outdated", 0)],
        ["Blocked (needs real hardware)", sc.get("blocked", 0)],
    ]))
    A("")

    # ---- per repository ----------------------------------------------------
    A("## By repository")
    A("")
    rows = []
    for repo in sorted({i["repo"] for i in items}):
        g = [i for i in items if i["repo"] == repo]
        d = sum(1 for i in g if i["doc_status"] in DOC_DONE)
        rows.append([repo, len(g), d,
                     sum(1 for i in g if i["doc_status"] == "draft"),
                     sum(1 for i in g if i["doc_status"] == "missing"),
                     sum(1 for i in g if i.get("verify_code") == "verified"),
                     f"{100*d//max(len(g),1)}%"])
    A(table(["Repository", "Items", "Documented", "Draft", "Missing",
             "Code verified", "Documented %"], rows))
    A("")

    # ---- per category ------------------------------------------------------
    A("## By category")
    A("")
    rows = []
    for cat in sorted({i["category"] for i in items}):
        g = [i for i in items if i["category"] == cat]
        d = sum(1 for i in g if i["doc_status"] in DOC_DONE)
        rows.append([cat, len(g), d,
                     sum(1 for i in g if i["doc_status"] == "draft"),
                     sum(1 for i in g if i["doc_status"] == "missing"),
                     f"{100*d//max(len(g),1)}%"])
    A(table(["Category", "Items", "Documented", "Draft", "Missing",
             "Documented %"], rows))
    A("")

    # ---- source revisions used for discovery -------------------------------
    A("## Source revisions this inventory was discovered at")
    A("")
    rows = []
    seen = {}
    for i in items:
        k = (i["repo"], i.get("source_branch"), i.get("source_commit"))
        seen[k] = seen.get(k, 0) + 1
    for (repo, br, c), cnt in sorted(seen.items()):
        rows.append([repo, br or "-", (c or "not cloned locally")[:12], cnt])
    A(table(["Repository", "Branch", "Commit", "Items"], rows))
    A("")

    # ---- blockers ----------------------------------------------------------
    bl = [i for i in items if i.get("blockers")]
    A("## Blocked items")
    A("")
    if not bl:
        A("None recorded.")
    else:
        A(table(["Item", "Repository", "Reason"],
                [[i["id"], i["repo"], i["blockers"]] for i in bl]))
    A("")
    open(out, "w").write("\n".join(L) + "\n")
    print(f"dashboard: {n} items -> {out}")


if __name__ == "__main__":
    main()
