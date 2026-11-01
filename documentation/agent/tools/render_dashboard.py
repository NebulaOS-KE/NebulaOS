#!/usr/bin/env python3
"""Render COVERAGE.md from coverage.jsonl.

Every number below is counted from the inventory.  Nothing is estimated.
Code, test, hardware and screenshot verification are reported separately on
purpose - they must never be blended into one flattering percentage.

Usage:  render_dashboard.py <coverage.jsonl> <COVERAGE.md>
"""
import collections, datetime, json, os, sys

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
        ["Blocked (cannot proceed without hardware, access or a decision)",
         sum(1 for i in items if i.get("blockers")),
         f"{100*sum(1 for i in items if i.get('blockers'))//max(n,1)}%"],
        ["Has a recorded completeness gap (work not done, not stuck)",
         sum(1 for i in items if i.get("gaps")),
         f"{100*sum(1 for i in items if i.get('gaps'))//max(n,1)}%"],
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
    rows = [
        ["Captured and confirmed current", sc.get("captured", 0)],
        ["Verified against the running UI", sc.get("verified", 0)],
        ["Candidate image exists, version unconfirmed",
         sc.get("candidate-unconfirmed", 0)],
        ["Missing outright", sc.get("missing", 0)],
        ["Outdated", sc.get("outdated", 0)],
        ["Blocked (needs real hardware)", sc.get("blocked", 0)],
    ]
    A(table(["Measure", "Items"], [["Required", len(need)]] + rows))
    A("")
    # Self-check. An unrecognised screenshot_status used to vanish from this
    # table, leaving the rows silently failing to add up to the required total -
    # which is the one thing a coverage dashboard must never do. If this fires,
    # add the new status to the rows above rather than ignoring it.
    counted = sum(r[1] for r in rows)
    if counted != len(need):
        leaked = sorted(set(sc) - {"captured", "verified",
                                   "candidate-unconfirmed", "missing",
                                   "outdated", "blocked"})
        A(f"> **Dashboard self-check failed.** {len(need)} items require a "
          f"screenshot but only {counted} are accounted for above. "
          f"Unreported status values: {', '.join(leaked) or 'none'}. "
          "Fix `render_dashboard.py` rather than trusting this table.")
        A("")
        print(f"WARNING: screenshot rows sum to {counted}, required is "
              f"{len(need)}; unreported: {leaked}")
    A("A *candidate* is not coverage. It means a real image exists but has not "
      "been confirmed against the commit this documentation describes, so it "
      "cannot yet be trusted to show the reader what they will see.")
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
    A("Only genuine blockers: something that cannot proceed without hardware, "
      "access or a decision this agent cannot make. Work that is simply not "
      "finished is a *completeness gap*, counted separately above - conflating "
      "the two made this dashboard report 57% \"blocked\", which reads as a "
      "stuck project rather than one in progress.")
    A("")
    if not bl:
        A("None recorded.")
    else:
        A(table(["Item", "Repository", "Reason"],
                [[i["id"], i["repo"], i["blockers"]] for i in bl]))
    A("")
    open(out, "w").write("\n".join(L) + "\n")
    print(f"dashboard: {n} items -> {out}")

    # Keep STATUS.md's factual block in step with the inventory.
    #
    # It drifted badly once: STATUS.md was edited by appending a section per
    # batch until it was 557 lines long, with a summary at the top still saying
    # "510 items, all missing, no pages written" while the dashboard said
    # otherwise. An append-only status file becomes a changelog, and its oldest
    # paragraph is the one a reader sees first. So the numbers now come from
    # here, between markers, and nothing hand-written sits above them.
    status = os.path.join(os.path.dirname(out), "STATUS.md")
    if os.path.exists(status):
        txt = open(status).read()
        start, end = "<!-- BEGIN GENERATED STATUS -->", "<!-- END GENERATED STATUS -->"
        if start in txt and end in txt:
            doc = sum(1 for i in items if i["doc_status"] in DOC_DONE)
            blk = [start,
                   f"*Figures generated {datetime.date.today().isoformat()} from "
                   f"`coverage.jsonl` by `tools/render_dashboard.py`. Do not edit "
                   f"this block by hand.*",
                   "",
                   "| | |", "|---|---|",
                   f"| Discovered items | **{n}** |",
                   f"| Documented | **{doc}** ({100*doc//max(n,1)}%) |",
                   f"| Draft | {sum(1 for i in items if i['doc_status']=='draft')} |",
                   f"| Missing | {sum(1 for i in items if i['doc_status']=='missing')} |",
                   f"| Code verified | {sum(1 for i in items if i.get('verify_code')=='verified')} |",
                   f"| Test verified | {sum(1 for i in items if i.get('verify_test')=='verified')} |",
                   f"| Hardware verified | {sum(1 for i in items if i.get('verify_hardware')=='verified')} |",
                   f"| Screenshots required / captured | "
                   f"{sum(1 for i in items if i.get('screenshot_required'))} / "
                   f"{sum(1 for i in items if i.get('screenshot_status')=='captured')} |",
                   f"| Blocked (cannot proceed) | {sum(1 for i in items if i.get('blockers'))} |",
                   f"| Completeness gaps (work not done) | {sum(1 for i in items if i.get('gaps'))} |",
                   "",
                   "Per-repository and per-category breakdowns are in `COVERAGE.md`.",
                   end]
            pre, _, rest = txt.partition(start)
            _, _, post = rest.partition(end)
            open(status, "w").write(pre + "\n".join(blk) + post)
            print(f"status block refreshed in {status}")


if __name__ == "__main__":
    main()
