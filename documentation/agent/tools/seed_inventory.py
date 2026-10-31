#!/usr/bin/env python3
"""Seed / refresh the machine-readable documentation coverage inventory.

Discovery is mechanical: it reads the real source trees and emits one JSONL
record per discovered documentation item.  It never invents items and never
upgrades a status - statuses already present in coverage.jsonl are preserved
so that writing progress is not lost when discovery is re-run.

Usage:  seed_inventory.py <workspace-root> <out.jsonl>
"""
import json, os, re, subprocess, sys, datetime

TODAY = datetime.date.today().isoformat()

REPOS = {
    "NebulaOS":                    ("main",   None),
    "NebulaOS-firmware":           ("main",   "NebulaOS-firmware"),
    "NebulaOS-nebulascreen":       ("main",   "NebulaOS-nebulascreen"),
    "NebulaOS-klipper-extensions": ("main",   "NebulaOS-klipper-extensions"),
    "NebulaOS-klipper-mcu":        ("main",   "NebulaOS-klipper-mcu"),
    "NebulaOS-kernel":             ("openke", "NebulaOS-kernel"),
    "nebulaos-packages":           ("main",   None),
    "lv_drivers":                  ("master", None),
}

BLANK = dict(
    doc_page=None, doc_status="missing", verify_code="unknown",
    verify_test="unknown", verify_hardware="n/a",
    screenshot_required=False, screenshot_status="n/a",
    evidence=[], last_verified=None, blockers=[], priority=3,
)


