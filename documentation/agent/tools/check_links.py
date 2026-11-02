#!/usr/bin/env python3
"""Validate the manual's internal links, image references and sidebar.

Pass --external to also check that every http(s) link resolves. That is off by
default because it needs the network and is slow, but it is worth running before
publishing: two links in this manual pointed at
github.com/NebulaOS-KE/NebulaOS-nebulascreen/wiki/<Page> and returned 404,
because that repository's GitHub wiki is not published - the pages exist only as
files in its wiki/ directory. The in-repo blob URLs work today and do not depend
on anyone running a wiki publish step.

What this proves: every relative link points at a page that exists, and every
referenced image file is present. What it cannot prove: that a page says
anything true, or that a screenshot shows the screen it claims to. Those need
source verification and a human eye respectively.

Exits non-zero if anything is broken, so it can gate a pull request.

Usage:  check_links.py <wiki-dir>
"""
import os, re, sys, glob

LINK = re.compile(r'\]\(([^)\s]+)\)')
IMG = re.compile(r'!\[[^\]]*\]\(([^)\s]+)\)')


def check_external(wiki):
    """Every http(s) link, with its status. Needs the network."""
    import subprocess
    urls = set()
    for f in glob.glob(os.path.join(wiki, "*.md")):
        for u in re.findall(r'https?://[^)\s]+', open(f).read()):
            u = u.rstrip(".,`\"'")
            # Skip documentation placeholders - http://<printer-ip> and
            # http://<printer-name>.local are examples a reader substitutes
            # into, not addresses that resolve from here.
            if "<" in u or ">" in u:
                continue
            urls.add(u)
    bad = []
    for u in sorted(urls):
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                            "--max-time", "15", u], capture_output=True, text=True)
        code = r.stdout.strip()
        if code not in ("200", "301", "302"):
            bad.append((u, code or "no response"))
    print(f"{len(urls)} external links checked")
    for u, code in bad:
        print(f"  {code:>14}  {u}")
    return bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    external = "--external" in sys.argv
    wiki = args[0] if args else "wiki"
    pages = {os.path.basename(f)[:-3] for f in glob.glob(os.path.join(wiki, "*.md"))}
    problems = []
    for f in sorted(glob.glob(os.path.join(wiki, "*.md"))):
        text = open(f).read()
        name = os.path.basename(f)
        for target in IMG.findall(text):
            if target.startswith(("http://", "https://")):
                continue
            if not os.path.exists(os.path.join(wiki, target)):
                problems.append((name, "missing image", target))
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            page = target.split("#")[0]
            if not page:
                continue
            if page.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
                continue
            if page not in pages:
                problems.append((name, "missing page", page))

    if not os.path.exists(os.path.join(wiki, "_Sidebar.md")):
        problems.append(("_Sidebar.md", "missing file", "navigation sidebar"))
    else:
        linked = {t.split("#")[0] for t
                  in LINK.findall(open(os.path.join(wiki, "_Sidebar.md")).read())
                  if not t.startswith(("http", "mailto:", "#"))}
        for p in sorted(pages):
            if p not in linked and not p.startswith("_"):
                problems.append(("_Sidebar.md", "page not in navigation", p))

    if external:
        problems += [(u, "external link", code) for u, code in check_external(wiki)]

    print(f"{len(pages)} pages checked in {wiki}/")
    if problems:
        for where, kind, what in problems:
            print(f"  {kind:24s} {what}   (in {where})")
        print(f"\n{len(problems)} problem(s)")
        return 1
    print("no broken links, no missing images, every page reachable from the sidebar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
