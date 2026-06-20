#!/usr/bin/env python3
"""Extract and normalize file_path from a Claude Code hook JSON payload.

Handles both valid JSON (properly escaped backslashes) and the Windows edge
case where Claude Code sends raw backslashes that make the JSON technically
invalid — the regex fallback covers that case.
"""

import json
import re
import sys

data = sys.stdin.read()
fp = ""
try:
    d = json.loads(data)
    fp = d.get("tool_input", {}).get("file_path", "")
except Exception:
    m = re.search(r'"file_path"\s*:\s*"([^"]*)"', data)
    if m:
        fp = m.group(1)

print(fp.replace("\\", "/"))