def sha(root, checkout):
    if not checkout:
        return None
    p = os.path.join(root, checkout)
    if not os.path.isdir(p):
        return None
    return subprocess.run(["git", "-C", p, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip() or None


def rec(id_, repo, component, topic, category, paths, commit, branch, **kw):
    r = dict(id=id_, repo=repo, component=component, topic=topic,
             category=category, source_paths=paths, source_commit=commit,
             source_branch=branch, release_applicability="unknown")
    r.update(BLANK)
    r.update(kw)
    return r


def discover(root):
    items = []
    shas = {r: sha(root, c) for r, (b, c) in REPOS.items()}

    # --- repository-level technical references -------------------------------
    for repo, (branch, checkout) in REPOS.items():
        cat = "user-manual" if repo == "NebulaOS" else "developer-wiki"
        items.append(rec(
            f"repo:{repo}", repo, repo,
            f"{repo}: complete {cat} for this repository", "repo-overview",
            ["<repository root>"], shas[repo], branch, priority=1,
            blockers=[] if checkout or repo == "NebulaOS"
                     else "not cloned locally; clone into _worktrees/docs"
        ))

    # --- end-user manual sections (Part 4.2 of the mission) ------------------
    sections = [
        ("01-start-here",      "Start Here: what NebulaOS is, supported hardware, safety, terminology"),
        ("02-installation",    "Installation: download, choose the file, USB, install from stock / OpenKE, first boot, going back"),
        ("03-first-setup",     "First-time setup: startup, Wi-Fi, finding the IP, Mainsail, first calibration, first print"),
        ("04-nebulascreen",    "Complete NebulaScreen guide: every tab, menu, button, dialog and message"),
        ("05-calibration",     "Calibration: every workflow, what it changes, how to read the result"),
        ("06-printing",        "Everyday printing: upload, start, pause, resume, cancel, filament, temperatures, fans, Z offset"),
        ("07-advanced",        "Advanced features: camera, Spoolman, adaptive meshing, macros, console, power-loss recovery"),
        ("08-updates",         "Updates and maintenance: checking, updating, release notes, resets, backups, rollback"),
        ("09-troubleshooting", "Troubleshooting, organised by what the user sees"),
        ("10-recovery",        "Recovery: boot slots, USB recovery, factory reset, config recovery, data-loss risks"),
    ]
    for sid, topic in sections:
        items.append(rec(f"manual:{sid}", "NebulaOS", "user-manual", topic,
                         "user-manual-section", ["wiki/"], shas["NebulaOS"],
                         "main", priority=1, screenshot_required=True,
                         screenshot_status="missing"))

    # --- NebulaScreen panels (one user-facing screen reference each) ---------
    src = os.path.join(root, "NebulaOS-nebulascreen", "src")
    if os.path.isdir(src):
        for f in sorted(os.listdir(src)):
            if not f.endswith("_panel.cpp"):
                continue
            name = f[:-4]
            items.append(rec(
                f"screen:{name}", "NebulaOS-nebulascreen", "nebulascreen-ui",
                f"NebulaScreen panel: {name}", "screen",
                [f"src/{name}.cpp", f"src/{name}.h"],
                shas["NebulaOS-nebulascreen"], "main", priority=2,
                screenshot_required=True, screenshot_status="missing"))

    # --- Klipper extension G-code commands ----------------------------------
    ext = os.path.join(root, "NebulaOS-klipper-extensions", "extras")
    if os.path.isdir(ext):
        pat = re.compile(r"register_(?:mux_)?command\(\s*(?:'([^']+)'|\"([^\"]+)\")")
        found = {}
        for f in sorted(os.listdir(ext)):
            if not f.endswith(".py") or f.startswith("test_"):
                continue
            for m in pat.finditer(open(os.path.join(ext, f)).read()):
                n = m.group(1) or m.group(2)
                if not re.fullmatch(r"[A-Z_][A-Z0-9_]*", n):
                    continue          # built from a constant - resolve by hand
                found.setdefault(n, []).append(f"extras/{f}")
        for n, paths in sorted(found.items()):
            items.append(rec(
                f"gcode:{n}", "NebulaOS-klipper-extensions", "klipper-extensions",
                f"G-code command: {n}", "command", paths,
                shas["NebulaOS-klipper-extensions"], "main", priority=2))
        # extension modules themselves
        for f in sorted(os.listdir(ext)):
            if not f.endswith(".py") or f.startswith("test_"):
                continue
            items.append(rec(
                f"extension:{f[:-3]}", "NebulaOS-klipper-extensions",
                "klipper-extensions", f"Klipper extension module: {f}",
                "extension", [f"extras/{f}"],
                shas["NebulaOS-klipper-extensions"], "main", priority=2))

    # --- firmware init scripts / services -----------------------------------
    initd = os.path.join(root, "NebulaOS-firmware",
                         "scripts/build/overlay/etc/init.d")
    if os.path.isdir(initd):
        for f in sorted(os.listdir(initd)):
            if not re.match(r"S\d\d", f):
                continue
            items.append(rec(
                f"service:{f}", "NebulaOS-firmware", "firmware-init",
                f"Boot service: {f}", "service",
                [f"scripts/build/overlay/etc/init.d/{f}"],
                shas["NebulaOS-firmware"], "main", priority=2))

    return items


def main():
    root, out = sys.argv[1], sys.argv[2]
    old = {}
    if os.path.exists(out):
        for line in open(out):
            line = line.strip()
            if line:
                r = json.loads(line)
                old[r["id"]] = r
    new = discover(root)
    keep = ("doc_page doc_status verify_code verify_test verify_hardware "
            "screenshot_required screenshot_status evidence last_verified "
            "blockers priority release_applicability").split()
    for r in new:
        o = old.get(r["id"])
        if o:
            for k in keep:
                if k in o:
                    r[k] = o[k]
    seen = {r["id"] for r in new}
    retired = [o for i, o in old.items() if i not in seen]
    for o in retired:
        o["doc_status"] = o.get("doc_status", "missing")
        o["blockers"] = "no longer discovered in source; review and retire"
    allr = new + retired
    with open(out, "w") as fh:
        for r in allr:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(f"inventory: {len(new)} discovered, {len(retired)} retired, "
          f"{len(allr)} total -> {out}")


if __name__ == "__main__":
    main()
