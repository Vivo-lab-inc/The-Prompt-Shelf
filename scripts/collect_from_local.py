#!/usr/bin/env python3
"""
Collect rules from locally cloned repos (no GitHub API needed).

Usage:
  # First clone the repos:
  git clone --depth 1 https://github.com/PatrickJS/awesome-cursorrules.git /tmp/awesome-cursorrules

  # Then run:
  python scripts/collect_from_local.py
  python scripts/collect_from_local.py --dry-run
"""

import json
import re
import hashlib
from pathlib import Path

RULES_JSON = Path(__file__).parent.parent / "src" / "data" / "rules.json"
AWESOME_DIR = Path("/tmp/awesome-cursorrules/rules")


def detect_metadata(content: str, dir_name: str) -> dict:
    text = (content + " " + dir_name).lower()

    # Language
    lang_map = {
        "TypeScript": ["typescript", "tsx", " ts "],
        "JavaScript": ["javascript", " js ", "nodejs", "node.js"],
        "Python": ["python", "pip", "pytest", "fastapi", "django", "flask"],
        "Go": ["golang", " go ", ".go"],
        "Rust": ["rust", "cargo"],
        "Java": ["java", "spring", "maven", "gradle"],
        "Ruby": ["ruby", "rails"],
        "Swift": ["swift", "swiftui", "ios"],
        "Kotlin": ["kotlin", "android", "jetpack"],
        "C#": ["c#", "csharp", ".net", "dotnet", "aspnet", "blazor"],
        "C++": ["c++", "cpp"],
        "PHP": ["php", "laravel", "symfony", "wordpress"],
        "Dart": ["dart", "flutter"],
        "Elixir": ["elixir", "phoenix"],
        "Lua": ["lua", "dragonruby"],
    }
    language = "Any"
    for lang, keywords in lang_map.items():
        if any(k in text for k in keywords):
            language = lang
            break

    # Framework
    fw_map = {
        "Next.js": ["next.js", "nextjs"],
        "React": ["react"],
        "Vue": ["vue", "nuxt"],
        "Svelte": ["svelte", "sveltekit"],
        "Astro": ["astro"],
        "Angular": ["angular"],
        "FastAPI": ["fastapi"],
        "Django": ["django"],
        "Flask": ["flask"],
        "Express": ["express"],
        "Rails": ["rails"],
        "Spring": ["spring"],
        "Laravel": ["laravel"],
        "Flutter": ["flutter"],
        "Tailwind": ["tailwind"],
        "Shadcn UI": ["shadcn"],
        "Convex": ["convex"],
        "Supabase": ["supabase"],
        "Prisma": ["prisma"],
        "WordPress": ["wordpress"],
        "Cypress": ["cypress"],
        "Jetpack Compose": ["jetpack compose"],
    }
    framework = "Any"
    for fw, keywords in fw_map.items():
        if any(k in text for k in keywords):
            framework = fw
            break

    # Category
    cat_keywords = {
        "web-frontend": ["react", "vue", "svelte", "next", "frontend", "css", "html", "ui", "component", "tailwind", "angular"],
        "backend": ["api", "server", "backend", "database", "auth", "rest", "graphql", "fastapi", "django", "flask", "express", "rails", "spring"],
        "mobile": ["ios", "android", "react native", "flutter", "mobile", "jetpack", "swiftui"],
        "cli": ["cli", "command line", "terminal"],
        "devops": ["docker", "kubernetes", "ci/cd", "deploy", "infra", "terraform"],
        "testing": ["test", "cypress", "jest", "pytest", "testing"],
        "data": ["data", "ml", "machine learning", "ai", "pandas"],
        "security": ["security", "auth", "permission"],
        "game": ["game", "unity", "dragonruby", "simulation"],
    }
    category = "web-frontend"
    best_score = 0
    for cat, keywords in cat_keywords.items():
        score = sum(1 for k in keywords if k in text)
        if score > best_score:
            best_score = score
            category = cat

    # Tags
    all_tags = [
        "react", "nextjs", "vue", "svelte", "astro", "angular",
        "typescript", "javascript", "python", "go", "rust", "java", "ruby", "swift", "kotlin", "php", "dart", "elixir",
        "tailwind", "css", "shadcn-ui",
        "fastapi", "django", "flask", "express", "rails", "spring", "laravel",
        "docker", "kubernetes", "terraform",
        "testing", "cypress", "jest", "vitest", "pytest",
        "graphql", "rest", "api", "grpc",
        "prisma", "supabase", "mongodb", "postgresql",
        "auth", "security", "performance", "seo", "accessibility",
        "monorepo", "turborepo",
        "storybook", "component-library",
        "mobile", "ios", "android", "flutter", "react-native",
        "wordpress", "chrome-extension",
        "game", "ai", "machine-learning",
    ]
    tags = sorted([t for t in all_tags if t in text or t.replace("-", " ") in text])[:8]

    return {"language": language, "framework": framework, "category": category, "tags": tags}


