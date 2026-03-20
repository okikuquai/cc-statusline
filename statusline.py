#!/usr/bin/env python3
"""Claude Code status line with model stats, git repo, branch, and PR info"""
import json, sys, subprocess
from datetime import datetime, timezone

data = json.load(sys.stdin)

R = '\033[0m'
DIM = '\033[2m'
BOLD = '\033[1m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
MAGENTA = '\033[35m'
GREEN = '\033[32m'
RED = '\033[31m'

def gradient(pct):
    if pct < 50:
        r = int(pct * 5.1)
        return f'\033[38;2;{r};200;80m'
    else:
        g = int(200 - (pct - 50) * 4)
        return f'\033[38;2;255;{max(g, 0)};60m'

def fmt_remaining(resets_at):
    try:
        now = datetime.now(timezone.utc).timestamp()
        total_sec = int(resets_at - now)
        if total_sec <= 0:
            return None
        d, rem = divmod(total_sec, 86400)
        h, rem = divmod(rem, 3600)
        m = rem // 60
        if d > 0:
            return f'{d}d{h}h'
        if h > 0:
            return f'{h}h{m:02d}m'
        return f'{m}m'
    except Exception:
        return None

def dot(pct, resets_at=None):
    p = round(pct)
    remaining = fmt_remaining(resets_at) if resets_at else None
    reset_str = f' {DIM}({remaining}){R}' if remaining else ''
    return f'{gradient(pct)}\u25cf{R} {BOLD}{p}%{R}{reset_str}'

def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=3).stdout.strip()
    except Exception:
        return ''

# --- Model & usage ---
model = data.get('model', {}).get('display_name', 'Claude')
parts = [f'\U0001f916 {BOLD}{model}{R}']

ctx = data.get('context_window', {}).get('used_percentage')
if ctx is not None:
    parts.append(f'\U0001f4ad ctx {dot(ctx)}')

five_hour = data.get('rate_limits', {}).get('five_hour', {})
five = five_hour.get('used_percentage')
if five is not None:
    parts.append(f'\u23f1\ufe0f  5h {dot(five, five_hour.get("resets_at"))}')

seven_day = data.get('rate_limits', {}).get('seven_day', {})
week = seven_day.get('used_percentage')
if week is not None:
    parts.append(f'\U0001f4c5 7d {dot(week, seven_day.get("resets_at"))}')

# --- Git info ---
repo = run(['git', 'rev-parse', '--show-toplevel'])
if repo:
    repo_name = repo.rsplit('/', 1)[-1]
    parts.append(f'\U0001f4c2 {CYAN}{repo_name}{R}')

branch = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
if branch:
    parts.append(f'\U0001f33f {YELLOW}{branch}{R}')

# --- PR info ---
pr_json = run(['gh', 'pr', 'view', '--json', 'number,state,url'])
if pr_json:
    try:
        pr = json.loads(pr_json)
        num = pr.get('number', '')
        state = pr.get('state', '')
        state_icons = {
            'OPEN': (GREEN, '\U0001f7e2'),
            'MERGED': (MAGENTA, '\U0001f7e3'),
            'CLOSED': (RED, '\U0001f534'),
        }
        c, icon = state_icons.get(state, (DIM, '\u2753'))
        parts.append(f'{icon} {c}PR #{num}{R}')
    except (json.JSONDecodeError, KeyError):
        pass

print(f' {DIM}|{R} '.join(parts), end='')
