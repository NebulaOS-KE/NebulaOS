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
    # The central repo is cloned at _worktrees/docs/NebulaOS - this agent's
    # own branch lives there. Naming it here means its items carry a real
    # commit instead of "not cloned locally".
    "NebulaOS":                    ("main",   "NebulaOS"),
    "NebulaOS-firmware":           ("main",   "NebulaOS-firmware"),
    "NebulaOS-nebulascreen":       ("main",   "NebulaOS-nebulascreen"),
    "NebulaOS-klipper-extensions": ("main",   "NebulaOS-klipper-extensions"),
    "NebulaOS-klipper-mcu":        ("main",   "NebulaOS-klipper-mcu"),
    "NebulaOS-kernel":             ("openke", "NebulaOS-kernel"),
    "nebulaos-packages":           ("main",   None),
    "lv_drivers":                  ("master", None),
}

# G-code commands whose registered name is assembled from a module constant, so
# the literal-string scan below cannot see them. Each entry was resolved by
# reading the module and is listed with the constant it comes from, so the
# mapping can be re-checked rather than trusted.
RESOLVED_COMMANDS = {
    "_NEBULAOS_BED_TRAM":            ("nebulaos_bed_tram.py", "'_' + CMD"),
    "_NEBULAOS_BED_TRAM_CANCEL":     ("nebulaos_bed_tram.py", "CANCEL"),
    "NEBULAOS_BED_TRAM":             ("nebulaos_bed_tram.py", "CMD (wrapper macro name)"),
    "_NEBULAOS_LOAD_CELL_CALIBRATE": ("nebulaos_load_cell_calibration.py", "'_' + CMD"),
    "_NEBULAOS_LOAD_CELL_CANCEL":    ("nebulaos_load_cell_calibration.py", "CANCEL"),
    "NEBULAOS_LOAD_CELL_MODE":       ("nebulaos_load_cell_calibration.py", "MODE_CMD"),
    "NEBULAOS_LOAD_CELL_AUTO_CHECK": ("nebulaos_load_cell_calibration.py", "CHECK_CMD"),
    "NEBULAOS_Z_ADJUST":             ("nebulaos_z_adjust.py", "CMD"),
}

BLANK = dict(
    doc_page=None, doc_status="missing", verify_code="unknown",
    verify_test="unknown", verify_hardware="n/a",
    screenshot_required=False, screenshot_status="n/a",
    evidence=[], last_verified=None, blockers=[], priority=3,
)


def checkout_path(root, checkout):
    """Where to read a repository's source from.

    Prefer this agent's own pinned worktree under _worktrees/docs/ over the
    checkout at the workspace root. The root checkouts belong to the foreground
    development session and move without warning - on 2026-11-01 the firmware
    one was already a commit ahead of the SHA this inventory had recorded.
    Reading evidence from a tree that can change under you means the recorded
    commit stops matching the content it describes, silently.
    """
    if not checkout:
        return None
    own = os.path.join(root, "_worktrees", "docs", checkout)
    if os.path.isdir(os.path.join(own, ".git")) or os.path.exists(
            os.path.join(own, ".git")):
        return own
    p = os.path.join(root, checkout)
    return p if os.path.isdir(p) else None


