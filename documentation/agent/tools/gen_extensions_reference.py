#!/usr/bin/env python3
"""Generate the Klipper extensions command and configuration reference.

Parsed with `ast`, not regex. Two regex extraction bugs earlier in this project
silently mis-sized the inventory - one dropped an API path because it contained
a digit, one collected 85 things that were not settings at all. A real parser
cannot make either mistake: it sees the call, its arguments and their literal
values, or it sees nothing and says so.

What this proves: that a command is registered, that a config option is read,
and what literal default and constraints the source gives it. What it cannot
prove: that any of it behaves correctly on a printer. Items whose default is
computed rather than literal are reported as "computed", never guessed.

Usage:  gen_extensions_reference.py <extensions-checkout> <out-dir>
"""
import ast, json, os, re, subprocess, sys, datetime
import _srccommit

GETTERS = {
    "get": "string", "getint": "int", "getfloat": "float",
    "getboolean": "bool", "getlists": "list", "getlist": "list",
    "getchoice": "choice", "get_name": "name", "getfloatlist": "float list",
    "getintlist": "int list",
    # Deliberately NOT here: getsection and get_prefix_sections look up other
    # config sections rather than reading an option, so counting them would
    # report section lookups as settings.
}
CONSTRAINTS = ("minval", "maxval", "above", "below")


def literal(node):
    """A literal value, or None if it is not one."""
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def is_literal(node):
    try:
        ast.literal_eval(node)
        return True
    except Exception:
        return False


def fmt(v):
    if v is None:
        return "-"
    if isinstance(v, str):
        return f"`{v}`" if v else "`\"\"`"
    if isinstance(v, bool):
        return "`true`" if v else "`false`"
    return f"`{v}`"


HEADING = re.compile(r"^[A-Z][A-Za-z0-9 /()-]{2,40}$")


def option_comment(lines, lineno):
    """The comment block immediately above a config line, if it is about that
    option rather than a heading for the group below it.

    A comment like "Coolstep Tunables" heads several options; attaching it to
    whichever one happens to come first would quietly mislabel that option. So
    short title-like lines with no verb and no full stop are rejected.
    """
    i = lineno - 2
    block = []
    while i >= 0 and lines[i].strip().startswith("#"):
        block.insert(0, lines[i].strip().lstrip("#").strip())
        i -= 1
    text = " ".join(x for x in block if x)
    text = " ".join(text.split())
    if not text or HEADING.match(text):
        return ""
    if len(text) > 300:
        text = text[:297].rsplit(" ", 1)[0] + "..."
    return text


def load_purposes():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "data", "extension_option_purposes.json")
    if not os.path.exists(path):
        return {}
    return {k: v for k, v in json.load(open(path)).items()
            if not k.startswith("_")}


def module_purpose(path):
    """The module's own header comment, as its purpose.

    The authors' words, not an inference from the module name. Config options
    themselves carry no inline comments in this repository, so a per-option
    purpose cannot be extracted - and guessing one from an option's name is
    exactly the kind of plausible invention this project refuses. The module
    header is the honest unit of explanation: it says what the thing is for,
    and the option table says what you can set.
    """
    out = []
    for ln in open(path, errors="replace").read().split("\n"):
        s = ln.strip()
        if not s.startswith("#"):
            break
        body = s.lstrip("#").strip()
        if not body:
            if out:
                break
            continue
        if body.startswith(("!", "SPDX", "Copyright")):
            continue
        out.append(body)
        if len(out) >= 6:
            break
    text = " ".join(out)
    base = os.path.basename(path)
    stem = base[:-3] if base.endswith(".py") else base
    # Headers open with either "name.py - ..." or "name - ...".
    text = re.sub(r"^(" + re.escape(base) + "|" + re.escape(stem) + r")\s*[-:]\s*",
                  "", text)
    text = " ".join(text.split())
    if text:
        text = text[0].upper() + text[1:]
    m = re.search(r"^(.{60,400}?[.!])(\s|$)", text)
    if m:
        text = m.group(1)
    elif len(text) > 400:
        text = text[:397].rsplit(" ", 1)[0] + "..."
    return text


def module_consts(tree):
    """Top-level NAME = <literal> assignments, for names built from constants."""
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) and is_literal(node.value):
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


def resolve_name(node, consts):
    """The command name a register_command call uses, if it can be established."""
    if is_literal(node):
        v = ast.literal_eval(node)
        return v if isinstance(v, str) else None
    if isinstance(node, ast.Name):
        return consts.get(node.id)
    # '_' + CMD  /  CMD + '_SUFFIX'
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = resolve_name(node.left, consts)
        right = resolve_name(node.right, consts)
        if isinstance(left, str) and isinstance(right, str):
            return left + right
    return None


