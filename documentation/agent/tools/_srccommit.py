"""The commit a generated reference describes - the *code*, not this agent's branch.

These generators read a worktree that sits on a `docs/*` branch. That branch
carries documentation commits and merges on top of the code, so its `HEAD` is a
prose commit. Recording it meant a reference saying "generated from <sha>" where
<sha> is a page of Markdown: a citation that looks checkable and leads nowhere.

The same mistake was found and fixed in `seed_inventory.py` on 2026-11-02; the
four generators kept it until 2026-11-03. So: resolve the tip of the branch the
documentation describes, and fall back to HEAD only when no such ref exists -
with the fallback made visible rather than silent.
"""
import subprocess

# repository directory name -> its default branch
DEFAULT_BRANCH = {
    "NebulaOS-kernel": "openke",
}


def _run(args):
    return subprocess.run(args, capture_output=True, text=True).stdout.strip()


def source_commit(root, branch=None):
    """(sha, how) for the code in `root`. `how` is "origin/<branch>" or "HEAD"."""
    if branch is None:
        name = root.rstrip("/").rsplit("/", 1)[-1]
        branch = DEFAULT_BRANCH.get(name, "main")
    sha = _run(["git", "-C", root, "rev-parse", f"origin/{branch}"])
    if sha:
        return sha, f"origin/{branch}"
    return _run(["git", "-C", root, "rev-parse", "HEAD"]), "HEAD"