def sha(root, checkout):
    """The *code* commit an item was discovered at.

    Not the worktree's HEAD. These worktrees sit on this agent's own `docs/*`
    branches, which carry documentation commits and merges on top of the code.
    Recording HEAD meant the inventory cited a documentation commit as the
    source of a code fact - so anyone checking the SHA would find prose, not
    the implementation it described.

    So: the tip of the branch the documentation describes (`origin/<default>`),
    falling back to HEAD only where no such ref exists.
    """
    p = checkout_path(root, checkout)
    if not p:
        return None
    branch = None
    for repo, (b, c) in REPOS.items():
        if c == checkout:
            branch = b
            break
    if branch:
        out = subprocess.run(["git", "-C", p, "rev-parse", f"origin/{branch}"],
                             capture_output=True, text=True).stdout.strip()
        if out:
            return out
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
    fw = checkout_path(root, "NebulaOS-firmware") or ""

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
    src = os.path.join(checkout_path(root, "NebulaOS-nebulascreen") or "", "src")
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
    ext = os.path.join(checkout_path(root, "NebulaOS-klipper-extensions") or "", "extras")
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
        for n, (mod, const) in RESOLVED_COMMANDS.items():
            found.setdefault(n, []).append(f"extras/{mod}")
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

    # --- Klipper extension configuration keys -------------------------------
    if os.path.isdir(ext):
        cfg = re.compile(
            r"config\.get(float|int|boolean|lists?|choice|_name|)\("
            r"\s*['\"]([a-z0-9_]+)['\"]")
        for f in sorted(os.listdir(ext)):
            if not f.endswith(".py") or f.startswith("test_"):
                continue
            section = f[:-3]
            seen = set()
            for m in cfg.finditer(open(os.path.join(ext, f)).read()):
                key = m.group(2)
                if key in seen:
                    continue
                seen.add(key)
                kind = {"": "string", "float": "float", "int": "int",
                        "boolean": "bool", "list": "list", "lists": "list",
                        "choice": "choice", "_name": "name"}[m.group(1)]
                items.append(rec(
                    f"config:{section}:{key}", "NebulaOS-klipper-extensions",
                    "klipper-extensions",
                    f"Config option [{section}] {key} ({kind})",
                    "config-option", [f"extras/{f}"],
                    shas["NebulaOS-klipper-extensions"], "main", priority=2))

    # --- NebulaScreen configuration keys ------------------------------------
    # Only real settings, which means two places and no more: the keys the
    # config schema itself touches (src/config.cpp / config.h, where the
    # defaults are applied) and the keys any panel reads through the Config
    # object. A blind sweep for `_json_pointer` across the whole UI is wrong -
    # most of those pointers address Moonraker response and status objects, not
    # settings, and counting them as configuration would inflate the inventory
    # with items that do not exist. The API surface is discovered separately.
    nsrc = os.path.join(checkout_path(root, "NebulaOS-nebulascreen") or "", "src")
    if os.path.isdir(nsrc):
        schema = re.compile(r'"(/[a-z0-9_]+)"_json_pointer')
        viaconf = re.compile(r'get(?:<[^>]*>)?\(\s*"(/[a-z0-9_]+)"')
        keys = set()
        for f in ("config.cpp", "config.h"):
            fp = os.path.join(nsrc, f)
            if os.path.exists(fp):
                txt = open(fp, errors="replace").read()
                keys.update(m.group(1) for m in schema.finditer(txt))
                keys.update(m.group(1) for m in viaconf.finditer(txt))
        # A setting is anything read or written through the Config object:
        # get, get_json and set all name real keys. Writes matter as much as
        # reads - a toggle the UI stores is a setting even if only one panel
        # reads it back.
        conf_call = re.compile(
            r'(?:Config::get_instance\(\)|(?:conf|config|_conf|cfg)\w*)'
            r'(?:->|\.)(?:get|get_json|set)[A-Za-z_]*(?:<[^>]*>)?'
            r'\(\s*"(/[a-z0-9_]+)"')
        for f in sorted(os.listdir(nsrc)):
            if not f.endswith((".cpp", ".h")):
                continue
            keys.update(m.group(1) for m in conf_call.finditer(
                open(os.path.join(nsrc, f), errors="replace").read()))
        for k in sorted(keys):
            items.append(rec(
                f"nsconfig:{k}", "NebulaOS-nebulascreen", "nebulascreen-config",
                f"NebulaScreen setting {k}", "config-option",
                ["src/config.cpp", "src/config.h"],
                shas["NebulaOS-nebulascreen"], "main", priority=2))

    # --- NebulaOS Moonraker API (the public OS-settings surface) -------------
    # The authoritative list is the registration table in the Moonraker
    # component, not the call sites in the UI: the UI is one client among
    # several, and an endpoint nobody calls yet is still public API.
    # Moonraker exposes each HTTP path /machine/nebulaos/x/y as the JSON-RPC
    # method machine.nebulaos.x.y, which is how NebulaScreen addresses them.
    comp = os.path.join(fw, "scripts/build/overlay",
                        "usr/lib/nebulaos/moonraker/nebulaos.py")
    if os.path.exists(comp):
        txt = open(comp).read()
        # NOTE: the character class must include digits. Without 0-9 it
        # silently drops /machine/nebulaos/network/ipv4 - a dropped endpoint
        # looks exactly like an endpoint that does not exist.
        tbl = re.compile(r'\(\s*"(/machine/nebulaos/[a-z0-9_/]+)"\s*,'
                         r'\s*RequestType\.([A-Z|_ ]+?)\s*,\s*self\.(\w+)')
        for path, rt, handler in tbl.findall(txt):
            rpc = path.lstrip("/").replace("/", ".")
            items.append(rec(
                f"api:{rpc}", "NebulaOS-firmware", "nebulaos-moonraker-api",
                f"Moonraker method {rpc} ({rt.strip()})", "api",
                ["scripts/build/overlay/usr/lib/nebulaos/moonraker/"
                 "nebulaos.py"],
                shas["NebulaOS-firmware"], "main", priority=2,
                evidence=[f"NebulaOS-firmware@{(shas['NebulaOS-firmware'] or '')[:7]}:"
                          f"scripts/build/overlay/usr/lib/nebulaos/moonraker/"
                          f"nebulaos.py#{handler}"]))
        for note in re.findall(r'register_notification\(\s*"([^"]+)"', txt):
            items.append(rec(
                f"api:notification:{note}", "NebulaOS-firmware",
                "nebulaos-moonraker-api",
                f"Moonraker notification {note}", "api",
                ["scripts/build/overlay/usr/lib/nebulaos/moonraker/"
                 "nebulaos.py"],
                shas["NebulaOS-firmware"], "main", priority=2))

    # --- nebulaos_osconfig helper modules (what the API delegates to) --------
    osc = os.path.join(fw, "scripts/build/overlay",
                       "usr/lib/nebulaos/python/nebulaos_osconfig")
    if os.path.isdir(osc):
        for f in sorted(os.listdir(osc)):
            if not f.endswith(".py") or f == "__init__.py":
                continue
            items.append(rec(
                f"osconfig:{f[:-3]}", "NebulaOS-firmware", "nebulaos-osconfig",
                f"OS settings helper module: {f}", "os-helper",
                [f"scripts/build/overlay/usr/lib/nebulaos/python/"
                 f"nebulaos_osconfig/{f}"],
                shas["NebulaOS-firmware"], "main", priority=2))

    # --- firmware init scripts / services -----------------------------------
    initd = os.path.join(fw, "scripts/build/overlay/etc/init.d")
    if os.path.isdir(initd):
        for f in sorted(os.listdir(initd)):
            if not re.match(r"S\d\d", f):
                continue
            items.append(rec(
                f"service:{f}", "NebulaOS-firmware", "firmware-init",
                f"Boot service: {f}", "service",
                [f"scripts/build/overlay/etc/init.d/{f}"],
                shas["NebulaOS-firmware"], "main", priority=2))

    # --- existing NebulaScreen wiki pages, with a reuse disposition ---------
    # Audited page by page on 2026-10-31 (Q-006). The wiki is good: real file
    # paths, exact error strings, and safety notes written by someone who had
    # actually done the procedure. It is reused, not replaced.
    #
    # "move" = end-user material that belongs in the central manual
    # "adapt" = end-user material needing rework or merging before it moves
    # "keep"  = developer material that stays in the component wiki
    # "historical" = describes something NebulaOS does not have; keep as a
    #                signpost, do not carry into the manual
    WIKI = {
        "Installing-NebulaOS.md":     ("move", "02-installation"),
        "Updating-NebulaOS.md":       ("move", "08-updates"),
        "Recovery.md":                ("move", "10-recovery"),
        "Resetting.md":               ("move", "08-updates"),
        "Troubleshooting.md":         ("move", "09-troubleshooting"),
        "Using-NebulaScreen.md":      ("adapt", "04-nebulascreen"),
        "Calibration-Guide.md":       ("move", "05-calibration"),
        "Calibration-Explained.md":   ("move", "05-calibration"),
        "Bed-Tramming.md":            ("move", "05-calibration"),
        "Load-Cell-Calibration.md":   ("move", "05-calibration"),
        "Axis-Twist-Compensation.md": ("move", "05-calibration"),
        "Skew-Correction.md":         ("move", "05-calibration"),
        "TMC-Autotune.md":            ("move", "07-advanced"),
        "Adaptive-Print-Setup.md":    ("move", "07-advanced"),
        "Camera-Image-Tuning.md":     ("move", "07-advanced"),
        "Buzzer-and-Sounds.md":       ("move", "07-advanced"),
        "Home.md":                    ("keep", "component navigation"),
        "_Sidebar.md":                ("keep", "component navigation"),
        "Installation.md":            ("keep", "component files and paths"),
        "Architecture.md":            ("keep", "developer"),
        "Building-from-Source.md":    ("keep", "developer"),
        "Development-and-Simulator.md": ("keep", "developer"),
        "Configuration.md":           ("keep", "developer"),
        "Config-and-Theme.md":        ("keep", "developer"),
        "Releases-and-Deployment.md": ("keep", "developer"),
        "Testing.md":                 ("keep", "developer"),
        "CI.md":                      ("keep", "developer"),
        "Contributing.md":            ("keep", "developer"),
        "Vendored-Dependencies.md":   ("keep", "developer"),
        "Integration-with-NebulaOS.md": ("keep", "developer"),
        "Wiki-Publishing.md":         ("keep", "developer"),
        "History-and-Credits.md":     ("keep", "developer"),
        "Upgrading.md":               ("historical", "redirect stub"),
        "Emergency-Factory-Reset.md": ("historical", "documents an absence"),
    }
    wdir = os.path.join(checkout_path(root, "NebulaOS-nebulascreen") or "", "wiki")
    if os.path.isdir(wdir):
        for f in sorted(os.listdir(wdir)):
            if not f.endswith(".md"):
                continue
            disp, dest = WIKI.get(f, ("unaudited", "-"))
            items.append(rec(
                f"existing:{f}", "NebulaOS-nebulascreen", "existing-wiki",
                f"Existing wiki page {f} -> {disp} ({dest})", "existing-page",
                [f"wiki/{f}"], shas["NebulaOS-nebulascreen"], "main",
                priority=1 if disp in ("move", "adapt") else 3,
                blockers="" if disp != "unaudited"
                        else "discovered after the Q-006 audit; needs a disposition"))

    # --- firmware build pipeline --------------------------------------------
    bld = os.path.join(fw, "scripts/build")
    if os.path.isdir(bld):
        for f in sorted(os.listdir(bld)):
            if not f.endswith(".sh"):
                continue
            items.append(rec(
                f"buildscript:{f}", "NebulaOS-firmware", "firmware-build",
                f"Build pipeline script: {f}", "build-command",
                [f"scripts/build/{f}"], shas["NebulaOS-firmware"], "main",
                priority=2))

    # --- firmware developer and operator tooling ----------------------------
    tools = os.path.join(fw, "tools")
    if os.path.isdir(tools):
        for d in sorted(os.listdir(tools)):
            dp = os.path.join(tools, d)
            if os.path.isdir(dp):
                files = sorted(f for f in os.listdir(dp)
                               if f.endswith((".sh", ".py")))
                if not files:
                    continue
                items.append(rec(
                    f"toolset:{d}", "NebulaOS-firmware", "firmware-tools",
                    f"Tooling: tools/{d} ({len(files)} scripts)",
                    "developer-tool", [f"tools/{d}/{f}" for f in files],
                    shas["NebulaOS-firmware"], "main", priority=3))
            elif d.endswith((".sh", ".py")):
                items.append(rec(
                    f"toolset:{d}", "NebulaOS-firmware", "firmware-tools",
                    f"Tooling: tools/{d}", "developer-tool",
                    [f"tools/{d}"], shas["NebulaOS-firmware"], "main",
                    priority=3))

    # --- runtime helpers shipped in the overlay ------------------------------
    # Everything executable in the overlay outside init.d. Note that the
    # ones with ordinary system names - passwd, sudo, supervisorctl,
    # sftp-server, git - are NOT vendor binaries: each is a NebulaOS shell
    # shim, and `sudo` is explicitly an adapter rather than sudo. They were
    # nearly filtered out as third-party noise; they are in fact some of the
    # most surprising things in the image and a developer who assumes
    # otherwise will be badly misled. They stay in the inventory.
    ov = os.path.join(fw, "scripts/build/overlay")
    if os.path.isdir(ov):
        skip_ext = (".conf", ".cfg", ".json", ".txt", ".png", ".service")
        for dirpath, _dirnames, filenames in os.walk(ov):
            if "init.d" in dirpath:
                continue
            for f in sorted(filenames):
                full = os.path.join(dirpath, f)
                if f.endswith(skip_ext):
                    continue
                if not (f.endswith(".sh") or os.access(full, os.X_OK)):
                    continue
                relov = os.path.relpath(full, ov)
                items.append(rec(
                    f"overlay:{relov}", "NebulaOS-firmware", "firmware-runtime",
                    f"Runtime helper: /{relov}", "runtime-helper",
                    [f"scripts/build/overlay/{relov}"],
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
