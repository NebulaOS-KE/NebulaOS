#!/usr/bin/env python3
"""Generate the NebulaOS Moonraker API reference from the component source.

Parsed with `ast`. For each registered endpoint it finds the handler function
and extracts the parameters that handler actually reads from the request, with
their literal defaults - so a parameter list cannot be guessed from an endpoint
name, and a default cannot be transcribed wrongly.

What this establishes: the endpoint exists, its HTTP method, its JSON-RPC name,
its handler, and which request parameters that handler reads. What it does not
establish: the response shape (the helper CLI produces it at runtime), or that
any of it works on a printer.

Usage:  gen_firmware_api_reference.py <firmware-checkout> <out-file>
"""
import ast, json, os, subprocess, sys, datetime
import _srccommit
import gen_firmware_api_responses as _resp

COMPONENT = ("scripts/build/overlay/usr/lib/nebulaos/moonraker/nebulaos.py")
GETTERS = {"get_str": "string", "get_int": "int", "get_float": "float",
           "get_boolean": "bool", "get": "any"}


def is_lit(n):
    try:
        ast.literal_eval(n)
        return True
    except Exception:
        return False


def fmt(v):
    if v is None:
        return "`null`"
    if isinstance(v, str):
        return f"`\"{v}\"`" if v else "`\"\"`"
    if isinstance(v, bool):
        return "`true`" if v else "`false`"
    return f"`{v}`"


def handler_params(fn):
    """Parameters a handler reads from the web request."""
    out = {}
    for node in ast.walk(fn):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr not in GETTERS or not node.args:
            continue
        recv = node.func.value
        rname = getattr(recv, "id", None) or getattr(recv, "attr", None)
        if rname not in ("web_request", "req", "request"):
            continue
        if not is_lit(node.args[0]):
            continue
        name = ast.literal_eval(node.args[0])
        if not isinstance(name, str):
            continue
        if len(node.args) > 1:
            d = fmt(ast.literal_eval(node.args[1])) if is_lit(node.args[1]) else "computed"
            req = False
        else:
            d, req = "-", True
        # A parameter read twice in one handler: the stricter reading wins.
        prev = out.get(name)
        if prev and not prev["required"]:
            continue
        out[name] = dict(kind=GETTERS[node.func.attr], default=d, required=req)
    return out


