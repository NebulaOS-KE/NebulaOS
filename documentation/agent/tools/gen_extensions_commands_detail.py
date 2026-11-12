#!/usr/bin/env python3
"""Generate a per-command reference for the Klipper extensions.

One section per command, with everything the source actually establishes:
the handler, the help text, the parameters that handler reads (with types,
defaults and valid ranges), the errors it raises, and whether it runs G-code
or moves the machine.

Everything here is derived from the handler that the registration points at,
so a parameter cannot be attributed to the wrong command, and a default cannot
be transcribed wrongly.

Four things the mission asks for that are deliberately NOT generated, because
the source does not contain them and inventing them would be worse than
omitting them:

  * expected output - most handlers respond through gcmd.respond_info with
    runtime values, so the text depends on machine state
  * preconditions beyond the guards visible in the handler
  * safety warnings - a judgement about physical consequence, not a fact in
    the file
  * hardware behaviour of any kind

Each command section says which of those are unestablished rather than leaving
a reader to assume the silence means "nothing to worry about".

Usage:  gen_extensions_commands_detail.py <extensions-checkout> <out-file>
"""
import ast, json, os, subprocess, sys, datetime
import _srccommit

EFFECTS = {}
PARAM_GETTERS = {"get": "string", "get_int": "int", "get_float": "float",
                 "get_boolean": "bool"}
CONSTRAINTS = ("minval", "maxval", "above", "below")
RUNNERS = ("run_script", "run_script_from_command")

# Side-effect detection, by class.
#
# The first version of this reference printed a single line, "Runs G-code:
# yes / no - reports only", derived purely from whether the handler called
# run_script. That was actively misleading and was caught in review:
# NEBULAOS_BEEP drives the buzzer's PWM, SAVE_INPUT_SHAPER rewrites
# printer.cfg, EEPROM_WRITE_INT writes the EEPROM, Z_OFFSET_APPLY_PROBE
# persists an offset - and every one of them was labelled "reports only",
# which tells a reader the command is safe to try.
#
# "Runs no G-code" and "has no effect" are completely different claims.
WRITE_CALLS = ("write", "writelines", "replace", "rename", "unlink", "remove",
               "rmtree", "fsync", "dump", "truncate", "mkdir", "makedirs")
PERSIST_CALLS = ("set", "remove_section", "save_config")
MOVE_CALLS = ("set_gcode_offset", "set_position", "manual_move", "move",
              "set_digital", "set_pwm", "setup_pin", "set_temp",
              "set_speed", "home")


CLASS_TEXT = {
    "gcode": "**Runs G-code** - can move the machine or change temperatures",
    "hardware": "**Writes hardware directly** (sysfs, PWM, I2C or EEPROM)",
    "files": "**Writes or deletes files** on the printer",
    "config": "**Changes the saved Klipper configuration**",
    "persistent": "**Changes state that survives a restart**",
    "readonly": "Reports only - no effect found when the handler and the objects "
                "it calls were read",
}


def load_effects():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "data", "extension_command_effects.json")
    if not os.path.exists(path):
        return {}
    # Filter the exact metadata key only. Filtering anything starting with
    # "_" would silently drop every internal command - 15 of them here all
    # begin with an underscore by convention.
    return {k: v for k, v in json.load(open(path)).items() if k != "_comment"}


def is_lit(n):
    try:
        ast.literal_eval(n)
        return True
    except Exception:
        return False


def fmt(v):
    if v is None:
        return "`none`"
    if isinstance(v, str):
        return f"`{v}`" if v else "`\"\"`"
    if isinstance(v, bool):
        return "`true`" if v else "`false`"
    return f"`{v}`"


def consts_of(tree):
    out = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                and isinstance(n.targets[0], ast.Name) and is_lit(n.value):
            out[n.targets[0].id] = ast.literal_eval(n.value)
    return out


def resolve(node, consts):
    if is_lit(node):
        v = ast.literal_eval(node)
        return v if isinstance(v, str) else None
    if isinstance(node, ast.Name):
        return consts.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = resolve(node.left, consts), resolve(node.right, consts)
        if isinstance(a, str) and isinstance(b, str):
            return a + b
    return None


