#!/usr/bin/env python3
"""Resolve what each NebulaOS Moonraker endpoint actually returns.

The API reference could already prove that an endpoint exists, its method, its
JSON-RPC name and its request parameters. It could not prove the *response*, and
said so rather than inventing one.

This closes that, mechanically, by walking the chain the reference already
describes:

    endpoint handler   nebulaos.py   -> self._read/_write("<domain>", "<verb>", ...)
    CLI dispatch       cli.py        -> <module>.<function>(...)
    helper module      <module>.py   -> the keys its return statements carry

Everything is read with `ast`. A key appears here only because a `return` in the
helper puts it there; a function whose returns this cannot resolve is reported as
unresolved rather than guessed at. That distinction is the whole value: a response
example invented from an endpoint's name would look exactly like a real one.

Usage:  gen_firmware_api_responses.py <firmware-checkout> <out.json>
"""
import ast, json, os, sys
import _srccommit

COMPONENT = "scripts/build/overlay/usr/lib/nebulaos/moonraker/nebulaos.py"
# Responses recorded from a real printer, for endpoints this extractor cannot
# resolve. Observation is weaker evidence than source - a sample shows what one
# printer sent once, not what the code can send - so it is attached only where
# the static answer is missing, and never allowed to overwrite one.
OBSERVED = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "api_observed_responses.json")
OSCONFIG = "scripts/build/overlay/usr/lib/nebulaos/python/nebulaos_osconfig"
TESTS = "tests/nebulaos-osconfig-tests.py"


def _str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def endpoints(path):
    """{handler name: (domain, verb)} and [(http path, method, handler)]."""
    tree = ast.parse(open(path).read())
    routes, calls = [], {}
    for node in ast.walk(tree):
        # the routes table: ("/machine/nebulaos/x", RequestType.GET, self._h)
        if isinstance(node, ast.Tuple) and len(node.elts) == 3:
            p = _str(node.elts[0])
            h = node.elts[2]
            if p and p.startswith("/machine/nebulaos") and isinstance(h, ast.Attribute):
                m = node.elts[1]
                method = m.attr if isinstance(m, ast.Attribute) else "?"
                routes.append((p, method, h.attr))
        # handler bodies: self._read("domain", "verb") / self._write(...)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found = []
            # Local `args = ["domain", "verb", ...]`, for handlers that build the
            # argv before calling - `_ota_check` appends --force and then calls
            # self._write(*args).
            local_lists = {}
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Assign) and isinstance(sub.value, ast.List)
                        and len(sub.targets) == 1 and isinstance(sub.targets[0], ast.Name)):
                    vals = [_str(e) for e in sub.value.elts]
                    if len(vals) >= 2 and vals[0] and vals[1]:
                        local_lists[sub.targets[0].id] = (vals[0], vals[1])
            for sub in ast.walk(node):
                if not (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute)):
                    continue
                attr = sub.func.attr
                if attr not in ("_read", "_write", "_exec"):
                    continue
                pair = None
                if sub.args:
                    first = sub.args[0]
                    # self._exec(["domain", "verb", ...]) - and the same shape
                    # inside _write when the argv was built as a list
                    if isinstance(first, ast.List) and len(first.elts) >= 2:
                        d, v = _str(first.elts[0]), _str(first.elts[1])
                        if d and v:
                            pair = (d, v)
                    elif isinstance(first, ast.BinOp) and isinstance(first.left, ast.List) \
                            and len(first.left.elts) >= 2:
                        d, v = _str(first.left.elts[0]), _str(first.left.elts[1])
                        if d and v:
                            pair = (d, v)
                    else:
                        d = _str(first)
                        v = _str(sub.args[1]) if len(sub.args) > 1 else None
                        if d and v:
                            pair = (d, v)
                for st in sub.args:
                    if isinstance(st, ast.Starred) and isinstance(st.value, ast.Name) \
                            and st.value.id in local_lists:
                        pair = local_lists[st.value.id]
                if pair:
                    found.append(pair)
            if found:
                calls[node.name] = found
    return routes, calls


def _target(node):
    """"module.function" for a call expression, or None."""
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            return f"{f.value.id}.{f.attr}"
    return None


def _targets(node):
    """Every module.function a return expression can evaluate to."""
    out = []
    if isinstance(node, ast.IfExp):
        out += _targets(node.body) + _targets(node.orelse)
        return out
    t = _target(node)
    if t:
        out.append(t)
    return out


