#!/usr/bin/env python3
"""Add more curated rules to existing rules.json."""

import json
from pathlib import Path

RULES_JSON = Path(__file__).parent.parent / "src" / "data" / "rules.json"
AWESOME_DIR = Path("/tmp/awesome-cursorrules/rules")
AWESOME_BASE = "https://github.com/PatrickJS/awesome-cursorrules/tree/main/rules"

# Additional rules to add (dir_name -> curated metadata)
ADDITIONS = {
    "convex-cursorrules-prompt-file": {
        "id": "convex-backend",
        "title": "Convex Backend",
        "title_ja": "Convex バックエンド",
        "description": "Convex real-time backend platform. Schema design, queries, mutations, file storage, and real-world patterns.",
        "description_ja": "Convexリアルタイムバックエンドプラットフォーム。スキーマ設計、クエリ、ミューテーション、ファイルストレージ。",
        "language": "TypeScript", "framework": "Convex", "category": "backend",
        "tags": ["typescript", "convex", "api", "react"],
    },
    "go-backend-scalability-cursorrules-prompt-file": {
        "id": "go-backend-scalability",
        "title": "Go Backend Scalability",
        "title_ja": "Go バックエンドスケーラビリティ",
        "description": "Comprehensive Go backend patterns. Database management, API design, caching, message queues, security.",
        "description_ja": "包括的なGoバックエンドパターン。データベース管理、API設計、キャッシュ、メッセージキュー、セキュリティ。",
        "language": "Go", "framework": "Any", "category": "backend",
        "tags": ["go", "api", "docker", "performance", "security"],
    },
    "python-llm-ml-workflow-cursorrules-prompt-file": {
        "id": "python-ml-workflow",
        "title": "Python ML & LLM Workflow",
        "title_ja": "Python ML・LLM ワークフロー",
        "description": "Machine learning and LLM development with Python. Best practices, design patterns, efficient data pipelines.",
        "description_ja": "PythonでのML・LLM開発。ベストプラクティス、デザインパターン、効率的なデータパイプライン。",
        "language": "Python", "framework": "Any", "category": "data",
        "tags": ["python", "machine-learning", "ai"],
    },
    "pandas-scikit-learn-guide-cursorrules-prompt-file": {
        "id": "pandas-scikit-learn",
        "title": "Pandas + Scikit-learn Data Analysis",
        "title_ja": "Pandas + Scikit-learn データ分析",
        "description": "Data analysis and visualization with pandas, matplotlib, seaborn. Jupyter Notebook best practices.",
        "description_ja": "pandas、matplotlib、seabornによるデータ分析・可視化。Jupyter Notebookベストプラクティス。",
        "language": "Python", "framework": "Any", "category": "data",
        "tags": ["python", "machine-learning", "ai"],
    },
    "kotlin-ktor-development-cursorrules-prompt-file": {
        "id": "kotlin-ktor",
        "title": "Kotlin Ktor Server",
        "title_ja": "Kotlin Ktor サーバー",
        "description": "Kotlin Ktor development following SOLID, DRY, KISS principles. OWASP security, coroutines, testing.",
        "description_ja": "SOLID・DRY・KISS原則に基づくKotlin Ktor開発。OWASPセキュリティ、コルーチン、テスト。",
        "language": "Kotlin", "framework": "Any", "category": "backend",
        "tags": ["kotlin", "api", "security", "testing"],
    },
    "react-graphql-apollo-client-cursorrules-prompt-file": {
        "id": "react-graphql-apollo",
        "title": "React + GraphQL (Apollo Client)",
        "title_ja": "React + GraphQL (Apollo Client)",
        "description": "React with GraphQL and Apollo Client. Functional components, hooks, type-safe queries, caching strategies.",
        "description_ja": "ReactとGraphQL・Apollo Client。関数コンポーネント、Hooks、型安全クエリ、キャッシュ戦略。",
        "language": "TypeScript", "framework": "React", "category": "web-frontend",
        "tags": ["react", "graphql", "typescript"],
    },
    "vscode-extension-dev-typescript-cursorrules-prompt-file": {
        "id": "vscode-extension-dev",
        "title": "VS Code Extension Development",
        "title_ja": "VS Code 拡張機能開発",
        "description": "VS Code extension development with TypeScript. VS Code APIs, Electron, modular design patterns.",
        "description_ja": "TypeScriptでのVS Code拡張機能開発。VS Code API、Electron、モジュラーデザインパターン。",
        "language": "TypeScript", "framework": "Any", "category": "web-frontend",
        "tags": ["typescript", "javascript"],
    },
    "drupal-11-cursorrules-prompt-file": {
        "id": "drupal-11",
        "title": "Drupal 11 + PHP 8.x",
        "title_ja": "Drupal 11 + PHP 8.x",
        "description": "Drupal 11 development with PHP 8.x and Symfony 6. Module/theme development, security, performance.",
        "description_ja": "PHP 8.x・Symfony 6でのDrupal 11開発。モジュール/テーマ開発、セキュリティ、パフォーマンス。",
        "language": "PHP", "framework": "Any", "category": "backend",
        "tags": ["php", "security", "performance"],
    },
    "aspnet-abp-cursorrules-prompt-file": {
        "id": "aspnet-abp-framework",
        "title": "ASP.NET Core + ABP Framework",
        "title_ja": "ASP.NET Core + ABP Framework",
        "description": "ASP.NET Core with ABP Framework and Entity Framework Core. Clean architecture, DDD patterns.",
        "description_ja": "ASP.NET CoreとABPフレームワーク、Entity Framework Core。クリーンアーキテクチャ、DDDパターン。",
        "language": "C#", "framework": "Any", "category": "backend",
        "tags": ["csharp", "api", "testing"],
    },
    "wordpress-php-guzzle-gutenberg-cursorrules-prompt-": {
        "id": "wordpress-gutenberg",
        "title": "WordPress + Gutenberg Blocks",
        "title_ja": "WordPress + Gutenberg ブロック",
        "description": "WordPress plugin development with Gutenberg blocks, Guzzle HTTP client, and WP REST API.",
        "description_ja": "Gutenbergブロック、Guzzle HTTPクライアント、WP REST APIを使ったWordPressプラグイン開発。",
        "language": "PHP", "framework": "WordPress", "category": "web-frontend",
        "tags": ["php", "wordpress", "javascript", "api"],
    },
    "tailwind-react-firebase-cursorrules-prompt-file": {
        "id": "react-tailwind-firebase",
        "title": "React + Tailwind + Firebase",
        "title_ja": "React + Tailwind + Firebase",
        "description": "Mobile-first web app with React, Tailwind CSS, and Firebase. Authentication, Firestore, responsive UI.",
        "description_ja": "React、Tailwind CSS、Firebaseでのモバイルファーストウェブアプリ。認証、Firestore、レスポンシブUI。",
        "language": "TypeScript", "framework": "React", "category": "web-frontend",
        "tags": ["react", "tailwind", "typescript"],
    },
    "nextjs-supabase-shadcn-pwa-cursorrules-prompt-file": {
        "id": "nextjs-supabase-shadcn-pwa",
        "title": "Next.js + Supabase + Shadcn PWA",
        "title_ja": "Next.js + Supabase + Shadcn PWA",
        "description": "Full-stack Next.js with Supabase backend, Shadcn UI components, and PWA support.",
        "description_ja": "Supabaseバックエンド、Shadcn UIコンポーネント、PWAサポート付きフルスタックNext.js。",
        "language": "TypeScript", "framework": "Next.js", "category": "web-frontend",
        "tags": ["nextjs", "react", "typescript", "supabase", "tailwind", "shadcn-ui"],
    },
    "typescript-llm-tech-stack-cursorrules-prompt-file": {
        "id": "typescript-llm-stack",
        "title": "TypeScript LLM Tech Stack",
        "title_ja": "TypeScript LLM テックスタック",
        "description": "Multi-provider LLM architecture with TypeScript. Prompt engineering, API integration, token management.",
        "description_ja": "TypeScriptによるマルチプロバイダーLLMアーキテクチャ。プロンプトエンジニアリング、API連携、トークン管理。",
        "language": "TypeScript", "framework": "Any", "category": "backend",
        "tags": ["typescript", "ai", "api"],
    },
    "htmx-basic-cursorrules-prompt-file": {
        "id": "htmx-basic",
        "title": "HTMX Basics",
        "title_ja": "HTMX ベーシック",
        "description": "HTMX development best practices. Hypermedia-driven approach, minimal JavaScript, server-side rendering.",
        "description_ja": "HTMX開発ベストプラクティス。ハイパーメディア駆動アプローチ、最小限のJS、サーバーサイドレンダリング。",
        "language": "JavaScript", "framework": "Any", "category": "web-frontend",
        "tags": ["javascript", "api"],
    },
    "svelte-5-vs-svelte-4-cursorrules-prompt-file": {
        "id": "svelte-5-migration",
        "title": "Svelte 5 Migration Guide",
        "title_ja": "Svelte 5 移行ガイド",
        "description": "Svelte 5 changes from Svelte 4. Runes, snippets, event handling, component lifecycle updates.",
        "description_ja": "Svelte 4からSvelte 5への変更点。Runes、スニペット、イベントハンドリング、コンポーネントライフサイクル。",
        "language": "TypeScript", "framework": "Svelte", "category": "web-frontend",
        "tags": ["svelte", "typescript", "javascript"],
    },
    "unity-cursor-ai-c-cursorrules-prompt-file": {
        "id": "unity-csharp-game",
        "title": "Unity Game Development (C#)",
        "title_ja": "Unity ゲーム開発 (C#)",
        "description": "Unity game development with C#. Game mechanics, physics, input handling, tower defense patterns.",
        "description_ja": "C#でのUnityゲーム開発。ゲームメカニクス、物理演算、入力処理、タワーディフェンスパターン。",
        "language": "C#", "framework": "Any", "category": "game",
        "tags": ["csharp", "game"],
    },
    "netlify-official-cursorrules-prompt-file": {
        "id": "netlify-official",
        "title": "Netlify Official",
        "title_ja": "Netlify 公式",
        "description": "Official Netlify development rules. Serverless functions, edge functions, storage, and deployment best practices.",
        "description_ja": "Netlify公式開発ルール。サーバーレス関数、エッジ関数、ストレージ、デプロイベストプラクティス。",
        "language": "TypeScript", "framework": "Any", "category": "devops",
        "tags": ["typescript", "javascript", "react"],
    },
    "flutter-riverpod-cursorrules-prompt-file": {
        "id": "flutter-riverpod",
        "title": "Flutter + Riverpod",
        "title_ja": "Flutter + Riverpod",
        "description": "Flutter development with Riverpod state management. Advanced problem-solving, clean architecture.",
        "description_ja": "Riverpod状態管理を使ったFlutter開発。高度な問題解決、クリーンアーキテクチャ。",
        "language": "Dart", "framework": "Flutter", "category": "mobile",
        "tags": ["dart", "flutter", "mobile"],
    },
}