def class_help(tree):
    """cmd_<NAME>_help = "..." assignments, including implicit concatenation."""
    out = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and len(n.targets) == 1:
            t = n.targets[0]
            name = getattr(t, "id", None) or getattr(t, "attr", None)
            if name and name.startswith("cmd_") and name.endswith("_help") \
                    and is_lit(n.value):
                v = ast.literal_eval(n.value)
                if isinstance(v, str):
                    out[name[4:-5]] = " ".join(v.split())
    return out


def analyse(fn, consts, funcs=None, _depth=0, _seen=None):
    """Parameters, errors and side effects of a command handler.

    Follows `self._helper(...)` calls into methods of the same module, to a
    bounded depth. Without that almost every effect is invisible, because
    handlers delegate: NEBULAOS_BEEP's PWM write lives in `_schedule`, and a
    scan of the handler body alone reports "none detected" for it.

    Parameters are collected at depth 0 only - a helper's own arguments are not
    command parameters.
    """
    funcs = funcs or {}
    _seen = _seen if _seen is not None else set()
    params, errors, runs, responds = {}, [], [], False
    effects = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            a = node.func.attr
            recv = getattr(node.func.value, "id", None) or \
                getattr(node.func.value, "attr", None)
            if a in PARAM_GETTERS and recv == "gcmd" and node.args and is_lit(node.args[0]):
                nm = ast.literal_eval(node.args[0])
                if not isinstance(nm, str):
                    continue
                def render(v):
                    """A default or constraint value, as informatively as the
                    source allows. "computed" is a last resort: a module
                    constant has a literal value worth printing, and a
                    `self.x` default is almost always a config option, which
                    is far more useful to a reader than the word computed."""
                    if is_lit(v):
                        return fmt(ast.literal_eval(v))
                    if isinstance(v, ast.Name) and v.id in consts:
                        return f"{fmt(consts[v.id])} (`{v.id}`)"
                    if isinstance(v, ast.Attribute) and \
                            getattr(v.value, "id", None) == "self":
                        return f"the `{v.attr}` config option"
                    return "computed"

                if len(node.args) > 1:
                    d, req = render(node.args[1]), False
                else:
                    kw = {k.arg: k.value for k in node.keywords}
                    if "default" in kw:
                        d, req = render(kw["default"]), False
                    else:
                        d, req = "-", True
                def plain(v):
                    """A constraint value without markup: the table column reads
                    as prose ("minval 0, maxval 20000"), so backticks from the
                    default renderer would leak into it."""
                    if is_lit(v):
                        return str(ast.literal_eval(v))
                    if isinstance(v, ast.Name) and v.id in consts:
                        return f"{consts[v.id]} ({v.id})"
                    if isinstance(v, ast.Attribute):
                        return v.attr
                    return "computed"

                cons = [f"{k.arg} {plain(k.value)}"
                        for k in node.keywords if k.arg in CONSTRAINTS]
                prev = params.get(nm)
                if prev and not prev["required"]:
                    continue
                params[nm] = dict(kind=PARAM_GETTERS[a], default=d, required=req,
                                  constraints=", ".join(cons) or "-")
            if a == "error":
                if node.args and is_lit(node.args[0]):
                    errors.append(" ".join(str(ast.literal_eval(node.args[0])).split()))
                else:
                    errors.append("(message built at runtime)")
            if a in WRITE_CALLS:
                effects.add("writes files or deletes them")
            if a in MOVE_CALLS:
                effects.add("changes machine or printer state directly")
            if a in PERSIST_CALLS and isinstance(node.func.value, ast.Attribute) \
                    and node.func.value.attr in ("configfile", "config"):
                effects.add("writes the saved configuration")
            if a in RUNNERS:
                if node.args and is_lit(node.args[0]):
                    runs.append(" ".join(str(ast.literal_eval(node.args[0])).split())[:120])
                else:
                    runs.append("(script built at runtime)")
            if a in ("respond_info", "respond_raw"):
                responds = True
        # open(path, "w"/"a"/"x") - a file write the call-name scan misses.
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "open" and len(node.args) > 1 \
                and is_lit(node.args[1]):
            mode = str(ast.literal_eval(node.args[1]))
            if any(m in mode for m in ("w", "a", "x", "+")):
                effects.add("writes files or deletes them")
        if isinstance(node, ast.Raise):
            exc = node.exc
            if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Attribute):
                if exc.args and is_lit(exc.args[0]):
                    errors.append(" ".join(str(ast.literal_eval(exc.args[0])).split()))
    if _depth < 3:
        for node in ast.walk(fn):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            if getattr(node.func.value, "id", None) != "self":
                continue
            target = node.func.attr
            if target in _seen or target not in funcs:
                continue
            _seen.add(target)
            _p, _e, _r, _resp, _eff = analyse(funcs[target], consts, funcs,
                                              _depth + 1, _seen)
            errors.extend(_e)
            runs.extend(_r)
            effects.update(_eff)
    if runs:
        effects.add("runs G-code, so it can move the machine or change temperatures")
    return params, errors, runs, responds, sorted(effects)