def _constraint(test, name):
    """The literal values `name` is pinned to by `test`, or None."""
    if isinstance(test, ast.Compare) and len(test.ops) == 1:
        left, op, right = test.left, test.ops[0], test.comparators[0]
        if isinstance(left, ast.Name) and left.id == name:
            if isinstance(op, ast.Eq):
                v = _str(right)
                return [v] if v else None
            if isinstance(op, ast.In) and isinstance(right, (ast.Tuple, ast.List, ast.Set)):
                vs = [_str(e) for e in right.elts]
                return vs if all(vs) else None
    return None


def _pair(test):
    """(domain, verb) for `(domain, verb) == ("a", "b")`, or None."""
    if (isinstance(test, ast.Compare) and len(test.ops) == 1
            and isinstance(test.ops[0], ast.Eq)
            and isinstance(test.left, ast.Tuple) and len(test.left.elts) == 2
            and isinstance(test.comparators[0], ast.Tuple)):
        names = [e.id for e in test.left.elts if isinstance(e, ast.Name)]
        if names == ["domain", "verb"]:
            k = tuple(_str(e) for e in test.comparators[0].elts)
            if len(k) == 2 and None not in k:
                return k
    return None


def _str_dict(node):
    """{"key": module.function} as {key: "module.function"}, or None."""
    if not isinstance(node, ast.Dict):
        return None
    out = {}
    for k, v in zip(node.keys, node.values):
        ks = _str(k)
        if ks is None or not (isinstance(v, ast.Attribute) and isinstance(v.value, ast.Name)):
            return None
        out[ks] = f"{v.value.id}.{v.attr}"
    return out


def dispatch(path):
    """{(domain, verb): ["module.function", ...]} from cli.py's dispatcher.

    The dispatcher is a hand-written if-chain, so this walks it the way it
    executes: carrying whatever `domain` and `verb` have been pinned to on the
    branch currently being read. Four shapes appear and all four are handled -
    `(domain, verb) == (...)`, nested `domain ==` / `verb ==`, a local
    `{verb: function}` table, and a `{domain: function}[domain]()` lookup.
    """
    tree = ast.parse(open(path).read())
    out, tables = {}, {}

    # READ_ONLY = {("domain", "verb"), ...} at module level. The dispatcher's
    # read-only branch pins the domain but not the verb, so without this the
    # status endpoints resolve to nothing.
    readonly = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "READ_ONLY"
                and isinstance(node.value, (ast.Set, ast.Tuple, ast.List))):
            for e in node.value.elts:
                if isinstance(e, ast.Tuple) and len(e.elts) == 2:
                    d, v = _str(e.elts[0]), _str(e.elts[1])
                    if d and v:
                        readonly.setdefault(d, []).append(v)

    def record(dom, vrb, targets):
        if not dom or not vrb or not targets:
            return
        for d in dom:
            for v in vrb:
                out.setdefault((d, v), [])
                for t in targets:
                    if t not in out[(d, v)]:
                        out[(d, v)].append(t)

    def walk(body, dom, vrb):
        for node in body:
            if isinstance(node, ast.Assign):
                d = _str_dict(node.value)
                if d and isinstance(node.targets[0], ast.Name):
                    tables[node.targets[0].id] = d
                continue
            if isinstance(node, ast.If):
                nd, nv = dom, vrb
                pair = _pair(node.test)
                if pair:
                    nd, nv = [pair[0]], [pair[1]]
                else:
                    c = _constraint(node.test, "domain")
                    if c:
                        nd = c
                    c = _constraint(node.test, "verb")
                    if c:
                        nv = c
                    # `if verb in verbs:` - a local {verb: function} table
                    if (isinstance(node.test, ast.Compare)
                            and isinstance(node.test.ops[0], ast.In)
                            and isinstance(node.test.left, ast.Name)
                            and node.test.left.id == "verb"
                            and isinstance(node.test.comparators[0], ast.Name)
                            and node.test.comparators[0].id in tables):
                        tbl = tables[node.test.comparators[0].id]
                        for v, t in tbl.items():
                            record(dom, [v], [t])
                walk(node.body, nd, nv)
                walk(node.orelse, dom, vrb)
                continue
            if isinstance(node, (ast.With, ast.AsyncWith, ast.Try)):
                walk(node.body, dom, vrb)
                for h in getattr(node, "handlers", []):
                    walk(h.body, dom, vrb)
                walk(getattr(node, "orelse", []), dom, vrb)
                walk(getattr(node, "finalbody", []), dom, vrb)
                continue
            if isinstance(node, ast.Return) and node.value is not None:
                v = node.value
                # {domain: function}[domain]() - the read-only status lookup
                if (isinstance(v, ast.Call) and isinstance(v.func, ast.Subscript)
                        and isinstance(v.func.value, ast.Dict)):
                    tbl = _str_dict(v.func.value)
                    idx = v.func.slice
                    if tbl and isinstance(idx, ast.Name) and idx.id == "domain":
                        for d, t in tbl.items():
                            record([d], vrb or readonly.get(d), [t])
                        continue
                    # an inline {verb: function}[verb]() - cli.py uses this for
                    # the camera's defaults/reset/version trio
                    if tbl and isinstance(idx, ast.Name) and idx.id == "verb":
                        for vb, t in tbl.items():
                            record(dom, [vb], [t])
                        continue
                # table[verb]()
                if (isinstance(v, ast.Call) and isinstance(v.func, ast.Subscript)
                        and isinstance(v.func.value, ast.Name)
                        and v.func.value.id in tables):
                    for vb, t in tables[v.func.value.id].items():
                        record(dom, [vb], [t])
                    continue
                if isinstance(v, ast.IfExp):
                    c = _constraint(v.test, "verb")
                    if c and dom:
                        other = [x for x in (vrb or readonly.get(dom[0], []))
                                 if x not in c]
                        record(dom, c, _targets(v.body))
                        record(dom, other, _targets(v.orelse))
                        continue
                record(dom, vrb, _targets(v))

    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef) and fn.name == "_dispatch":
            walk(fn.body, None, None)
    return out