def receiver_name(node):
    """The name the getter is called on: config, gcmd, some dict, ..."""
    r = node.func.value
    if isinstance(r, ast.Name):
        return r.id
    if isinstance(r, ast.Attribute):
        return r.attr
    return None


def scan(path, consts):
    """(config options, gcode parameters, commands) found in one module.

    The receiver matters enormously. A naive walk over every `.getX(...)` call
    finds 299 "config options" in this repository, of which only 159 are on a
    config object at all - the rest are dictionary and JSON lookups (`data`,
    `manifest`, `raw`, `sidecar_state`) and G-code parameter reads on `gcmd`.
    Publishing that would have invented roughly 140 configuration options.

    So: `config` receivers are configuration, `gcmd` receivers are command
    parameters, and everything else is ignored.
    """
    src_text = open(path).read()
    src_lines = src_text.split("\n")
    tree = ast.parse(src_text)
    consts = module_consts(tree)
    options, params, commands = [], [], []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        attr = node.func.attr

        if attr in GETTERS and node.args:
            recv = receiver_name(node)
            if recv not in ("config", "gcmd"):
                continue          # a dict or JSON lookup, not an interface
            name = literal(node.args[0])
            if not isinstance(name, str):
                continue
            kind = GETTERS[attr]
            # The default arrives three ways, and missing one makes an optional
            # setting look required - a worse lie than a wrong default, because
            # it tells the reader to go and set something they do not need to.
            # autotune_tmc passes 15 options as `default=CONSTANT`, every one of
            # which this reported as **required** until the keyword form was
            # handled.
            dflt_node = None
            if len(node.args) > 1:
                dflt_node = node.args[1]
            else:
                for kw in node.keywords:
                    if kw.arg == "default":
                        dflt_node = kw.value
                        break
            if dflt_node is None:
                default, required = "-", True
            else:
                required = False
                def dflt(v):
                    # "-" is what the constraints column uses for "none", so a
                    # None default rendered that way reads as missing data
                    # rather than as the actual value.
                    return "`none`" if v is None else fmt(v)
                if is_literal(dflt_node):
                    default = dflt(ast.literal_eval(dflt_node))
                elif isinstance(dflt_node, ast.Name) and dflt_node.id in consts:
                    default = f"{dflt(consts[dflt_node.id])} (`{dflt_node.id}`)"
                elif isinstance(dflt_node, ast.Attribute):
                    default = f"`{dflt_node.attr}`"
                else:
                    default = "computed"
            cons = []
            for kw in node.keywords:
                if kw.arg in CONSTRAINTS and is_literal(kw.value):
                    cons.append(f"{kw.arg} {ast.literal_eval(kw.value)}")
            rec_ = dict(name=name, kind=kind, default=default,
                        required=required, constraints=", ".join(cons) or "-",
                        comment=option_comment(src_lines, node.lineno))
            (params if recv == "gcmd" else options).append(rec_)

        elif attr in ("register_command", "register_mux_command") and node.args:
            cname = resolve_name(node.args[0], consts)
            if not cname or not cname.replace("_", "").isalnum():
                continue
            desc = "-"
            for kw in node.keywords:
                if kw.arg == "desc" and is_literal(kw.value):
                    desc = " ".join(str(ast.literal_eval(kw.value)).split())
            handler = None
            if len(node.args) > 1 and isinstance(node.args[1], ast.Attribute):
                handler = node.args[1].attr
            elif len(node.args) > 3 and isinstance(node.args[3], ast.Attribute):
                handler = node.args[3].attr
            # register_command(name, None) de-registers an upstream command
            dereg = len(node.args) > 1 and isinstance(node.args[1], ast.Constant) \
                and node.args[1].value is None
            commands.append(dict(name=cname, desc=desc, handler=handler,
                                 mux=attr == "register_mux_command",
                                 dereg=dereg))
    return options, params, commands


