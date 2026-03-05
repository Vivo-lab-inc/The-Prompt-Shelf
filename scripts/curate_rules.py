#!/usr/bin/env python3
"""
Curate the best ~20 rules from collected data.
Adds proper source attribution (sourceUrl) and polishes metadata.
"""

import json
from pathlib import Path

RULES_JSON = Path(__file__).parent.parent / "src" / "data" / "rules.json"
AWESOME_BASE = "https://github.com/PatrickJS/awesome-cursorrules/tree/main/rules"

# Hand-picked best rules — diverse languages/frameworks, good content quality
SELECTED = {
    # --- Web Frontend ---
    "nextjs-typescript-app": {
        "title": "Next.js + TypeScript App",
        "title_ja": "Next.js + TypeScript アプリ",
        "description": "Comprehensive rules for Next.js App Router with TypeScript. Server Components first, Shadcn UI, Tailwind CSS.",
        "description_ja": "Next.js App Router + TypeScriptの包括的ルール。Server Components優先、Shadcn UI、Tailwind CSS。",
        "language": "TypeScript", "framework": "Next.js", "category": "web-frontend",
        "tags": ["react", "nextjs", "typescript", "tailwind", "app-router", "shadcn-ui"],
    },
    "sveltekit-typescript-guide": {
        "title": "SvelteKit + TypeScript",
        "title_ja": "SvelteKit + TypeScript",
        "description": "Expert rules for Svelte 5, SvelteKit, TypeScript with Supabase and Drizzle ORM integration.",
        "description_ja": "Svelte 5、SvelteKit、TypeScriptのエキスパートルール。Supabase・Drizzle ORM連携。",
        "language": "TypeScript", "framework": "Svelte", "category": "web-frontend",
        "tags": ["svelte", "sveltekit", "typescript", "supabase"],
    },
    "vue-3-nuxt-3-development": {
        "title": "Vue 3 + Nuxt 3",
        "title_ja": "Vue 3 + Nuxt 3",
        "description": "Vue 3 and Nuxt 3 development rules with Composition API, TypeScript, and modern best practices.",
        "description_ja": "Vue 3とNuxt 3の開発ルール。Composition API、TypeScript、モダンベストプラクティス。",
        "language": "TypeScript", "framework": "Vue", "category": "web-frontend",
        "tags": ["vue", "nuxt", "typescript", "javascript"],
    },
    "react-component-library": {
        "title": "React Component Library",
        "title_ja": "React コンポーネントライブラリ",
        "description": "Rules for building reusable React component libraries. Storybook, testing, and accessibility focused.",
        "description_ja": "再利用可能なReactコンポーネントライブラリ構築ルール。Storybook、テスト、アクセシビリティ重視。",
        "language": "TypeScript", "framework": "React", "category": "web-frontend",
        "tags": ["react", "component-library", "storybook", "accessibility", "testing"],
    },
    "astro-typescript": {
        "title": "Astro + TypeScript",
        "title_ja": "Astro + TypeScript",
        "description": "Astro framework development rules with TypeScript, Tailwind CSS, and content-first architecture.",
        "description_ja": "AstroフレームワークのTypeScript開発ルール。Tailwind CSS、コンテンツファーストアーキテクチャ。",
        "language": "TypeScript", "framework": "Astro", "category": "web-frontend",
        "tags": ["astro", "typescript", "tailwind", "seo"],
    },

    # --- Backend ---
    "python-fastapi-best-practicesmpt-f": {
        "title": "Python FastAPI Best Practices",
        "title_ja": "Python FastAPI ベストプラクティス",
        "description": "Production-grade FastAPI development. Async patterns, Pydantic v2, SQLAlchemy, structured error handling.",
        "description_ja": "本番グレードのFastAPI開発。非同期パターン、Pydantic v2、SQLAlchemy、構造化エラーハンドリング。",
        "language": "Python", "framework": "FastAPI", "category": "backend",
        "tags": ["python", "fastapi", "api", "pydantic", "async"],
    },
    "python-django-best-practicesmpt-fi": {
        "title": "Python Django Best Practices",
        "title_ja": "Python Django ベストプラクティス",
        "description": "Django development rules for scalable web applications. Class-based views, ORM best practices, security.",
        "description_ja": "スケーラブルなWebアプリのためのDjango開発ルール。クラスベースビュー、ORMベストプラクティス、セキュリティ。",
        "language": "Python", "framework": "Django", "category": "backend",
        "tags": ["python", "django", "api", "security"],
    },
    "java-springboot-jpa": {
        "title": "Java Spring Boot + JPA",
        "title_ja": "Java Spring Boot + JPA",
        "description": "Spring Boot with JPA/Hibernate. Entity design, repository patterns, transaction management, testing.",
        "description_ja": "Spring Boot + JPA/Hibernate。エンティティ設計、リポジトリパターン、トランザクション管理、テスト。",
        "language": "Java", "framework": "Spring", "category": "backend",
        "tags": ["java", "spring", "api", "testing"],
    },
    "typescript-nestjs-best-practicesmp": {
        "title": "NestJS Best Practices",
        "title_ja": "NestJS ベストプラクティス",
        "description": "Senior-level NestJS development. Modular architecture, decorators, guards, interceptors, microservices.",
        "description_ja": "シニアレベルのNestJS開発。モジュラーアーキテクチャ、デコレータ、ガード、インターセプタ、マイクロサービス。",
        "language": "TypeScript", "framework": "Express", "category": "backend",
        "tags": ["typescript", "nestjs", "api", "testing"],
    },
    "go-microservice": {
        "title": "Go Microservice",
        "title_ja": "Go マイクロサービス",
        "description": "Go microservice development rules. Clean architecture, gRPC, structured logging, context patterns.",
        "description_ja": "Goマイクロサービス開発ルール。クリーンアーキテクチャ、gRPC、構造化ロギング。",
        "language": "Go", "framework": "stdlib", "category": "backend",
        "tags": ["go", "microservice", "grpc", "clean-architecture", "docker"],
    },
    "laravel-php-83": {
        "title": "Laravel PHP 8.3",
        "title_ja": "Laravel PHP 8.3",
        "description": "Laravel package development with PHP 8.3. Modern PHP features, testing, strict typing.",
        "description_ja": "PHP 8.3でのLaravelパッケージ開発。モダンPHP機能、テスト、厳密な型付け。",
        "language": "PHP", "framework": "Laravel", "category": "backend",
        "tags": ["php", "laravel", "api", "testing"],
    },
    "elixir-engineer-guidelines": {
        "title": "Elixir + Phoenix",
        "title_ja": "Elixir + Phoenix",
        "description": "Elixir and Phoenix framework development. Docker integration, PostgreSQL, functional programming patterns.",
        "description_ja": "ElixirとPhoenixフレームワーク開発。Docker連携、PostgreSQL、関数型プログラミングパターン。",
        "language": "Elixir", "framework": "Any", "category": "backend",
        "tags": ["elixir", "docker", "postgresql", "api"],
    },

    # --- Mobile ---
    "flutter-app-expert": {
        "title": "Flutter App Expert",
        "title_ja": "Flutter アプリエキスパート",
        "description": "Flutter development rules. Widget patterns, state management, platform-specific code, performance.",
        "description_ja": "Flutter開発ルール。Widgetパターン、状態管理、プラットフォーム固有コード、パフォーマンス。",
        "language": "Dart", "framework": "Flutter", "category": "mobile",
        "tags": ["dart", "flutter", "mobile"],
    },
    "android-jetpack-compose": {
        "title": "Android Jetpack Compose",
        "title_ja": "Android Jetpack Compose",
        "description": "Android development with Jetpack Compose. Material Design 3, Kotlin patterns, lifecycle-aware components.",
        "description_ja": "Jetpack ComposeでのAndroid開発。Material Design 3、Kotlinパターン、ライフサイクル対応コンポーネント。",
        "language": "Kotlin", "framework": "Jetpack Compose", "category": "mobile",
        "tags": ["kotlin", "android", "mobile"],
    },
    "swiftui-guidelines": {
        "title": "SwiftUI Guidelines",
        "title_ja": "SwiftUI ガイドライン",
        "description": "SwiftUI development rules. Maintainable, clean, and readable Swift code with modern patterns.",
        "description_ja": "SwiftUI開発ルール。保守性の高い、クリーンで可読性のあるSwiftコード。",
        "language": "Swift", "framework": "Any", "category": "mobile",
        "tags": ["swift", "ios", "mobile"],
    },
    "react-native-expo": {
        "title": "React Native + Expo",
        "title_ja": "React Native + Expo",
        "description": "React Native with Expo framework. Cross-platform development, navigation, native modules.",
        "description_ja": "ExpoフレームワークでのReact Native開発。クロスプラットフォーム、ナビゲーション、ネイティブモジュール。",
        "language": "TypeScript", "framework": "React", "category": "mobile",
        "tags": ["react-native", "typescript", "mobile"],
    },

    # --- CLI ---
    "rust-cli-tool": {
        "title": "Rust CLI Tool",
        "title_ja": "Rust CLIツール",
        "description": "Rust CLI tool development. clap, error handling with thiserror/anyhow, cross-platform support.",
        "description_ja": "Rust CLIツール開発ルール。clap、thiserror/anyhowエラーハンドリング、クロスプラットフォーム対応。",
        "language": "Rust", "framework": "clap", "category": "cli",
        "tags": ["rust", "cli", "cross-platform", "error-handling"],
    },

    # --- DevOps ---
    "monorepo-turborepo": {
        "title": "Turborepo Monorepo",
        "title_ja": "Turborepo モノレポ",
        "description": "Turborepo monorepo management. Package dependencies, shared configs, CI/CD pipelines.",
        "description_ja": "Turborepoモノレポ管理ルール。パッケージ依存関係、共有設定、CI/CDパイプライン。",
        "language": "TypeScript", "framework": "Turborepo", "category": "devops",
        "tags": ["monorepo", "turborepo", "ci-cd", "typescript"],
    },

    # --- Other ---
    "chrome-extension-dev-js-typescript": {
        "title": "Chrome Extension Development",
        "title_ja": "Chrome拡張機能開発",
        "description": "Chrome Extension development with JavaScript/TypeScript. Manifest V3, service workers, content scripts.",
        "description_ja": "JavaScript/TypeScriptでのChrome拡張機能開発。Manifest V3、Service Worker、コンテンツスクリプト。",
        "language": "TypeScript", "framework": "Any", "category": "web-frontend",
        "tags": ["chrome-extension", "typescript", "javascript"],
    },
    "solidity-foundry": {
        "title": "Solidity + Foundry",
        "title_ja": "Solidity + Foundry",
        "description": "Solidity smart contract development. Security-first patterns, gas optimization, Foundry testing.",
        "description_ja": "Solidityスマートコントラクト開発。セキュリティファースト、ガス最適化、Foundryテスト。",
        "language": "Any", "framework": "Any", "category": "backend",
        "tags": ["solidity", "security", "testing"],
    },
    "cpp-programming-guidelines": {
        "title": "C++ Programming Guidelines",
        "title_ja": "C++ プログラミングガイドライン",
        "description": "Modern C++ development guidelines. Memory safety, RAII, STL usage, CMake build system.",
        "description_ja": "モダンC++開発ガイドライン。メモリ安全性、RAII、STL活用、CMakeビルドシステム。",
        "language": "C++", "framework": "Any", "category": "backend",
        "tags": ["cpp", "performance"],
    },
}