def main():
    root, out = sys.argv[1], sys.argv[2]
    # The code commit, not this worktree's docs branch - see _srccommit.py.
    sha, sha_from = _srccommit.source_commit(root)
    # Response shapes, resolved endpoint -> osconfig helper -> its return keys.
    try:
        routes, calls = _resp.endpoints(os.path.join(root, _resp.COMPONENT))
        disp = _resp.dispatch(os.path.join(root, _resp.OSCONFIG, "cli.py"))
        responses = _resp.resolve(root, routes, calls, disp)
    except Exception as exc:            # never lose the reference over this
        print(f"WARNING: response resolution failed: {exc}")
        responses = {}
    path = os.path.join(root, COMPONENT)
    tree = ast.parse(open(path).read())

    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs[node.name] = node

    endpoints, notifications = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Tuple) and len(node.elts) == 3:
            p, m, h = node.elts
            if not (is_lit(p) and isinstance(ast.literal_eval(p), str)):
                continue
            path_s = ast.literal_eval(p)
            if not path_s.startswith("/machine/nebulaos/"):
                continue
            method = ""
            if isinstance(m, ast.Attribute):
                method = m.attr
            elif isinstance(m, ast.BinOp):      # RequestType.GET | RequestType.POST
                parts = []
                for side in (m.left, m.right):
                    if isinstance(side, ast.Attribute):
                        parts.append(side.attr)
                method = "|".join(parts)
            hname = h.attr if isinstance(h, ast.Attribute) else None
            endpoints.append(dict(path=path_s, method=method, handler=hname,
                                  rpc=path_s.lstrip("/").replace("/", "."),
                                  params=handler_params(funcs[hname]) if hname in funcs else {}))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "register_notification" and node.args \
                and is_lit(node.args[0]):
            notifications.append(ast.literal_eval(node.args[0]))

    endpoints.sort(key=lambda e: e["rpc"])
    # Counted, never typed: this sentence was already wrong once by three.
    unresolved_n = sum(1 for e in endpoints
                       if not (responses.get(e["path"]) or {}).get("result_keys"))
    L = [f"<!-- Generated by documentation/agent/tools/gen_firmware_api_reference.py "
         f"from NebulaOS-firmware@{sha[:7]} on {datetime.date.today().isoformat()}. "
         f"Do not edit by hand. -->", "",
         "# NebulaOS Moonraker API reference", "",
         "The OS-settings API that NebulaScreen - and any other Moonraker client - uses to",
         "read and change NebulaOS settings.", "",
         f"Source: `NebulaOS-firmware` at `{sha[:7]}`, "
         f"`{COMPONENT}`. **{len(endpoints)} endpoints**, "
         f"{len(notifications)} notification(s).", "",
         "## How this fits together", "",
         "```",
         "NebulaScreen panel  (or any Moonraker client)",
         "  -> Moonraker JSON-RPC   machine.nebulaos.*",
         "  -> nebulaos.py          a Moonraker component, in Moonraker's own process",
         "  -> /usr/libexec/nebulaos/nebulaos-osconfig",
         "                          argv in, one JSON object out, validated, atomic",
         "  -> nebulaos_osconfig/*.py   the helper modules that do the work",
         "```", "",
         "There is **no second daemon**. The component is composed into the Moonraker",
         "checkout by the `S05nebulaos-activate` boot service as an excluded symlink - the",
         "same mechanism NebulaOS uses for its Klipper extras - and is configured by a",
         "`[nebulaos]` section in `/etc/nebulaos/moonraker/nebulaos.conf`. **If that file is",
         "absent, Moonraker runs without the component**, and every endpoint below is simply",
         "missing. That is the difference between a printer that shows OS settings and one",
         "that does not.", "",
         "Moonraker exposes each HTTP path `/machine/nebulaos/x/y` as the JSON-RPC method",
         "`machine.nebulaos.x.y`, which is how NebulaScreen addresses them.", "",
         "## What this reference proves, and what it does not", "",
         "**Established from source:** that each endpoint is registered, its HTTP method, its",
         "JSON-RPC name, its handler, and which request parameters that handler reads with",
         "which defaults.", "",
         "**Also established, since 2026-11-03:** which `nebulaos-osconfig` call each endpoint",
         "makes, and the keys that helper's own `return` statements carry - see",
         "[Responses](#responses) for how far that goes and where it stops.", "",
         "**Not established here:** the *values*. A key is listed because a `return` in the",
         "helper puts it there, not because anyone saw what it contained on a printer.", "",
         "**No endpoint here is hardware-verified.** Nothing in this reference was observed on",
         "a printer.", "",
         "## Responses", "",
         "Every endpoint answers through the same envelope, and it is worth reading once",
         "rather than per endpoint.", "",
         "The helper writes a single JSON object to stdout: `{\"ok\": true, ...}` with its own",
         "result merged in, or `{\"ok\": false, \"error\": \"<CODE>\", \"message\": \"...\"}`.",
         "The Moonraker component pops `ok`. On success **the JSON-RPC result is the helper's",
         "object verbatim**, which is why listing the helper's return keys is the same thing",
         "as listing the response keys. On failure it raises a Moonraker error",
         "`\"<CODE>: <message>\"`, with the HTTP status taken from the helper's exit code:", "",
         "| Helper exit | What the client sees |",
         "|---|---|",
         "| refused | a refusal, carrying the code and message |",
         "| 1 or 64 | HTTP 400 |",
         "| anything else | HTTP 500 |",
         "| no JSON at all | HTTP 500, *nebulaos-osconfig returned no result* |",
         "| over the timeout | HTTP 504 |", "",
         "**Where the keys come from.** They are extracted with `ast` by walking the chain",
         "this reference already describes - endpoint handler to its `_read`/`_write` call, the",
         "CLI dispatcher to the helper function, that function's `return` statements to their",
         "keys. Nothing is transcribed by hand.", "",
         "**Where it stops, and why that is said out loud.** "
         f"{unresolved_n} of the {len(endpoints)} endpoints could",
         "not be resolved this way: some handlers build their answer in the component rather",
         "than delegating a single call, and some helpers return a value this extractor cannot",
         "read. Those say *Result keys not resolved from source* rather than carrying a",
         "plausible list. An invented response example is indistinguishable from a real one to",
         "the reader, which is exactly why guessing here would be worse than a gap.", "",
         "A key listed on a branch - added only when some condition holds - is still listed,",
         "because the response can carry it. The list is what the endpoint *may* return, not",
         "what it always returns.", "",
         "### Example values",
         "",
         "Three endpoints carry a table of values asserted by the repository's own tests,",
         "with the test named. That is the whole yield, and the number is the finding rather",
         "than a shortfall: `tests/nebulaos-osconfig-tests.py` is 4381 lines, but it mostly",
         "exercises the `nebulaos_osconfig` helper functions **directly** rather than through",
         "an endpoint, so it is not a source of per-endpoint examples at scale. A value is",
         "only attributed to an endpoint when the test calls exactly one, so it cannot land on",
         "the wrong one.",
         "",
         "The alternative - composing plausible example responses from the key names - was",
         "available and was not taken. It would have read better and been unfalsifiable.", "",
         "### Recorded from a printer", "",
         "Where static analysis cannot resolve an endpoint, a response **recorded from a**",
         "**real printer** is shown instead, with the capture's date, source file and the",
         "firmware it ran - and with the reason it is still current, which is always a",
         "checked statement about the helper's source rather than an assumption. Such a",
         "sample is weaker evidence than the code: it shows one answer this endpoint gave",
         "once, not every answer it can give. It is therefore never attached to an endpoint",
         "whose keys the source already settles.", "",
         "## Endpoints", "",
         "A parameter with no default is **required**; the request fails without it.", ""]

    for e in endpoints:
        L.append(f"### `{e['rpc']}`")
        L.append("")
        L.append(f"| | |")
        L.append(f"|---|---|")
        L.append(f"| HTTP | `{e['method']}` `{e['path']}` |")
        L.append(f"| JSON-RPC | `{e['rpc']}` |")
        L.append(f"| Handler | `{e['handler']}` |")
        L.append("")
        if e["params"]:
            L.append("| Parameter | Type | Default |")
            L.append("|---|---|---|")
            for n in sorted(e["params"]):
                p = e["params"][n]
                L.append(f"| `{n}` | {p['kind']} | "
                         f"{'**required**' if p['required'] else p['default']} |")
        else:
            L.append("*No request parameters.*")
        L.append("")
        r = responses.get(e["path"])
        if r and r.get("function"):
            L.append(f"Runs `nebulaos-osconfig "
                     f"{' '.join(h['domain'] + ' ' + h['verb'] for h in r['helper'])}`"
                     f" -> `{'`, `'.join(r['function'])}`.")
            L.append("")
        if r and r.get("result_keys"):
            L.append("Result keys: " +
                     ", ".join(f"`{k}`" for k in r["result_keys"]) + ".")
            L.append("")
        elif r is not None:
            L.append("*Result keys not resolved from source - see "
                     "[Responses](#responses).*")
            L.append("")
        if r and r.get("observed"):
            o = r["observed"]
            L.append(f"**Recorded from a printer** on {o['captured']} by "
                     f"{o['captured_by']} (`{o['source']}`, firmware "
                     f"`{o['firmware_at_capture']}`). One sample, not a schema: "
                     f"it shows what this printer sent once. It is current because "
                     f"{o['still_current_because']}.")
            L.append("")
            L.append("Keys in that response: " +
                     ", ".join(f"`{k}`" for k in sorted(o["result"])) + ".")
            L.append("")
            L.append("```json")
            L.append(json.dumps({"result": o["result"]}, indent=2, sort_keys=True))
            L.append("```")
            L.append("")
        if r and r.get("examples"):
            L.append("From the repository's own tests:")
            L.append("")
            L.append("| Key | Asserted value | Test |")
            L.append("|---|---|---|")
            for k in sorted(r["examples"]):
                ex = r["examples"][k]
                L.append(f"| {('the whole result' if not k else '`' + k + '`')} | "
                         f"`{json.dumps(ex['value'])}` | `{ex['test']}` |")
            L.append("")

    if notifications:
        L.append("## Notifications")
        L.append("")
        L.append("Published by the component over Moonraker's websocket.")
        L.append("")
        for n in notifications:
            L.append(f"- `{n}`")
        L.append("")
    open(out, "w").write("\n".join(L) + "\n")
    withp = sum(1 for e in endpoints if e["params"])
    print(f"{len(endpoints)} endpoints ({withp} with parameters), "
          f"{len(notifications)} notification(s) -> {out}")


if __name__ == "__main__":
    main()
