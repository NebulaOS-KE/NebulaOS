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

Anchors (#fragment) are checked against GitHub's heading slugs. A page that
contains the marker <!-- moved-page-stub --> is a pointer left at an old name
so outside links still land; it need not be in the sidebar, and no other page
may link it.

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


STUB = "<!-- moved-page-stub -->"


def slug(heading):
    """GitHub's heading anchor: lower case, punctuation and emoji dropped,
    spaces to hyphens (runs are not collapsed)."""
    h = re.sub(r'[`*_]', '', heading.strip().lower())
    h = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', h)
    h = ''.join(c for c in h if c.isalnum() or c in ' -')
    return h.replace(' ', '-')


def anchors(text):
    out, seen = set(), {}
    in_code = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            continue
        m = re.match(r'#{1,6}\s+(.*)', line)
        if m and not in_code:
            a = slug(m.group(1))
            n = seen.get(a, 0)
            seen[a] = n + 1
            out.add(a if n == 0 else f"{a}-{n}")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    external = "--external" in sys.argv
    wiki = args[0] if args else "wiki"
    pages = {os.path.basename(f)[:-3] for f in glob.glob(os.path.join(wiki, "*.md"))}
    problems = []
    texts = {os.path.basename(f)[:-3]: open(f).read()
             for f in glob.glob(os.path.join(wiki, "*.md"))}
    stubs = {p for p, t in texts.items() if STUB in t}
    page_anchors = {p: anchors(t) for p, t in texts.items()}
    for f in sorted(glob.glob(os.path.join(wiki, "*.md"))):
        text = open(f).read()
        name = os.path.basename(f)
        me = name[:-3]
        for target in IMG.findall(text):
            if target.startswith(("http://", "https://")):
                continue
            if not os.path.exists(os.path.join(wiki, target)):
                problems.append((name, "missing image", target))
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            page, _, frag = target.partition("#")
            if page.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
                continue
            if page and page not in pages:
                problems.append((name, "missing page", page))
                continue
            dest = page or me
            if frag and dest in page_anchors and frag not in page_anchors[dest]:
                problems.append((name, "missing anchor", f"{dest}#{frag}"))
            # A moved page is only a landing spot for old outside links; the
            # manual itself must link the new place.
            if page in stubs and me not in stubs and not me.startswith("_"):
                problems.append((name, "links a moved-page stub", page))

    if not os.path.exists(os.path.join(wiki, "_Sidebar.md")):
        problems.append(("_Sidebar.md", "missing file", "navigation sidebar"))
    else:
        linked = {t.split("#")[0] for t
                  in LINK.findall(open(os.path.join(wiki, "_Sidebar.md")).read())
                  if not t.startswith(("http", "mailto:", "#"))}
        for p in sorted(pages):
            if p not in linked and not p.startswith("_") and p not in stubs:
                problems.append(("_Sidebar.md", "page not in navigation", p))

    if external:
        problems += [(u, "external link", code) for u, code in check_external(wiki)]

    print(f"{len(pages)} pages checked in {wiki}/ ({len(stubs)} moved-page stubs)")
    if problems:
        for where, kind, what in problems:
            print(f"  {kind:24s} {what}   (in {where})")
        print(f"\n{len(problems)} problem(s)")
        return 1
    print("no broken links, no missing images, every page reachable from the sidebar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
