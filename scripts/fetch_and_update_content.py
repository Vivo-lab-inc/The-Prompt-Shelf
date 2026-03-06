#!/usr/bin/env python3
"""Fetch full content for AGENTS.md and CLAUDE.md rules and update rules.json."""
import json
import urllib.request
from pathlib import Path

RULES_JSON = Path(__file__).parent.parent / "src" / "data" / "rules.json"

# Map rule IDs to raw GitHub URLs
CONTENT_URLS = {
    "agents-md-openai-codex": "https://raw.githubusercontent.com/openai/codex/main/AGENTS.md",
    "agents-md-prisma-orm": "https://raw.githubusercontent.com/prisma/prisma/main/AGENTS.md",
    "agents-md-bun-runtime": "https://raw.githubusercontent.com/oven-sh/bun/main/AGENTS.md",
    "agents-md-calcom": "https://raw.githubusercontent.com/calcom/cal.com/main/AGENTS.md",
    "agents-md-cloudflare-workers": "https://raw.githubusercontent.com/cloudflare/workers-sdk/main/AGENTS.md",
    "agents-md-sveltekit": "https://raw.githubusercontent.com/sveltejs/kit/main/AGENTS.md",
    "claude-md-excalidraw": "https://raw.githubusercontent.com/excalidraw/excalidraw/master/CLAUDE.md",
    "claude-md-overreacted-dan-abramov": "https://raw.githubusercontent.com/gaearon/overreacted.io/main/CLAUDE.md",
    "claude-md-mcp-typescript-sdk": "https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/CLAUDE.md",
    "claude-md-claude-code-action": "https://raw.githubusercontent.com/anthropics/claude-code-action/main/CLAUDE.md",
    "claude-md-pytorch-image-models": "https://raw.githubusercontent.com/huggingface/pytorch-image-models/main/CLAUDE.md",
}

rules = json.loads(RULES_JSON.read_text())

updated = 0
for rule in rules:
    if rule["id"] not in CONTENT_URLS:
        continue
    url = CONTENT_URLS[rule["id"]]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
        # Truncate very long content to 15000 chars for reasonable card previews
        if len(content) > 15000:
            content = content[:15000] + "\n\n... [truncated — full content at source]"
        rule["content"] = content
        updated += 1
        print(f"  OK: {rule['id']} ({len(content)} chars)")
    except Exception as e:
        print(f"  FAIL: {rule['id']} — {e}")

RULES_JSON.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n")
print(f"\nUpdated {updated} rules with full content.")
