#!/usr/bin/env python3
"""
daily_collector.py — The Prompt Shelf リアルタイム収集バッチ

毎朝4:00に実行。一次ソースAPIを直接叩いてCLAUDE.md/AGENTS.md/.cursorrules
を収集し、AIキュレーション後にrules.jsonに追加→ビルド→デプロイ。

★ WebSearch（Serper等）は使わない ★
GoogleインデックスはGitHubへのpushから数時間〜数日遅れるため。
代わりに一次ソースAPIを直接叩く（数分〜リアルタイム）。

情報ソース（鮮度順）:
  1. GitHub Search API — pushed:>YYYY-MM-DD で直近コミットを即時検索
  2. GitHub Events API — 公開リポのリアルタイムアクティビティ
  3. awesome-cursorrules/awesome-claude-md リポの最新コミット
  4. cursor.directory (pontusab/directories) の最新追加
  5. Hacker News Algolia API — 投稿数分後からインデックス
  6. Reddit JSON API — r/cursor, r/ClaudeAI 投稿直後から取得可能

使い方:
  python daily_collector.py           # フル実行
  python daily_collector.py --dry-run # 収集のみ（追加・デプロイなし）
  python daily_collector.py --test    # テスト（件数制限）

スケジュール: 毎日 04:00（LaunchAgent）
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# パス・設定
# ============================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
RULES_JSON = PROJECT_DIR / "src" / "data" / "rules.json"
WORKSPACE = Path(__file__).resolve().parent.parent.parent / "Moru_workspace"
SECRETS_FILE = WORKSPACE / ".env.secrets"
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

MAX_TOTAL_RULES = 120
MAX_NEW_PER_RUN = 10
GITHUB_API = "https://api.github.com"
MIN_STARS = 100  # 最低スター数（品質フィルタ）

# ============================================================
# 環境変数
# ============================================================

def load_env() -> dict:
    env = {}
    for ef in [WORKSPACE / ".env", SECRETS_FILE]:
        if not ef.exists():
            continue
        for line in ef.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env

ENV = load_env()
OPENAI_KEY = ENV.get("OPENAI_API_KEY", "")
GITHUB_TOKEN = ENV.get("GITHUB_TOKEN", "")


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def api_get(url: str, headers: dict = None, timeout: int = 15) -> dict | list | None:
    """汎用GETリクエスト"""
    h = {"User-Agent": "PromptShelfCollector/1.0"}
    if headers:
        h.update(headers)
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"  API GET failed ({url[:80]}): {e}")
        return None


# ============================================================
# Source 1: GitHub Search API（★最重要・即時反映）
# ============================================================

def github_search_repos(query: str, sort: str = "updated", limit: int = 30) -> list:
    """GitHub Repository Search — pushed日付指定で最新を取得"""
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    encoded = urllib.parse.quote(query)
    url = f"{GITHUB_API}/search/repositories?q={encoded}&sort={sort}&order=desc&per_page={min(limit, 100)}"
    data = api_get(url, headers)
    if data and "items" in data:
        return data["items"]
    return []


def search_recent_rules(days_back: int = 7) -> list:
    """直近N日間にpushされたCLAUDE.md/AGENTS.md/.cursorrules含むリポを検索"""
    since = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    candidates = []

    searches = [
        (f"filename:CLAUDE.md pushed:>{since} stars:>={MIN_STARS}", "claude-code", "CLAUDE.md"),
        (f"filename:AGENTS.md pushed:>{since} stars:>={MIN_STARS}", "agents-md", "AGENTS.md"),
        # .cursorrules は stars でリポ検索できないので別アプローチ
    ]

    for query, tool, filename in searches:
        log(f"  GitHub Search: {filename} (since {since})")
        # GitHub Code Search は認証必須
        headers = {"Accept": "application/vnd.github+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

        encoded = urllib.parse.quote(query)
        url = f"{GITHUB_API}/search/code?q={encoded}&sort=indexed&order=desc&per_page=30"
        data = api_get(url, headers)
        if data and "items" in data:
            for item in data["items"]:
                repo_full = item.get("repository", {}).get("full_name", "")
                if repo_full:
                    candidates.append({
                        "repo": repo_full,
                        "path": item.get("path", filename),
                        "tool": tool,
                        "format": filename,
                        "source": "github_search",
                    })
        time.sleep(3)  # Code Search rate limit (10 req/min for unauthenticated)

    # リポ検索でスター数の高いCLAUDE.md/AGENTS.md含むリポも追加
    for kw in ["CLAUDE.md", "AGENTS.md"]:
        log(f"  GitHub Repo Search: popular repos with {kw}")
        repos = github_search_repos(f"{kw} in:readme stars:>500", sort="stars", limit=20)
        for r in repos:
            candidates.append({
                "repo": r["full_name"],
                "path": kw,
                "tool": "claude-code" if "CLAUDE" in kw else "agents-md",
                "format": kw,
                "stars": r.get("stargazers_count", 0),
                "description": r.get("description", ""),
                "source": "github_repo_search",
            })
        time.sleep(2)

    return candidates


# ============================================================
# Source 2: キュレーションリポの最新追加を監視
# ============================================================

def check_curated_repos() -> list:
    """awesome-cursorrules等のキュレーションリポの最新コミットを確認"""
    candidates = []
    curated_repos = [
        ("PatrickJS/awesome-cursorrules", "cursor", ".cursorrules"),
        ("josix/awesome-claude-md", "claude-code", "CLAUDE.md"),
        ("pontusab/directories", "cursor", ".cursorrules"),  # cursor.directory source
    ]

    for repo, tool, fmt in curated_repos:
        log(f"  Checking curated repo: {repo}")
        headers = {"Accept": "application/vnd.github+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

        # 最新コミット（直近7日）を取得
        since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00Z")
        url = f"{GITHUB_API}/repos/{repo}/commits?since={since}&per_page=10"
        commits = api_get(url, headers)
        if commits:
            for commit in commits[:5]:
                msg = commit.get("commit", {}).get("message", "")
                if any(kw in msg.lower() for kw in ["add", "new", "update", "feat"]):
                    candidates.append({
                        "repo": repo,
                        "path": fmt,
                        "tool": tool,
                        "format": fmt,
                        "commit_msg": msg[:100],
                        "source": "curated_repo",
                    })
        time.sleep(1)

    return candidates


# ============================================================
# Source 3: Hacker News Algolia API（数分遅延）
# ============================================================

def fetch_hn_rules() -> list:
    """HNからAIコーディングルール関連を検索"""
    candidates = []
    queries = [
        "CLAUDE.md", "AGENTS.md", "cursorrules",
        "AI coding rules", "cursor rules",
    ]

    for q in queries:
        encoded = urllib.parse.quote(q)
        url = f"https://hn.algolia.com/api/v1/search_by_date?query={encoded}&tags=story&hitsPerPage=5"
        data = api_get(url)
        if data and "hits" in data:
            for hit in data["hits"]:
                hit_url = hit.get("url", "")
                if "github.com" in hit_url:
                    match = re.search(r'github\.com/([^/]+/[^/]+)', hit_url)
                    if match:
                        candidates.append({
                            "repo": match.group(1).rstrip('/'),
                            "hn_title": hit.get("title", ""),
                            "hn_points": hit.get("points", 0),
                            "source": "hackernews",
                        })
        time.sleep(0.5)

    return candidates


# ============================================================
# Source 4: Reddit JSON API（即時）
# ============================================================

def fetch_reddit_rules() -> list:
    """RedditからAIルール関連の投稿を取得"""
    candidates = []
    subreddits = ["cursor", "ClaudeAI", "LocalLLaMA", "CodingWithAI"]

    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/search.json?q=cursorrules+OR+CLAUDE.md+OR+AGENTS.md&sort=new&limit=5&restrict_sr=1&t=week"
        data = api_get(url)
        if data and "data" in data:
            posts = data["data"].get("children", [])
            for p in posts:
                pd = p.get("data", {})
                post_url = pd.get("url", "")
                if "github.com" in post_url:
                    match = re.search(r'github\.com/([^/]+/[^/]+)', post_url)
                    if match:
                        candidates.append({
                            "repo": match.group(1).rstrip('/'),
                            "reddit_title": pd.get("title", ""),
                            "reddit_score": pd.get("score", 0),
                            "subreddit": sub,
                            "source": "reddit",
                        })
        time.sleep(1)

    return candidates


# ============================================================
# リポ情報取得 & コンテンツ取得
# ============================================================

def github_get_repo(owner_repo: str) -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return api_get(f"{GITHUB_API}/repos/{owner_repo}", headers) or {}


def fetch_raw_content(owner_repo: str, path: str, branch: str = "main") -> str:
    for b in [branch, "master", "canary", "develop"]:
        url = f"https://raw.githubusercontent.com/{owner_repo}/{b}/{path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8")
                if len(content) > 50:
                    return content
        except:
            continue
    return ""


def detect_rule_file(repo: str, branch: str = "main") -> tuple[str, str, str] | None:
    """リポからCLAUDE.md/AGENTS.md/.cursorrules を自動検出"""
    for fname, tool, fmt in [
        ("CLAUDE.md", "claude-code", "CLAUDE.md"),
        ("AGENTS.md", "agents-md", "AGENTS.md"),
        (".cursorrules", "cursor", ".cursorrules"),
    ]:
        content = fetch_raw_content(repo, fname, branch)
        if content:
            return (fname, tool, fmt)
    return None


# ============================================================
# AI キュレーション (GPT-4o-mini)
# ============================================================

def ai_curate(candidates: list, existing_repos: set) -> list:
    if not OPENAI_KEY or not candidates:
        return candidates[:MAX_NEW_PER_RUN]

    candidate_text = "\n".join(
        f"{i+1}. repo={c.get('repo','?')} stars={c.get('stars',0)} tool={c.get('tool','?')} desc={(c.get('description') or '')[:80]} src={c.get('source','')}"
        for i, c in enumerate(candidates[:40])
    )

    prompt = f"""Select the TOP {MAX_NEW_PER_RUN} most valuable AI coding rules to add to The Prompt Shelf gallery.