def main():
    global EFFECTS
    root, out = sys.argv[1], sys.argv[2]
    EFFECTS = load_effects()
    # The code commit, not this worktree's docs branch - see _srccommit.py.
    sha, sha_from = _srccommit.source_commit(root)
    ext = os.path.join(root, "extras")
    tests = {f for f in os.listdir(ext) if f.startswith("test_")}
    found = []
    for f in sorted(os.listdir(ext)):
        if not f.endswith(".py") or f.startswith("test_"):
            continue
        tree = ast.parse(open(os.path.join(ext, f)).read())
        consts = consts_of(tree)
        helps = class_help(tree)
        funcs = {n.name: n for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            if node.func.attr not in ("register_command", "register_mux_command"):
                continue
            if not node.args:
                continue
            name = resolve(node.args[0], consts)
            if not name or not name.replace("_", "").isalnum():
                continue
            handler = None
            for a in node.args[1:]:
                if isinstance(a, ast.Attribute):
                    handler = a.attr
                    break
            dereg = len(node.args) > 1 and isinstance(node.args[1], ast.Constant) \
                and node.args[1].value is None
            desc = None
            for kw in node.keywords:
                if kw.arg == "desc":
                    if is_lit(kw.value):
                        desc = " ".join(str(ast.literal_eval(kw.value)).split())
                    elif isinstance(kw.value, ast.Attribute):
                        desc = helps.get(kw.value.attr[4:-5] if
                                         kw.value.attr.startswith("cmd_") else "")
            if desc is None:
                desc = helps.get(name) or helps.get(name.lstrip("_"))
            p, e, r, resp, eff = ({}, [], [], False, [])
            if handler and handler in funcs:
                p, e, r, resp, eff = analyse(funcs[handler], consts, funcs)
            found.append(dict(name=name, module=f, handler=handler, desc=desc,
                              params=p, errors=e, runs=r, responds=resp, effects=eff,
                              dereg=dereg, mux=node.func.attr.endswith("mux_command"),
                              tested=f"test_{f[:-3]}.py" in tests))
    seen, cmds = set(), []
    for c in sorted(found, key=lambda c: (c["name"], c["module"])):
        key = (c["name"], c["module"])
        if key in seen and not c["handler"]:
            continue
        seen.add(key)
        cmds.append(c)

    L = [f"<!-- Generated by documentation/agent/tools/"
         f"gen_extensions_commands_detail.py from NebulaOS-klipper-extensions@"
         f"{sha[:7]} on {datetime.date.today().isoformat()}. "
         f"Do not edit by hand. -->", "",
         "# G-code commands, in detail", "",
         "One section per command. Everything below is derived from the handler the",
         "registration points at, so a parameter cannot be attributed to the wrong command",
         "and a default cannot be transcribed wrongly.", "",
         f"Source: `NebulaOS-klipper-extensions` at `{sha[:7]}`. {len(cmds)} commands.", "",
         "For the one-line summary table, see [Commands](Commands). For configuration,",
         "[Configuration](Configuration).", "",
         "## What is established here, and what is not", "",
         "**Established from source:** that the command is registered; its handler; its help",
         "text; the parameters that handler reads, with types, defaults and valid ranges; the",
         "error messages it raises as literals; and whether it runs G-code or only reports.", "",
         "**Not established, and not guessed:**", "",
         "- **Expected output.** Most handlers reply through `respond_info` with runtime",
         "  values, so the text depends on machine state. Writing an example response would",
         "  mean inventing it.",
         "- **Preconditions** beyond the guards visible in the handler. A command may also",
         "  depend on calibration state or configuration that the handler does not check.",
         "- **Safety warnings.** Whether a command is dangerous is a judgement about physical",
         "  consequence, not a fact in the file.",
         "- **Hardware behaviour.** Nothing here was run on a printer.", "",
         "## How to read the side effects", "",
         "Each command's effects were established by **reading** its handler and the objects",
         "that handler calls. They are not detected automatically, and the reason is worth",
         "stating, because the first version of this page did detect them and was wrong.",
         "",
         "That version printed *Runs G-code: yes / no - reports only*, derived from whether",
         "the handler called `run_script`. It labelled `NEBULAOS_BEEP` *reports only* - a",
         "command that drives the buzzer's PWM. Also `SAVE_INPUT_SHAPER`, which rewrites",
         "`printer.cfg`; `EEPROM_WRITE_INT`, which writes the EEPROM; and",
         "`Z_OFFSET_APPLY_PROBE`, which persists an offset. All four told the reader the",
         "command was safe to try. This was caught in review, not by the tool.",
         "",
         "Following the calls automatically does not fix it either. Effects are reached",
         "through collaborator objects held on the module - `self.pwm.off()`,",
         "`self.gcode.run_script()`, `self.journal.write()` - and resolving those object",
         "graphs soundly is real static analysis. A scan that walks only the handler, or only",
         "`self._method` calls, still reports nothing for the buzzer.",
         "",
         "So the automatic claim was removed. A command with no entry reads **not",
         "determined**, which is honest, and a reader is told not to treat it as harmless.",
         "**Running no G-code and having no effect are completely different claims.**", "",
         "A leading underscore means internal: a step of another command, or a macro's",
         "implementation detail. Not meant to be typed.", ""]

    for c in cmds:
        L.append(f"## `{c['name']}`")
        L.append("")
        if c["desc"]:
            L.append(c["desc"])
            L.append("")
        rows = [f"| Module | `extras/{c['module']}` |",
                f"| Handler | `{c['handler']}` |" if c["handler"] else "| Handler | - |",
                f"| Registration | {'mux command' if c['mux'] else 'command'} |"]
        if c["dereg"]:
            rows.append("| Upstream | **replaces an upstream Klipper command of this name** |")
        rows.append(f"| Test | {'`extras/test_'+c['module'][:-3]+'.py`' if c['tested'] else 'none'} |")
        cls = EFFECTS.get(c["name"])
        if cls:
            label = "reports only" if cls == ["readonly"] else ", ".join(cls)
        else:
            label = "**not determined**"
        rows.append(f"| Side effects | {label} |")
        L.append("| | |")
        L.append("|---|---|")
        L += rows
        L.append("")
        if c["params"]:
            L.append("**Parameters**")
            L.append("")
            L.append("| Parameter | Type | Default | Valid range |")
            L.append("|---|---|---|---|")
            for n in sorted(c["params"]):
                p = c["params"][n]
                L.append(f"| `{n}` | {p['kind']} | "
                         f"{'**required**' if p['required'] else p['default']} | "
                         f"{p['constraints']} |")
            L.append("")
            ex = [c["name"]]
            for n in sorted(c["params"]):
                p = c["params"][n]
                if p["required"]:
                    ex.append(f"{n}=<{p['kind']}>")
            L.append("**Example invocation**")
            L.append("")
            L.append("```")
            L.append(" ".join(ex))
            L.append("```")
            L.append("")
            L.append("*Constructed from the required parameters above. Optional parameters are")
            L.append("omitted; their defaults are in the table.*")
            L.append("")
        else:
            L.append("**Parameters:** none.")
            L.append("")
        if c["errors"]:
            L.append("**Errors raised**")
            L.append("")
            for e in sorted(set(c["errors"])):
                L.append(f"- {e}")
            L.append("")
        if cls:
            L.append("**Side effects**")
            L.append("")
            for k in cls:
                L.append(f"- {CLASS_TEXT.get(k, k)}")
            L.append("")
        else:
            L.append("**Side effects: not determined.** This command's handler has not been")
            L.append("read for effects yet. Do not read this as harmless.")
            L.append("")
        if c["runs"]:
            L.append("G-code this handler runs, where the source states it literally:")
            L.append("")
            for r in sorted(set(c["runs"]))[:6]:
                L.append(f"- `{r}`")
            L.append("")
        L.append("")
    open(out, "w").write("\n".join(L) + "\n")
    wp = sum(1 for c in cmds if c["params"])
    we = sum(1 for c in cmds if c["errors"])
    print(f"{len(cmds)} commands ({wp} with parameters, {we} with literal errors) -> {out}")


if __name__ == "__main__":
    main()