def main():
    rules = json.loads(RULES_JSON.read_text())
    existing_ids = {r["id"] for r in rules}
    added = 0

    for dir_name, meta in ADDITIONS.items():
        if meta["id"] in existing_ids:
            print(f"  Skip (exists): {meta['id']}")
            continue

        # Read content
        content = None
        rule_dir = AWESOME_DIR / dir_name
        for fname in [".cursorrules", "cursorrules", ".cursorules"]:
            f = rule_dir / fname
            if f.exists():
                content = f.read_text(errors="replace")
                break

        if not content:
            print(f"  Skip (no file): {dir_name}")
            continue

        if len(content) > 15000:
            content = content[:15000] + "\n\n... (truncated)"

        source_url = f"{AWESOME_BASE}/{dir_name}"

        rules.append({
            "id": meta["id"],
            "title": meta["title"],
            "title_ja": meta["title_ja"],
            "description": meta["description"],
            "description_ja": meta["description_ja"],
            "tool": "cursor",
            "format": ".cursorrules",
            "language": meta["language"],
            "framework": meta["framework"],
            "category": meta["category"],
            "tags": meta["tags"],
            "author": "awesome-cursorrules",
            "source": "awesome-cursorrules",
            "sourceUrl": source_url,
            "stars": 0,
            "content": content,
        })
        added += 1
        print(f"  + {meta['title']} [{meta['language']}]")

    RULES_JSON.write_text(json.dumps(rules, indent=2, ensure_ascii=False))
    print(f"\nAdded {added} rules (total: {len(rules)})")

    # Summary
    langs = sorted(set(r["language"] for r in rules))
    cats = sorted(set(r["category"] for r in rules))
    print(f"Languages: {langs}")
    print(f"Categories: {cats}")


if __name__ == "__main__":
    main()