Criteria:
- High GitHub stars (popular/trusted)
- Unique framework/language coverage
- Quality content (actionable, well-structured)
- Notable authors or organizations
- NOT duplicates

Already have: {', '.join(list(existing_repos)[:30])}

Candidates:
{candidate_text}

Return ONLY a JSON array of indices (1-based): [1, 5, 12]"""

    try:
        data = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 200,
        }).encode()
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=data,
                                     headers={"Authorization": f"Bearer {OPENAI_KEY}",
                                              "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        text = result["choices"][0]["message"]["content"].strip()
        match = re.search(r'\[[\d,\s]+\]', text)
        if match:
            indices = json.loads(match.group())
            return [candidates[i-1] for i in indices if 0 < i <= len(candidates)][:MAX_NEW_PER_RUN]
    except Exception as e:
        log(f"  AI curation failed: {e}")

    return candidates[:MAX_NEW_PER_RUN]


# ============================================================
# ルール生成
# ============================================================

def generate_rule_entry(candidate: dict) -> dict | None:
    repo = candidate.get("repo", "")
    if not repo or "/" not in repo:
        return None

    repo_info = github_get_repo(repo)
    if not repo_info:
        return None

    stars = repo_info.get("stargazers_count", 0)
    if stars < MIN_STARS:
        log(f"    Skip {repo}: only {stars} stars (min {MIN_STARS})")
        return None

    branch = repo_info.get("default_branch", "main")
    description = repo_info.get("description", "") or ""
    owner = repo.split("/")[0]
    repo_name = repo.split("/")[1]
    language = repo_info.get("language", "Any") or "Any"

    # ルールファイル検出
    tool = candidate.get("tool", "")
    path = candidate.get("path", "")
    fmt = candidate.get("format", "")

    if not tool or not path:
        detected = detect_rule_file(repo, branch)
        if not detected:
            return None
        path, tool, fmt = detected

    # コンテンツ取得
    content = fetch_raw_content(repo, path, branch)
    if not content or len(content) < 100:
        # シンボリックリンクの場合の代替チェック
        for alt in ["CLAUDE.md", "AGENTS.md"]:
            if alt != path:
                alt_content = fetch_raw_content(repo, alt, branch)
                if alt_content and len(alt_content) > 100:
                    content = alt_content
                    break
    if not content or len(content) < 100:
        return None

    if len(content) > 15000:
        content = content[:15000] + "\n\n... [truncated — full content at source]"

    rule_id = f"{tool.replace('-', '')}-{repo_name}".lower().replace(".", "-").replace("_", "-")[:50]
    tool_label = {"cursor": ".cursorrules", "claude-code": "CLAUDE.md", "agents-md": "AGENTS.md"}.get(tool, fmt)

    # フレームワーク推定
    framework = "Any"
    fw_map = {"next": "Next.js", "react": "React", "vue": "Vue", "svelte": "Svelte",
              "django": "Django", "flask": "Flask", "rails": "Rails", "spring": "Spring Boot",
              "rust": "Rust", "go": "Go", "swift": "Swift", "kotlin": "Kotlin",
              "angular": "Angular", "terraform": "Terraform", "k8s": "Kubernetes"}
    combined = f"{repo_name} {description}".lower()
    for kw, fw in fw_map.items():
        if kw in combined:
            framework = fw
            break

    category = "web-frontend"
    if any(w in combined for w in ["backend", "api", "server", "database", "orm"]):
        category = "backend"
    elif any(w in combined for w in ["cli", "terminal", "command"]):
        category = "cli"
    elif any(w in combined for w in ["devops", "deploy", "infra", "kubernetes", "terraform"]):
        category = "devops"

    return {
        "id": rule_id,
        "title": f"{repo_name} — {tool_label}",
        "title_ja": f"{repo_name} — {tool_label}",
        "description": description[:200] if description else f"{tool_label} for {repo_name}",
        "description_ja": description[:200] if description else f"{repo_name}の{tool_label}",
        "tool": tool,
        "format": fmt,
        "language": language,
        "framework": framework,
        "category": category,
        "tags": [t for t in [language.lower(), framework.lower(), tool] if t != "any"],
        "author": owner,
        "source": repo,
        "sourceUrl": f"https://github.com/{repo}/blob/{branch}/{path}",
        "stars": stars,
        "content": content,
    }


# ============================================================
# デプロイ
# ============================================================

def build_and_deploy():
    log("Building site...")
    result = subprocess.run(["npm", "run", "build"], cwd=str(PROJECT_DIR),
                          capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        log(f"  Build failed: {result.stderr[-500:]}")
        return False

    log("Deploying to Cloudflare Pages...")
    result = subprocess.run(
        ["npx", "wrangler", "pages", "deploy", "dist", "--project-name=the-prompt-shelf"],
        cwd=str(PROJECT_DIR), capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        log(f"  Deploy failed: {result.stderr[-500:]}")
        return False

    log("  Deployed!")
    return True


# ============================================================
# メイン
# ============================================================

def main():
    dry_run = "--dry-run" in sys.argv
    test_mode = "--test" in sys.argv

    log("=" * 60)
    log(f"The Prompt Shelf — Daily Collector v2")
    log(f"Mode: {'DRY RUN' if dry_run else 'TEST' if test_mode else 'LIVE'}")
    log("=" * 60)

    # 既存ルール
    rules = json.loads(RULES_JSON.read_text())
    existing_ids = {r["id"] for r in rules}
    existing_repos = {r.get("source", "") for r in rules}
    log(f"Existing: {len(rules)} rules")

    if len(rules) >= MAX_TOTAL_RULES:
        log(f"At {MAX_TOTAL_RULES} limit. Exiting.")
        return

    # === 収集（並列） ===
    log("\n--- Collecting from primary sources ---")
    all_candidates = []

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(search_recent_rules, 7 if not test_mode else 3): "GitHub",
            pool.submit(check_curated_repos): "Curated Repos",
            pool.submit(fetch_hn_rules): "Hacker News",
        }
        if not test_mode:
            futures[pool.submit(fetch_reddit_rules)] = "Reddit"

        for future in as_completed(futures):
            source = futures[future]
            try:
                results = future.result()
                log(f"  {source}: {len(results)} candidates")
                all_candidates.extend(results)
            except Exception as e:
                log(f"  {source} failed: {e}")

    # 重複排除（既存 + 今回内）
    seen = set(existing_repos)
    unique = []
    for c in all_candidates:
        repo = c.get("repo", "")
        if repo and repo not in seen:
            seen.add(repo)
            unique.append(c)
    all_candidates = unique

    # リポ情報取得（スター数等）— まだ持ってない候補のみ
    log(f"\nFetching repo info for {len(all_candidates)} unique candidates...")
    for c in all_candidates:
        if c.get("stars", 0) == 0:
            info = github_get_repo(c["repo"])
            if info:
                c["stars"] = info.get("stargazers_count", 0)
                c["description"] = info.get("description") or ""
            time.sleep(0.5)

    # スター数フィルタ & ソート
    all_candidates = [c for c in all_candidates if c.get("stars", 0) >= MIN_STARS]
    all_candidates.sort(key=lambda x: x.get("stars", 0), reverse=True)
    log(f"After filtering (>={MIN_STARS} stars): {len(all_candidates)} candidates")

    if not all_candidates:
        log("No new candidates. Done.")
        return

    # === AIキュレーション ===
    log("\n--- AI Curation ---")
    selected = ai_curate(all_candidates, existing_repos)
    log(f"Selected: {len(selected)} rules")

    # === ルール生成 & 追加 ===
    log("\n--- Generating entries ---")
    added = 0
    for c in selected:
        if added >= MAX_NEW_PER_RUN:
            break
        log(f"  {c.get('repo', '?')} ({c.get('stars', 0)}⭐)")
        entry = generate_rule_entry(c)
        if not entry:
            continue
        if entry["id"] in existing_ids:
            log(f"    Skip: {entry['id']} exists")
            continue

        if dry_run:
            log(f"    [DRY RUN] {entry['id']} — {entry['title']}")
        else:
            rules.append(entry)
            existing_ids.add(entry["id"])
            added += 1
            log(f"    ✅ {entry['id']} — {entry['title']}")

    log(f"\nResult: +{added} new, total {len(rules)}")

    if dry_run or added == 0:
        return

    RULES_JSON.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n")

    # === ビルド & デプロイ ===
    log("\n--- Build & Deploy ---")
    build_and_deploy()

    # ログ保存
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "candidates": len(all_candidates),
        "added": added,
        "total": len(rules),
        "new_ids": [r["id"] for r in rules[-added:]] if added > 0 else [],
    }
    log_file = LOG_DIR / f"collector_{datetime.now().strftime('%Y%m%d')}.json"
    log_file.write_text(json.dumps(log_entry, indent=2, ensure_ascii=False))
    log("✅ Done!")


if __name__ == "__main__":
    main()