def _keys_of(node, fns, depth=0):
    """Top-level keys a return expression can carry, or None if unresolvable."""
    if depth > 3:
        return None
    if isinstance(node, ast.Dict):
        ks = set()
        for k in node.keys:
            if k is None:            # {**other}
                return None
            s = _str(k)
            if s is None:
                return None
            ks.add(s)
        return ks
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == "dict":
            ks = set()
            for a in node.args:
                sub = _keys_of(a, fns, depth + 1)
                if sub is None:
                    return None
                ks |= sub
            ks |= {kw.arg for kw in node.keywords if kw.arg}
            return ks
        if node.func.id in fns:      # a local helper's own returns
            return return_keys(fns[node.func.id], fns, depth + 1)
    if isinstance(node, ast.IfExp):
        a = _keys_of(node.body, fns, depth + 1)
        b = _keys_of(node.orelse, fns, depth + 1)
        return None if a is None or b is None else a | b
    return None


def _local_dict_keys(name, fn, fns, depth):
    """Keys of a local dict built up before being returned.

    The common shape in these helpers is `out = {...}` followed by conditional
    `out["k"] = ...` and `out.update({...})`. A key added on a branch is still a
    key the response can carry, so it counts; an assignment this cannot read
    makes the whole function unresolved rather than partly guessed.
    """
    keys, seen = set(), False
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    sub = _keys_of(node.value, fns, depth + 1)
                    if sub is None:
                        return None
                    keys |= sub
                    seen = True
                elif (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name)
                      and t.value.id == name):
                    k = _str(t.slice)
                    if k is None:
                        return None
                    keys.add(k)
                    seen = True
        elif (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
              and isinstance(node.value.func, ast.Attribute)
              and isinstance(node.value.func.value, ast.Name)
              and node.value.func.value.id == name
              and node.value.func.attr == "update" and node.value.args):
            sub = _keys_of(node.value.args[0], fns, depth + 1)
            if sub is None:
                return None
            keys |= sub
            seen = True
    return keys if seen else None


def return_keys(fn, fns, depth=0):
    """The union of keys across a function's returns, or None if any is unclear."""
    ks, saw = set(), False
    for node in ast.walk(fn):
        if isinstance(node, ast.Return) and node.value is not None:
            saw = True
            if isinstance(node.value, ast.Name):
                sub = _local_dict_keys(node.value.id, fn, fns, depth)
            else:
                sub = _keys_of(node.value, fns, depth)
            if sub is None:
                return None
            ks |= sub
    return ks if saw else None