def make_title(dir_name: str, content: str) -> str:
    """Generate title from dir name or content."""
    # Try first heading in content
    for line in content.split('\n')[:10]:
        line = line.strip()
        if line.startswith('# ') and 3 < len(line) < 80:
            t = line[2:].strip()
            if t.lower() not in ("cursorrules", ".cursorrules", "rules"):
                return t

    # Clean dir name
    name = dir_name
    # Remove common suffixes
    for suffix in ["-cursorrules-prompt-file", "-cursorrules-pro", "-cursorrules-prompt-fil", "-cursorrules"]:
        name = name.replace(suffix, "")
    name = name.replace('-', ' ').replace('_', ' ').strip().title()
    return name[:80]


def make_description(content: str, dir_name: str) -> str:
    """Generate description from content."""
    # Try first non-heading paragraph
    lines = content.split('\n')
    for line in lines[:20]:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-') and not line.startswith('```') and len(line) > 30:
            return line[:200]

    # Try extracting "You are..." line
    for line in lines[:5]:
        if 'you are' in line.lower() and len(line.strip()) > 20:
            return line.strip()[:200]

    return f"Curated .cursorrules configuration from awesome-cursorrules."


def collect_awesome() -> list[dict]:
    if not AWESOME_DIR.exists():
        print(f"Directory not found: {AWESOME_DIR}")
        print("Run: git clone --depth 1 https://github.com/PatrickJS/awesome-cursorrules.git /tmp/awesome-cursorrules")
        return []

    rules = []
    dirs = sorted(AWESOME_DIR.iterdir())
    print(f"Found {len(dirs)} rule directories")

    for rule_dir in dirs:
        if not rule_dir.is_dir():
            continue

        # Find .cursorrules file
        cursorrule = None
        for name in [".cursorrules", "cursorrules", ".cursorules"]:
            f = rule_dir / name
            if f.exists():
                cursorrule = f
                break

        if not cursorrule:
            # Check subdirs
            for sub in rule_dir.iterdir():
                if sub.is_file() and sub.name in (".cursorrules", "cursorrules"):
                    cursorrule = sub
                    break

        if not cursorrule:
            continue

        content = cursorrule.read_text(errors="replace")
        if len(content) < 30:
            continue
        if len(content) > 15000:
            content = content[:15000] + "\n\n... (truncated)"

        dir_name = rule_dir.name
        meta = detect_metadata(content, dir_name)
        title = make_title(dir_name, content)
        desc = make_description(content, dir_name)
        rule_id = re.sub(r'[^a-z0-9-]', '', dir_name.lower().replace('_', '-'))
        # Shorten ID
        for suffix in ["-cursorrules-prompt-file", "-cursorrules-pro", "-cursorrules-prompt-fil", "-cursorrules"]:
            rule_id = rule_id.replace(suffix, "")
        rule_id = rule_id[:60].strip('-')

        rules.append({
            "id": rule_id,
            "title": title,
            "title_ja": "",
            "description": desc,
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
        })

    print(f"Collected {len(rules)} rules")
    return rules


def merge_rules(existing: list[dict], new_rules: list[dict]) -> list[dict]:
    existing_ids = {r["id"] for r in existing}
    existing_hashes = {hashlib.md5(r["content"][:500].encode()).hexdigest() for r in existing}

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

    print(f"Added {added} new rules (total: {len(merged)})")
    return merged


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    existing = []
    if RULES_JSON.exists():
        existing = json.loads(RULES_JSON.read_text())
        print(f"Existing: {len(existing)} rules")

    new_rules = collect_awesome()
    if not new_rules:
        return

    merged = merge_rules(existing, new_rules)

    if args.dry_run:
        print(f"[DRY RUN] Would write {len(merged)} rules")
        for r in new_rules[:10]:
            print(f"  {r['id']}: {r['title']} [{r['language']}] [{r['framework']}] [{r['category']}]")
        return

    RULES_JSON.write_text(json.dumps(merged, indent=2, ensure_ascii=False))
    print(f"Wrote {len(merged)} rules to {RULES_JSON}")


if __name__ == "__main__":
    main()