def main():
    all_rules = json.loads(RULES_JSON.read_text())
    rules_by_id = {r["id"]: r for r in all_rules}

    curated = []
    for rule_id, meta in SELECTED.items():
        rule = rules_by_id.get(rule_id)
        if not rule:
            print(f"WARNING: {rule_id} not found!")
            continue

        # Build source URL
        if rule.get("source", "").startswith("awesome-cursorrules"):
            # Find the directory name in awesome-cursorrules
            awesome_dir = rule_id
            # Map back to full dir name
            for suffix in ["-cursorrules-prompt-file", "-cursorrules-pro", "-cursorrules-prompt-fil", "-cursorrules"]:
                pass  # ID was already cleaned
            source_url = f"{AWESOME_BASE}/{awesome_dir}-cursorrules-prompt-file"
        elif rule.get("source", "").startswith("github:"):
            repo = rule["source"].replace("github:", "")
            source_url = f"https://github.com/{repo}"
        else:
            source_url = ""

        curated.append({
            "id": rule_id,
            "title": meta["title"],
            "title_ja": meta["title_ja"],
            "description": meta["description"],
            "description_ja": meta["description_ja"],
            "tool": rule["tool"],
            "format": rule["format"],
            "language": meta["language"],
            "framework": meta["framework"],
            "category": meta["category"],
            "tags": meta["tags"],
            "author": rule.get("author", "Community"),
            "source": rule.get("source", "awesome-cursorrules"),
            "sourceUrl": source_url,
            "stars": rule.get("stars", 0),
            "content": rule["content"],
        })
        print(f"+ {meta['title']} [{meta['language']}] [{meta['framework']}]")

    # Write
    RULES_JSON.write_text(json.dumps(curated, indent=2, ensure_ascii=False))
    print(f"\nWrote {len(curated)} curated rules to {RULES_JSON}")

    # Stats
    langs = set(r["language"] for r in curated)
    cats = set(r["category"] for r in curated)
    print(f"Languages: {sorted(langs)}")
    print(f"Categories: {sorted(cats)}")


if __name__ == "__main__":
    main()