def module_returns(mod_path):
    tree = ast.parse(open(mod_path).read())
    fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    return {name: return_keys(fn, fns) for name, fn in fns.items()}



def _res_chain(node):
    """["a", "b"] for res["a"]["b"], [] for a bare `res`, or None."""
    keys = []
    while isinstance(node, ast.Subscript):
        k = node.slice
        if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
            return None
        keys.append(k.value)
        node = node.value
    if isinstance(node, ast.Name) and node.id == "res":
        return list(reversed(keys))
    return None


def examples(path):
    """{http path: {key path: asserted value}} from the repository's own tests.

    Only an assertion made on the result of a `self.call("/machine/nebulaos/...")`
    in a test that calls exactly one endpoint counts, so a value can never be
    attributed to the wrong endpoint.

    The yield is small and that is the finding, not a failure of the extractor:
    measured on 2026-11-03 at 3 endpoints and 5 key/value pairs out of 59. These
    tests mostly exercise the osconfig helper functions directly rather than
    through an endpoint, so they are not a source of per-endpoint examples at
    scale. Inventing the rest from the key names would be the alternative, and it
    is not one.
    """
    if not os.path.exists(path):
        return {}
    tree = ast.parse(open(path).read())
    out = {}
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        called = {n.args[0].value for n in ast.walk(fn)
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                  and n.func.attr == "call" and n.args
                  and isinstance(n.args[0], ast.Constant)
                  and str(n.args[0].value).startswith("/machine/nebulaos")}
        if len(called) != 1:
            continue
        endpoint = called.pop()
        for n in ast.walk(fn):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr == "assertEqual" and len(n.args) == 2):
                continue
            chain = _res_chain(n.args[0])
            if chain is None:
                continue
            try:
                value = ast.literal_eval(n.args[1])
            except Exception:
                continue
            out.setdefault(endpoint, {})[".".join(chain)] = {
                "value": value, "test": fn.name}
    return out


def resolve(root, routes, calls, disp):
    """{http path: row} - the same rows main() writes, for the reference to use."""
    return {r["path"]: r for r in _rows(root, routes, calls, disp)[0]}


def observed():
    """{http path: entry} from data/api_observed_responses.json, or {}."""
    if not os.path.exists(OBSERVED):
        return {}
    return json.load(open(OBSERVED)).get("endpoints", {})


def _rows(root, routes, calls, disp):
    cache = {}
    exs = examples(os.path.join(root, TESTS))
    obs = observed()
    rows, resolved, unresolved = [], 0, 0
    for path, method, handler in sorted(routes):
        cv = calls.get(handler, [])
        row = {"path": path, "method": method, "handler": handler,
               "helper": [{"domain": d, "verb": v} for d, v in cv]}
        keys = set()
        ok = bool(cv)
        for d, v in cv:
            targets = disp.get((d, v)) or []
            if not targets:
                ok = False
                continue
            for target in targets:
                mod, fn = target.split(".", 1)
                if mod not in cache:
                    mp = os.path.join(root, OSCONFIG, mod + ".py")
                    cache[mod] = module_returns(mp) if os.path.exists(mp) else {}
                k = cache[mod].get(fn)
                row.setdefault("function", []).append(f"{mod}.{fn}")
                if k is None:
                    ok = False
                else:
                    keys |= k
        if ok and keys:
            row["result_keys"] = sorted(keys)
            resolved += 1
        else:
            row["result_keys"] = None
            unresolved += 1
        ex = exs.get(path)
        if ex:
            row["examples"] = ex
        o = obs.get(path)
        if o and not row["result_keys"]:
            row["observed"] = o
        rows.append(row)
    return rows, resolved, unresolved


def main():
    root, out_path = sys.argv[1], sys.argv[2]
    sha, sha_from = _srccommit.source_commit(root)
    routes, calls = endpoints(os.path.join(root, COMPONENT))
    disp = dispatch(os.path.join(root, OSCONFIG, "cli.py"))
    rows, resolved, unresolved = _rows(root, routes, calls, disp)
    meta = {"source_commit": sha, "resolved_from": sha_from,
            "endpoints": len(rows), "with_result_keys": resolved,
            "unresolved": unresolved, "routes": rows}
    json.dump(meta, open(out_path, "w"), indent=2, sort_keys=True)
    print(f"{len(rows)} endpoints: {resolved} with resolved result keys, "
          f"{unresolved} unresolved -> {out_path}")


if __name__ == "__main__":
    main()
