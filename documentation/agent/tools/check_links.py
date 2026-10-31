#!/usr/bin/env python3
"""Validate the manual's internal links, image references and sidebar.

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


def main():
    wiki = sys.argv[1] if len(sys.argv) > 1 else "wiki"
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