def main():
    root, out = sys.argv[1], sys.argv[2]
    # The code commit, not this worktree's docs branch - see _srccommit.py.
    sha, sha_from = _srccommit.source_commit(root)
    ext = os.path.join(root, "extras")
    mods = sorted(f for f in os.listdir(ext)
                  if f.endswith(".py") and not f.startswith("test_"))
    tests = {f for f in os.listdir(ext) if f.startswith("test_")}
    data = {}
    for f in mods:
        try:
            data[f] = scan(os.path.join(ext, f), {})
        except SyntaxError as e:
            print(f"  SKIP {f}: {e}")
    os.makedirs(out, exist_ok=True)
    today = datetime.date.today().isoformat()
    head = (f"<!-- Generated by documentation/agent/tools/"
            f"gen_extensions_reference.py from NebulaOS-klipper-extensions@"
            f"{sha[:7]} on {today}. Do not edit by hand. -->\n\n")

    # ---- commands -------------------------------------------------------
    cmds = []
    for f, (_o, _p, cs) in data.items():
        for c in cs:
            c["module"] = f
            cmds.append(c)
    by_name = {}
    for c in cmds:
        by_name.setdefault(c["name"], []).append(c)

    L = [head, "# G-code command reference\n",
         "Every command these extensions register, extracted from the source with a Python",
         "parser rather than a text search, so a command cannot be missed because of how its",
         "name is spelled or assembled.\n",
         f"Source: `NebulaOS-klipper-extensions` at `{sha[:7]}`. "
         f"{len(by_name)} commands across {len(mods)} modules.\n",
         "**What this establishes:** that the command is registered, by which module, with",
         "which handler and description. **What it does not establish:** that it behaves",
         "correctly on a printer. Where a test covers the module, it is named - that is",
         "evidence the logic is exercised, not that the hardware responds.\n",
         "A leading underscore marks a command as internal: it is a step of another command",
         "or a macro's implementation detail, and is not meant to be called directly.\n",
         "**Some public commands are not in this table.** Several user-facing names are",
         "`gcode_macro` definitions shipped in the firmware's own configuration, which call the",
         "underscore-prefixed command registered here. `NEBULAOS_BED_TRAM` is one: this",
         "repository registers `_NEBULAOS_BED_TRAM`, and the public name is a macro in the",
         "firmware's `calibration.cfg`. A reference built only from this repository cannot see",
         "those, and claiming it is the complete list of what a user can type would be wrong.\n",
         "## Commands\n",
         "| Command | Module | Kind | Test | Description |",
         "|---|---|---|---|---|"]
    for name in sorted(by_name):
        for c in by_name[name]:
            t = f"test_{c['module'][:-3]}.py"
            tcell = f"`{t}`" if t in tests else "-"
            kind = "mux" if c["mux"] else ("**replaces upstream**" if c["dereg"] else "command")
            L.append(f"| `{name}` | `{c['module']}` | {kind} | {tcell} | {c['desc']} |")
    L.append("")
    L.append("## Commands that replace upstream Klipper behaviour\n")
    L.append("These are registered with a `None` handler first, which de-registers the")
    L.append("upstream command, and then re-registered by this module. **They are modified")
    L.append("upstream behaviour, not NebulaOS inventions** - someone arriving from stock")
    L.append("Klipper will expect the upstream semantics.\n")
    dereg = sorted({c["name"] for c in cmds if c["dereg"]})
    if dereg:
        for n in dereg:
            mods_for = sorted({c["module"] for c in cmds if c["name"] == n})
            L.append(f"- `{n}` - {', '.join('`'+m+'`' for m in mods_for)}")
    else:
        L.append("*(none found)*")
    L.append("")
    L.append("## Command parameters, by module\n")
    L.append("Parameters each module reads from the G-code command line, with the literal")
    L.append("default where the source gives one. A parameter with no default is **required**")
    L.append("on the command. These are listed per module rather than per command, because a")
    L.append("module's handlers share its parameter parsing - matching each parameter to one")
    L.append("command would need tracing every handler, and guessing it would be worse than")
    L.append("saying so.\n")
    any_params = False
    for f in sorted(data):
        _o, ps, _c = data[f]
        if not ps:
            continue
        any_params = True
        seen = {}
        for o in ps:
            seen.setdefault(o["name"], o)
        L.append(f"### `{f}`\n")
        L.append("| Parameter | Type | Default | Constraints |")
        L.append("|---|---|---|---|")
        for n in sorted(seen):
            o = seen[n]
            d = "**required**" if o["required"] else o["default"]
            L.append(f"| `{n}` | {o['kind']} | {d} | {o['constraints']} |")
        L.append("")
    if not any_params:
        L.append("*(none found)*\n")
    open(os.path.join(out, "COMMANDS.md"), "w").write("\n".join(L) + "\n")

    # ---- configuration --------------------------------------------------
    L = [head, "# Configuration reference\n",
         "Every configuration option these extensions read, with the literal default and",
         "constraints the source gives it. Extracted with a Python parser, so no default is",
         "transcribed by hand.\n",
         f"Source: `NebulaOS-klipper-extensions` at `{sha[:7]}`.\n",
         "**Defaults are never invented.** An option whose default is computed at runtime",
         "rather than written as a literal is shown as `computed` - the source is the only",
         "honest answer there. An option with no default is **required**: Klipper raises an",
         "error if the section omits it.\n",
         "Section names are the module names, which is how Klipper's `[section]` headers map",
         "to these files.\n",
         "## Every one of these needs a Klipper restart\n",
         "**Checked, not assumed.** Every configuration read in this repository happens in a",
         "module's `__init__` or `load_config`, at load time - a scan of all call sites found",
         "no option re-read at runtime. So changing any option below takes effect only after",
         "Klipper restarts, and nothing here can be adjusted live.",
         "",
         "On the printer that is **Settings -> Printer -> Restart Klipper**, or",
         "`FIRMWARE_RESTART` from the console. The live adjustments a user can make during a",
         "print - speed, flow, Z offset, pressure advance - are not configuration options and",
         "are not in this file.\n",
         "## Where the explanations come from\n",
         "The text below each heading is the module's own header comment, written by its",
         "author. The **Purpose** column is hand-written, by reading the module that uses",
         "the option - not extracted, because this repository carries no inline comments",
         "above its options, and not inferred from the option's name, which would be",
         "invention dressed as documentation.",
         "",
         "Where an option is passed straight to a stepper driver register field, the purpose",
         "says so and names the field rather than explaining what the field does. That is",
         "the boundary of what can be established from this source: the driver's own",
         "datasheet is the authority on the field, and paraphrasing it from memory here",
         "would be the same invention in a more convincing costume.\n",
         "## Some options are accepted and then ignored\n",
         "A handful of options are read by a module and deliberately **not acted on**. Their",
         "Purpose cell begins *Accepted but not acted on*, and a reader who sets one should",
         "expect nothing to happen.",
         "",
         "Two different reasons, both from the source:",
         "",
         "- **To stop Klipper refusing to start.** Klipper hard-errors on any option in a",
         "  section that the module never reads. `[z_compensate]` on a real device sets",
         "  `tri_min_hold`, `tri_max_hold` and `speed`, which belonged to a sensitivity",
         "  override removed with PRTouch in Phase 1.8B. They are read and discarded so the",
         "  printer still boots.",
         "- **Because the meaning is unconfirmed.** `type_nozz`, `noz_pos_center`,",
         "  `noz_pos_offset` and `pumpback_mm` are read but unused, and the source explains",
         "  why: `noz_pos_center` is plausibly an XY reference point with nothing confirming",
         "  it, and misapplying it would send the toolhead somewhere unintended;",
         "  `pumpback_mm` is plausibly a pre-wipe retract, and wiring untested E-axis motion",
         "  into a probe and heat sequence was judged not worth the risk on a guess.",
         "",
         "That second group is the author choosing to leave a thing visibly unfinished rather",
         "than act on a plausible guess. Documenting them as ordinary settings would undo",
         "that: it would tell a reader these controls work.\n",
         "Where an option has its own **Purpose**, it was written by reading the module.",
         "Where the cell says *From the source comment*, it is the comment the author left",
         "above that line, quoted. A dash means neither exists - and a dash is the honest",
         "answer, because the alternative is a sentence invented from the option's name.\n"]
    purposes = load_purposes()
    # An orphan key is a purpose that was written and will never be shown.
    # Both of the first two here used the Python attribute name instead of the
    # config key (max_tune_printing_seconds for max_tune_seconds_printing), and
    # the file contributed nothing without saying so. Fail loudly instead.
    real = set()
    for f, (opts, _p, _c) in data.items():
        for o in opts:
            real.add(f"{f[:-3]}:{o['name']}")
    orphans = sorted(set(purposes) - real)
    if orphans:
        print("WARNING: purposes written for options that do not exist:")
        for o in orphans:
            print(f"  {o}")
    total = 0
    documented_purpose = 0
    for f in sorted(data):
        opts, _p, _c = data[f]
        if not opts:
            continue
        seen = {}
        for o in opts:
            seen.setdefault(o["name"], o)
        total += len(seen)
        documented_purpose += sum(
            1 for n in seen
            if purposes.get(f"{f[:-3]}:{n}") or seen[n].get("comment"))
        L.append(f"## `[{f[:-3]}]`\n")
        purpose = module_purpose(os.path.join(ext, f))
        if purpose:
            L.append(f"{purpose}\n")
        t = f"test_{f[:-3]}.py"
        if t in tests:
            L.append(f"Tested by `extras/{t}`.\n")
        L.append("| Option | Purpose | Type | Default | Constraints |")
        L.append("|---|---|---|---|---|")
        for n in sorted(seen):
            o = seen[n]
            d = "**required**" if o["required"] else o["default"]
            why = purposes.get(f"{f[:-3]}:{n}", "")
            if not why and o.get("comment"):
                why = f"*From the source comment:* {o['comment']}"
            L.append(f"| `{n}` | {why or '-'} | {o['kind']} | {d} | "
                     f"{o['constraints']} |")
        L.append("")
    L.insert(5, f"{total} options across {sum(1 for f in data if data[f][0])} modules.\n")
    open(os.path.join(out, "CONFIG.md"), "w").write("\n".join(L) + "\n")
    print(f"COMMANDS.md: {len(by_name)} commands")
    print(f"CONFIG.md:   {total} options, {documented_purpose} with a purpose")


if __name__ == "__main__":
    main()
