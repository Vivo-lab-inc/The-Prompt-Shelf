#!/usr/bin/env python3
"""
Rule collector for The-Prompt-Shelf.
Collects .cursorrules, CLAUDE.md, and AGENTS.md from GitHub repositories.

Sources:
1. GitHub Search API — search for files named .cursorrules, CLAUDE.md, AGENTS.md
2. awesome-cursorrules repo — curated list
3. cursor.directory API — if available

Usage:
  python scripts/collect_rules.py
  python scripts/collect_rules.py --source github
  python scripts/collect_rules.py --source awesome
"""

import json
import os
import re
import sys
import time
import hashlib
import argparse
import urllib.request
import urllib.error
from pathlib import Path

RULES_JSON = Path(__file__).parent.parent / "src" / "data" / "rules.json"
COLLECTED_DIR = Path(__file__).parent / "collected"
COLLECTED_DIR.mkdir(exist_ok=True)

# GitHub API (unauthenticated: 10 req/min, authenticated: 30 req/min)
GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "ThePromptShelf/1.0",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


def github_request(url: str) -> dict | list | None:
    """Make a GitHub API request with rate limit handling."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            remaining = resp.headers.get("X-RateLimit-Remaining", "?")
            print(f"  [rate-limit remaining: {remaining}]")
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            reset = int(e.headers.get("X-RateLimit-Reset", 0))
            wait = max(reset - int(time.time()), 60)
            print(f"  Rate limited. Waiting {wait}s...")
            time.sleep(wait)
            return github_request(url)
        elif e.code == 422:
            print(f"  Validation error for {url}")
            return None
        else:
            print(f"  HTTP {e.code}: {e.reason} for {url}")
            return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def fetch_file_content(url: str) -> str | None:
    """Fetch raw file content from GitHub."""
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "ThePromptShelf/1.0",
        **({"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  Failed to fetch content: {e}")
        return None


def detect_metadata(content: str, repo_name: str, file_path: str, format_type: str) -> dict:
    """Detect language, framework, category from content and repo name."""
    text = (content + " " + repo_name + " " + file_path).lower()

    # Language detection
    lang_map = {
        "typescript": ["typescript", "tsx", ".ts"],
        "python": ["python", ".py", "pip", "pytest"],
        "go": [" go ", "golang", ".go"],
        "rust": ["rust", "cargo", ".rs"],
        "java": ["java", "spring", "maven", "gradle"],
        "ruby": ["ruby", "rails", ".rb"],
        "swift": ["swift", "swiftui", "ios"],
        "kotlin": ["kotlin", "android"],
        "c#": ["c#", "csharp", ".net", "dotnet"],
        "php": ["php", "laravel", "symfony"],
    }
    language = "Any"
    for lang, keywords in lang_map.items():
        if any(k in text for k in keywords):
            language = lang.title() if lang != "c#" else "C#"
            break

    # Framework detection
    fw_map = {
        "Next.js": ["next.js", "nextjs", "next js"],
        "React": ["react", "jsx"],
        "Vue": ["vue", "nuxt"],
        "Svelte": ["svelte", "sveltekit"],
        "Astro": ["astro"],
        "Angular": ["angular"],
        "FastAPI": ["fastapi"],
        "Django": ["django"],
        "Flask": ["flask"],
        "Express": ["express"],
        "Rails": ["rails"],
        "Spring": ["spring boot", "spring"],
        "Laravel": ["laravel"],
        "Tailwind": ["tailwind"],
    }
    framework = "Any"
    for fw, keywords in fw_map.items():
        if any(k in text for k in keywords):
            framework = fw
            break

    # Category detection
    cat_keywords = {
        "web-frontend": ["react", "vue", "svelte", "next", "frontend", "css", "html", "ui", "component"],
        "backend": ["api", "server", "backend", "database", "auth", "rest", "graphql"],
        "mobile": ["ios", "android", "react native", "flutter", "mobile"],
        "cli": ["cli", "command line", "terminal"],
        "devops": ["docker", "kubernetes", "ci/cd", "deploy", "infra", "terraform"],
        "data": ["data", "ml", "machine learning", "ai", "pandas", "numpy"],
        "security": ["security", "auth", "permission", "encrypt"],
    }
    category = "backend"  # default
    best_score = 0
    for cat, keywords in cat_keywords.items():
        score = sum(1 for k in keywords if k in text)
        if score > best_score:
            best_score = score
            category = cat

    # Tag extraction
    tag_candidates = set()
    all_tags = [
        "react", "nextjs", "vue", "svelte", "astro", "angular",
        "typescript", "javascript", "python", "go", "rust", "java", "ruby", "swift", "kotlin",
        "tailwind", "css", "sass", "styled-components",
        "fastapi", "django", "flask", "express", "rails", "spring", "laravel",
        "docker", "kubernetes", "terraform", "ci-cd",
        "testing", "jest", "vitest", "pytest",
        "graphql", "rest", "api", "grpc",
        "prisma", "drizzle", "sqlalchemy", "mongodb",
        "auth", "security", "performance", "seo", "accessibility",
        "monorepo", "turborepo", "nx",
        "storybook", "component-library",
        "mobile", "ios", "android", "react-native", "flutter",
    ]
    for tag in all_tags:
        if tag in text or tag.replace("-", " ") in text:
            tag_candidates.add(tag)

    return {
        "language": language,
        "framework": framework,
        "category": category,
        "tags": sorted(list(tag_candidates))[:8],  # max 8 tags
    }


def make_id(repo_name: str, file_path: str) -> str:
    """Generate a URL-safe unique ID."""
    raw = f"{repo_name}/{file_path}".lower()
    # Clean up
    raw = re.sub(r'[^a-z0-9/\-]', '-', raw)
    raw = re.sub(r'-+', '-', raw).strip('-')
    # Shorten
    parts = raw.split('/')
    if len(parts) > 2:
        raw = f"{parts[0]}-{parts[-1]}"
    # Ensure uniqueness with hash suffix
    h = hashlib.md5(f"{repo_name}/{file_path}".encode()).hexdigest()[:6]
    slug = re.sub(r'-+', '-', raw.replace('/', '-'))[:50].strip('-')
    return f"{slug}-{h}"


def make_title(repo_name: str, file_path: str, content: str) -> str:
    """Generate a human-readable title."""
    # Try to extract from content (first heading)
    for line in content.split('\n')[:10]:
        line = line.strip()
        if line.startswith('# ') and len(line) > 3:
            title = line[2:].strip()
            if len(title) > 5 and title not in ("CLAUDE.md", "AGENTS.md"):
                return title[:80]

    # Fall back to repo name
    name = repo_name.split('/')[-1]
    name = name.replace('-', ' ').replace('_', ' ').title()
    return name[:80]


def search_github_files(filename: str, max_results: int = 50) -> list[dict]:
    """Search GitHub for files with a specific name."""
    print(f"\nSearching GitHub for '{filename}'...")
    results = []
    seen_repos = set()

    # Search with different quality signals
    queries = [
        f"filename:{filename} stars:>10",
        f"filename:{filename} stars:>5",
        f"filename:{filename} stars:>1",
    ]

    for query in queries:
        if len(results) >= max_results:
            break

        url = f"{GITHUB_API}/search/code?q={urllib.parse.quote(query)}&per_page=30"
        data = github_request(url)
        if not data or "items" not in data:
            continue

        print(f"  Found {data.get('total_count', 0)} total, processing {len(data['items'])} items...")

        for item in data["items"]:
            repo = item["repository"]
            repo_name = repo["full_name"]

            if repo_name in seen_repos:
                continue
            seen_repos.add(repo_name)

            # Get repo details for stars
            repo_data = github_request(f"{GITHUB_API}/repos/{repo_name}")
            if not repo_data:
                continue
            stars = repo_data.get("stargazers_count", 0)
            repo_desc = repo_data.get("description", "") or ""

            # Fetch file content
            content_url = item.get("url", "")
            content = fetch_file_content(content_url)
            if not content or len(content) < 50:
                print(f"  Skipping {repo_name} (content too short)")
                continue
            if len(content) > 15000:
                content = content[:15000] + "\n\n... (truncated)"

            # Detect format
            fname = item["name"]
            if fname == ".cursorrules" or fname == ".cursorules":
                format_type = ".cursorrules"
                tool = "cursor"
            elif fname.upper() == "CLAUDE.md" or fname == "CLAUDE.md":
                format_type = "CLAUDE.md"
                tool = "claude-code"
            elif fname.upper() == "AGENTS.md":
                format_type = "AGENTS.md"
                tool = "agents-md"
            else:
                format_type = fname
                tool = "cursor"

            meta = detect_metadata(content, repo_name, item["path"], format_type)
            title = make_title(repo_name, item["path"], content)
            rule_id = make_id(repo_name, item["path"])

            rule = {
                "id": rule_id,
                "title": title,
                "title_ja": "",
                "description": f"From {repo_name} ({stars} stars). {repo_desc[:120]}",
                "description_ja": "",
                "tool": tool,
                "format": format_type,
                "language": meta["language"],
                "framework": meta["framework"],
                "category": meta["category"],
                "tags": meta["tags"],
                "author": repo_name.split("/")[0],
                "source": f"github:{repo_name}",
                "stars": stars,
                "content": content,
            }
            results.append(rule)
            print(f"  + {title} ({repo_name}, {stars}★)")

            time.sleep(1)  # Be gentle with API

            if len(results) >= max_results:
                break

        time.sleep(2)  # Between search queries

    return results


def collect_awesome_cursorrules() -> list[dict]:
    """Collect rules from awesome-cursorrules repository."""
    print("\nCollecting from awesome-cursorrules...")
    results = []

    # Get the repo's rules directory listing
    url = f"{GITHUB_API}/repos/PatrickJS/awesome-cursorrules/contents/rules"
    items = github_request(url)
    if not items or not isinstance(items, list):
        print("  Failed to list awesome-cursorrules/rules/")
        return results

    print(f"  Found {len(items)} rule directories")

    for item in items[:60]:  # Process up to 60
        if item["type"] != "dir":
            continue

        dir_name = item["name"]
        # Look for .cursorrules file inside
        dir_url = f"{GITHUB_API}/repos/PatrickJS/awesome-cursorrules/contents/rules/{dir_name}"
        dir_items = github_request(dir_url)
        if not dir_items:
            continue

        cursorrule_file = None
        for f in dir_items:
            if f["name"] in (".cursorrules", "cursorrules", ".cursorules"):
                cursorrule_file = f
                break

        if not cursorrule_file:
            continue

        content = fetch_file_content(cursorrule_file["url"])
        if not content or len(content) < 50:
            continue
        if len(content) > 15000:
            content = content[:15000] + "\n\n... (truncated)"

        meta = detect_metadata(content, f"awesome-cursorrules/{dir_name}", dir_name, ".cursorrules")
        title = dir_name.replace('-', ' ').replace('_', ' ').title()

        # Try to get better title from content
        for line in content.split('\n')[:5]:
            if line.strip().startswith('You are') and len(line.strip()) < 100:
                title = line.strip()[:80]
                break

        rule_id = f"awesome-{dir_name}"[:60]

        rule = {
            "id": rule_id,
            "title": title,
            "title_ja": "",
            "description": f"Curated .cursorrules from awesome-cursorrules collection.",
            "description_ja": "",
            "tool": "cursor",
            "format": ".cursorrules",
            "language": meta["language"],
            "framework": meta["framework"],
            "category": meta["category"],
            "tags": meta["tags"],
            "author": "awesome-cursorrules",
            "source": "awesome-cursorrules",
            "stars": 0,
            "content": content,
        }
        results.append(rule)
        print(f"  + {title}")

        time.sleep(0.5)

    return results


def merge_rules(existing: list[dict], new_rules: list[dict]) -> list[dict]:
    """Merge new rules into existing, avoiding duplicates by content similarity."""
    existing_ids = {r["id"] for r in existing}
    # Simple dedup by content hash
    existing_hashes = set()
    for r in existing:
        h = hashlib.md5(r["content"][:500].encode()).hexdigest()
        existing_hashes.add(h)

    merged = list(existing)
    added = 0
    for rule in new_rules:
        if rule["id"] in existing_ids:
            continue
        h = hashlib.md5(rule["content"][:500].encode()).hexdigest()
        if h in existing_hashes:
            continue
        merged.append(rule)
        existing_ids.add(rule["id"])
        existing_hashes.add(h)
        added += 1

    print(f"\nMerged: {added} new rules added (total: {len(merged)})")
    return merged


def main():
    parser = argparse.ArgumentParser(description="Collect rules for The-Prompt-Shelf")
    parser.add_argument("--source", choices=["all", "github", "awesome"], default="all")
    parser.add_argument("--max", type=int, default=30, help="Max rules per source")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to rules.json")
    args = parser.parse_args()

    # Load existing
    existing = []
    if RULES_JSON.exists():
        with open(RULES_JSON) as f:
            existing = json.load(f)
        print(f"Loaded {len(existing)} existing rules")

    new_rules = []

    if args.source in ("all", "awesome"):
        new_rules.extend(collect_awesome_cursorrules())

    if args.source in ("all", "github"):
        for filename in [".cursorrules", "CLAUDE.md", "AGENTS.md"]:
            new_rules.extend(search_github_files(filename, max_results=args.max))

    if not new_rules:
        print("No new rules found.")
        return

    # Save raw collected data
    timestamp = int(time.time())
    collected_file = COLLECTED_DIR / f"collected_{timestamp}.json"
    with open(collected_file, "w") as f:
        json.dump(new_rules, f, indent=2, ensure_ascii=False)
    print(f"Raw data saved to {collected_file}")

    # Merge
    merged = merge_rules(existing, new_rules)

    if args.dry_run:
        print(f"\n[DRY RUN] Would write {len(merged)} rules to {RULES_JSON}")
        return

    # Write
    with open(RULES_JSON, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {len(merged)} rules to {RULES_JSON}")


if __name__ == "__main__":
    import urllib.parse
    main()
