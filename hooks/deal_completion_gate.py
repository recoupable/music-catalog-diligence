#!/usr/bin/env python3
"""recoup-catalogs-plugin Stop-hook completion gate.

Stays SILENT (exit 0, no stdout) unless the project is a catalog deal workspace
(cwd contains a `deals/` directory) AND one of:
  * Gate A — the agent's last message claims a deal package is ready (or finalized
             a memo under deals/{deal-id}/memos/), or
  * Gate B — the most recent user message launched /recoup-catalog-deal or
             /recoup-catalog-demo (an end-to-end run).
Only then does it run the shipped validators and block on failure.

Fails OPEN (stays silent) on any error or uncertainty — a false block is worse
than a missed one; the point is to remove noise without weakening the real gate
when it is genuinely in-context.

NOTE for maintainers: this assumes (1) run-deal-checks.py / validate-dashboard.py
signal pass/fail via exit code and/or a trailing JSON {"status": "ok"} line, and
(2) the transcript JSONL uses {"type":"assistant"|"user","message":{"content":[...]}}.
Confirm both against the real scripts/transcript and adjust if they differ.
"""
import glob
import json
import os
import re
import subprocess
import sys

# Deal/package-level completion language only — NOT bare "done"/"ready", so that
# scoped single-phase runs (ingest, analyze, kickoff) remain silent.
CLAIM_RE = re.compile(
    r"(package is (ready|complete|done|shareable)"
    r"|deal( package)? is (ready|complete|done|shareable)"
    r"|ready for (the )?(ic|review|the buyer|the seller|the lender|signing)"
    r"|ready to (share|send)( (it|this|the (deal|package)))?"
    r"|(deal|package) is good to go)",
    re.IGNORECASE,
)
MEMO_RE = re.compile(
    r"memos/(ic-memo|seller-cleanup-report|financing-pack|post-close-admin-plan)",
    re.IGNORECASE,
)
E2E_RE = re.compile(r"/recoup-catalog-(deal|demo)\b", re.IGNORECASE)


def silent():
    sys.exit(0)  # no stdout => the hook is invisible


def iter_events(path):
    if not path or not os.path.isfile(path):
        return
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue
    except Exception:
        return


def text_of(ev):
    content = ev.get("message", {}).get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            p.get("text", "") for p in content
            if isinstance(p, dict) and p.get("type") == "text"
        )
    return ""


def last_assistant_and_user(path):
    last_asst, last_user = "", ""
    for ev in iter_events(path):
        kind = ev.get("type")
        if kind == "assistant":
            t = text_of(ev)
            if t.strip():
                last_asst = t
        elif kind == "user":
            t = text_of(ev)
            if t.strip():
                last_user = t
    return last_asst, last_user


def newest_deal(deals_dir):
    dirs = [d for d in glob.glob(os.path.join(deals_dir, "*")) if os.path.isdir(d)]
    return max(dirs, key=os.path.getmtime) if dirs else None


def validator_ok(project_dir, script_name, deal_rel):
    script = os.path.join(os.environ.get("CLAUDE_PLUGIN_ROOT", ""), "scripts", script_name)
    if not os.path.isfile(script):
        return True  # can't validate -> fail open (stay silent)
    try:
        proc = subprocess.run(
            [sys.executable, script, deal_rel],
            cwd=project_dir, capture_output=True, text=True, timeout=90,
        )
    except Exception:
        return True
    if proc.returncode != 0:
        return False
    try:  # honor a trailing JSON {"status": "..."} line if the validator prints one
        result = json.loads(proc.stdout.strip().splitlines()[-1])
        if isinstance(result, dict) and "status" in result:
            return result["status"] == "ok"
    except Exception:
        pass
    return True


def block(reason, system_message):
    print(json.dumps({"decision": "block", "reason": reason, "systemMessage": system_message}))
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        silent()

    cwd = data.get("cwd") or ""
    deals_dir = os.path.join(cwd, "deals")
    if not cwd or not os.path.isdir(deals_dir):  # gate 1: workspace relevance
        silent()

    ws = newest_deal(deals_dir)
    if ws is None:
        silent()
    deal_rel = os.path.relpath(ws, cwd)

    last_asst, last_user = last_assistant_and_user(data.get("transcript_path") or "")

    # Gate A — completion claim in the agent's last message
    if CLAIM_RE.search(last_asst) or MEMO_RE.search(last_asst):
        if not validator_ok(cwd, "run-deal-checks.py", deal_rel):
            block(
                "deal package claimed ready but scripts/run-deal-checks.py did not pass",
                "Resolve the completion-gate items before declaring the package ready: run "
                "python3 scripts/run-deal-checks.py %s, confirm assumptions.yaml and "
                "evidence-ledger.json exist and findings are closed or explicitly listed as "
                "open, then disclose any remaining gap explicitly." % deal_rel,
            )
        silent()

    # Gate B — an end-to-end run must land a validated dashboard
    if E2E_RE.search(last_user):
        dashboard = os.path.join(ws, "DASHBOARD.html")
        if not os.path.isfile(dashboard) or not validator_ok(cwd, "validate-dashboard.py", deal_rel):
            block(
                "end-to-end workflow active but DASHBOARD.html missing or not validated",
                "/recoup-catalog-deal expects %s/DASHBOARD.html to exist AND pass "
                "scripts/validate-dashboard.py. Run the recoup-catalog-dashboard skill to write "
                "the HTML, then run the validator and fix any errors before stopping." % deal_rel,
            )
        silent()

    silent()


if __name__ == "__main__":
    main()
