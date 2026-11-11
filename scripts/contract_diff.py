#!/usr/bin/env python3
"""contract_diff.py - Larry's rule (BUILD_STANDARDS section 11): which EXISTING exported
features does a change alter or remove?

Compares every Eiffel class under the library's source (not its tests) between a base
ref and a head ref of one git repository, and lists, for exported features that exist
in the base:
  - removed (or made secret),
  - changed signature (arguments or result type),
  - changed export,
  - changed precondition (require) or postcondition (ensure),
and any changed class invariant, or a class removed. New features, new classes and
contracts on new features are not listed. Comments and spacing are ignored.

An empty list means no consumer run is needed. A non-empty list means: find the
consumers that call those features (a search across the simple_* tree) and run their
suites with contracts on, before the merge.

Usage:
  python3 contract_diff.py <repo> [<base> [<head>]]      (default base main, head HEAD)
Exit status: 0 with an empty list, 1 when something is listed, 2 on a usage error.
"""

import re
import subprocess
import sys

TEST_DIRS = ("testing", "tests", "test", "testing_print", "testing_gui")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def changed_classes(repo, base, head):
    out = git(repo, "diff", "--name-status", base + "..." + head, "--", "*.e")
    result = []
    for line in out.splitlines():
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        old_path = parts[1] if status.startswith("R") else path
        top = path.split("/")[0]
        if top in TEST_DIRS or "/testing" in path or path.startswith("EIFGENs"):
            continue
        result.append((status[0], old_path, path))
    return result


def strip_comment(line):
    # Remove an Eiffel comment, leaving "--" inside a string alone.
    out, in_str, i = [], False, 0
    while i < len(line):
        c = line[i]
        if c == '"':
            in_str = not in_str
        if not in_str and line.startswith("--", i):
            break
        if c == "%" and in_str and i + 1 < len(line):
            out.append(line[i:i + 2])
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out).rstrip()


def norm(lines):
    text = " ".join(strip_comment(l).strip() for l in lines)
    return re.sub(r"\s+", " ", text).strip()


BLOCK_END = re.compile(r"^\t\t(require|local|do|once|deferred|external|attribute|ensure|rescue|end)\b")


def parse_class(text):
    """Answer (exported features, invariant). features: name -> dict(sig, export, require, ensure)."""
    lines = text.replace("\r\n", "\n").split("\n")
    features, export, invariant = {}, None, []
    i, n = 0, len(lines)
    in_invariant = False
    while i < n:
        line = lines[i]
        if re.match(r"^feature\b", line):
            m = re.match(r"^feature\s*(\{[^}]*\})?", line)
            export = (m.group(1) or "{ANY}").replace(" ", "")
            in_invariant = False
            i += 1
            continue
        if re.match(r"^invariant\b", line):
            in_invariant = True
            i += 1
            continue
        if re.match(r"^end\b", line):
            in_invariant = False
            i += 1
            continue
        if in_invariant:
            if strip_comment(line).strip():
                invariant.append(line)
            i += 1
            continue
        m = re.match(r"^\t(frozen\s+)?([a-zA-Z_][\w]*(\s*,\s*(frozen\s+)?[a-zA-Z_][\w]*)*)(.*)$", line)
        if export is not None and m and not line.startswith("\t\t"):
            names = [x.strip().replace("frozen ", "").strip() for x in m.group(2).split(",")]
            sig_lines = [m.group(5)]
            j = i + 1
            # A long signature continues on deeper-indented lines that are not comments,
            # before the feature's first two-tab line (its header comment or its body).
            while j < n and lines[j].startswith("\t\t\t") and not lines[j].strip().startswith("--"):
                sig_lines.append(lines[j])
                j += 1
            body = []
            while j < n and (lines[j].startswith("\t\t") or not lines[j].strip()):
                body.append(lines[j])
                j += 1
            req, ens, mode = [], [], None
            for b in body:
                if re.match(r"^\t\trequire\b", b):
                    mode = "req"
                    rest = b.strip()[len("require"):]
                    if rest.strip().startswith("else"):
                        req.append("else")
                    continue
                if re.match(r"^\t\tensure\b", b):
                    mode = "ens"
                    rest = b.strip()[len("ensure"):]
                    if rest.strip().startswith("then"):
                        ens.append("then")
                    continue
                if BLOCK_END.match(b):
                    mode = None
                    continue
                if mode == "req":
                    req.append(b)
                elif mode == "ens":
                    ens.append(b)
            secret = export in ("{NONE}",)
            if not secret:
                for nm in names:
                    features[nm] = {
                        "sig": norm(sig_lines),
                        "export": export,
                        "require": norm(req),
                        "ensure": norm(ens),
                    }
            i = j
            continue
        i += 1
    return features, norm(invariant)


def class_name(text):
    m = re.search(r"^(?:deferred\s+|expanded\s+|frozen\s+)*class\s+([A-Z_][A-Z0-9_]*)", text, re.M)
    return m.group(1) if m else "?"


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    repo = argv[1]
    base = argv[2] if len(argv) > 2 else "main"
    head = argv[3] if len(argv) > 3 else "HEAD"
    findings = []
    for status, old_path, path in changed_classes(repo, base, head):
        old = git(repo, "show", base + ":" + old_path) if status != "A" else ""
        if not old:
            continue
        new = git(repo, "show", head + ":" + path) if status != "D" else ""
        cname = class_name(old)
        if not new:
            findings.append(f"{cname}: class removed ({old_path})")
            continue
        ofeat, oinv = parse_class(old)
        nfeat, ninv = parse_class(new)
        for name, o in sorted(ofeat.items()):
            nf = nfeat.get(name)
            if nf is None:
                findings.append(f"{cname}.{name}: removed or made secret")
                continue
            for key, label in (("sig", "signature"), ("export", "export"),
                               ("require", "precondition"), ("ensure", "postcondition")):
                if o[key] != nf[key]:
                    findings.append(f"{cname}.{name}: {label} changed\n    before: {o[key] or '(none)'}\n    after:  {nf[key] or '(none)'}")
        if oinv != ninv:
            findings.append(f"{cname}: class invariant changed\n    before: {oinv or '(none)'}\n    after:  {ninv or '(none)'}")
    print(f"contract_diff {repo} {base}...{head}")
    if findings:
        print(f"{len(findings)} change(s) to existing exported features:")
        for f in findings:
            print("  " + f)
        return 1
    print("No existing exported feature changed: no consumer run needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
