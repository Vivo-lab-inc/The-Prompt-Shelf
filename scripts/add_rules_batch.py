#!/usr/bin/env python3
"""Add batch of curated rules to rules.json."""
import json
from pathlib import Path

RULES_JSON = Path(__file__).parent.parent / "src" / "data" / "rules.json"

new_rules = [
    # === AGENTS.md (6) ===
    {
        "id": "agents-md-openai-codex",
        "title": "OpenAI Codex — Rust Development",
        "title_ja": "OpenAI Codex — Rust開発ガイドライン",
        "description": "AGENTS.md for OpenAI's Codex CLI. Covers Rust crate conventions, Clippy rules, cargo-insta snapshot tests, ratatui TUI styling, and app-server API design patterns.",
        "description_ja": "OpenAI Codex CLIのAGENTS.md。Rustクレート規約、Clippyルール、cargo-instaスナップショットテスト、ratatui TUIスタイリング、API設計パターンを網羅。",
        "tool": "agents-md",
        "format": "AGENTS.md",
        "language": "Rust",
        "framework": "Codex CLI",
        "category": "cli",
        "tags": ["rust", "codex", "openai", "tui", "ratatui", "snapshot-tests", "api-design"],
        "author": "openai",
        "source": "openai/codex",
        "sourceUrl": "https://github.com/openai/codex/blob/main/AGENTS.md",
        "stars": 63300,
        "content": open("/dev/null").read() if False else ""  # placeholder
    },
    {
        "id": "agents-md-prisma-orm",
        "title": "Prisma ORM — Agent Field Notes",
        "title_ja": "Prisma ORM — エージェント開発ナレッジベース",
        "description": "Living knowledge base for the Prisma monorepo. Covers pnpm+Turborepo layout, driver adapters, Wasm query compiler, Jest/Vitest testing, error handling chain, and coding conventions.",
        "description_ja": "Prismaモノレポの生きたナレッジベース。pnpm+Turborepoレイアウト、ドライバアダプタ、Wasmクエリコンパイラ、テスト、エラー処理チェーンを網羅。",
        "tool": "agents-md",
        "format": "AGENTS.md",
        "language": "TypeScript",
        "framework": "Prisma",
        "category": "backend",
        "tags": ["prisma", "orm", "typescript", "monorepo", "turborepo", "wasm", "testing"],
        "author": "prisma",
        "source": "prisma/prisma",
        "sourceUrl": "https://github.com/prisma/prisma/blob/main/AGENTS.md",
        "stars": 45300,
        "content": ""
    },
    {
        "id": "agents-md-bun-runtime",
        "title": "Bun Runtime — Zig/C++/TypeScript",
        "title_ja": "Bunランタイム — Zig/C++/TypeScript開発",
        "description": "AGENTS.md for the Bun JavaScript runtime. Covers Zig core, C++ JSC bindings, TypeScript built-in modules, test patterns with fixtures, code generation pipeline, and CI debugging.",
        "description_ja": "Bunランタイムの AGENTS.md。Zigコア、C++ JSCバインディング、TypeScript組み込みモジュール、テストパターン、コード生成パイプラインを網羅。",
        "tool": "agents-md",
        "format": "AGENTS.md",
        "language": "Zig",
        "framework": "Bun",
        "category": "backend",
        "tags": ["bun", "zig", "cpp", "typescript", "runtime", "jsc", "testing"],
        "author": "oven-sh",
        "source": "oven-sh/bun",
        "sourceUrl": "https://github.com/oven-sh/bun/blob/main/AGENTS.md",
        "stars": 82000,
        "content": ""
    },
    {
        "id": "agents-md-calcom",
        "title": "Cal.com — Do/Don't Format",
        "title_ja": "Cal.com — Do/Don'tフォーマット",
        "description": "Clean Do/Don't style AGENTS.md for Cal.com. Covers Prisma best practices, strict TypeScript rules, error handling patterns, PR size guidelines, and permission boundaries.",
        "description_ja": "Cal.comのクリーンなDo/Don'tスタイルAGENTS.md。Prismaベストプラクティス、TypeScript厳密ルール、エラー処理、PR規模ガイドラインを網羅。",
        "tool": "agents-md",
        "format": "AGENTS.md",
        "language": "TypeScript",
        "framework": "Next.js",
        "category": "web-frontend",
        "tags": ["calcom", "prisma", "typescript", "nextjs", "do-dont", "pr-guidelines"],
        "author": "calcom",
        "source": "calcom/cal.com",
        "sourceUrl": "https://github.com/calcom/cal.com/blob/main/AGENTS.md",
        "stars": 40200,
        "content": ""
    },
    {
        "id": "agents-md-cloudflare-workers",
        "title": "Cloudflare Workers SDK — Hierarchical",
        "title_ja": "Cloudflare Workers SDK — 階層型AGENTS.md",
        "description": "Hierarchical AGENTS.md for Wrangler/Miniflare monorepo. Features WHERE TO LOOK routing table, strict TypeScript rules, security ESLint rules, changeset workflow, and sub-directory AGENTS.md references.",
        "description_ja": "Wrangler/Miniflareモノレポの階層型AGENTS.md。WHERE TO LOOKルーティングテーブル、TypeScript厳密ルール、セキュリティESLint、changesetワークフローを網羅。",
        "tool": "agents-md",
        "format": "AGENTS.md",
        "language": "TypeScript",
        "framework": "Cloudflare Workers",
        "category": "backend",
        "tags": ["cloudflare", "workers", "wrangler", "miniflare", "monorepo", "security"],
        "author": "cloudflare",
        "source": "cloudflare/workers-sdk",
        "sourceUrl": "https://github.com/cloudflare/workers-sdk/blob/main/AGENTS.md",
        "stars": 6500,
        "content": ""
    },
    {
        "id": "agents-md-sveltekit",
        "title": "SvelteKit — Concise & Practical",
        "title_ja": "SvelteKit — 簡潔実用型AGENTS.md",
        "description": "Concise AGENTS.md with timeout hints for each command, Playwright test integration, pre-submission checklist, JSDoc code style, and troubleshooting section.",
        "description_ja": "各コマンドのタイムアウトヒント付き簡潔なAGENTS.md。Playwrightテスト統合、提出前チェックリスト、JSDocコードスタイル、トラブルシューティング。",
        "tool": "agents-md",
        "format": "AGENTS.md",
        "language": "TypeScript",
        "framework": "SvelteKit",
        "category": "web-frontend",
        "tags": ["svelte", "sveltekit", "playwright", "testing", "jsdoc"],
        "author": "sveltejs",
        "source": "sveltejs/kit",
        "sourceUrl": "https://github.com/sveltejs/kit/blob/main/AGENTS.md",
        "stars": 20300,
        "content": ""
    },

    # === CLAUDE.md (5) ===
    {
        "id": "claude-md-excalidraw",
        "title": "Excalidraw — Monorepo Guide",
        "title_ja": "Excalidraw — モノレポガイド",
        "description": "Concise CLAUDE.md for the 118K-star virtual whiteboard. Covers React component library structure, Yarn workspaces, esbuild/Vite build system, and TypeScript testing workflow.",
        "description_ja": "118Kスターの仮想ホワイトボードの簡潔なCLAUDE.md。Reactコンポーネントライブラリ構造、Yarnワークスペース、esbuild/Viteビルドシステムを網羅。",
        "tool": "claude-code",
        "format": "CLAUDE.md",
        "language": "TypeScript",
        "framework": "React",
        "category": "web-frontend",
        "tags": ["excalidraw", "react", "monorepo", "yarn", "esbuild", "vite", "whiteboard"],
        "author": "excalidraw",
        "source": "excalidraw/excalidraw",
        "sourceUrl": "https://github.com/excalidraw/excalidraw/blob/master/CLAUDE.md",
        "stars": 118000,
        "content": ""
    },
    {
        "id": "claude-md-overreacted-dan-abramov",
        "title": "Dan Abramov's Blog — overreacted.io",
        "title_ja": "Dan Abramovのブログ — overreacted.io",
        "description": "CLAUDE.md by React core team member Dan Abramov. Covers Next.js 15 static blog, MDX processing pipeline, Shiki syntax highlighting, and famously candid commit message guidelines.",
        "description_ja": "Reactコアチームメンバー Dan AbramovのCLAUDE.md。Next.js 15静的ブログ、MDX処理パイプライン、Shikiシンタックスハイライト、率直なコミットメッセージガイドライン。",
        "tool": "claude-code",
        "format": "CLAUDE.md",
        "language": "TypeScript",
        "framework": "Next.js",
        "category": "web-frontend",
        "tags": ["dan-abramov", "react", "nextjs", "blog", "mdx", "static-site"],
        "author": "gaearon",
        "source": "gaearon/overreacted.io",
        "sourceUrl": "https://github.com/gaearon/overreacted.io/blob/main/CLAUDE.md",
        "stars": 7300,
        "content": ""
    },
    {
        "id": "claude-md-mcp-typescript-sdk",
        "title": "MCP TypeScript SDK — Protocol Architecture",
        "title_ja": "MCP TypeScript SDK — プロトコルアーキテクチャ",
        "description": "One of the most comprehensive CLAUDE.md files. Documents three-layer SDK architecture (Types/Protocol/High-Level APIs), transport system, bidirectional message flow, and handler registration patterns.",
        "description_ja": "最も包括的なCLAUDE.mdの一つ。3層SDKアーキテクチャ、トランスポートシステム、双方向メッセージフロー、ハンドラ登録パターンを文書化。",
        "tool": "claude-code",
        "format": "CLAUDE.md",
        "language": "TypeScript",
        "framework": "MCP SDK",
        "category": "backend",
        "tags": ["mcp", "model-context-protocol", "anthropic", "sdk", "json-rpc", "protocol"],
        "author": "modelcontextprotocol",
        "source": "modelcontextprotocol/typescript-sdk",
        "sourceUrl": "https://github.com/modelcontextprotocol/typescript-sdk/blob/main/CLAUDE.md",
        "stars": 11400,
        "content": ""
    },
    {
        "id": "claude-md-claude-code-action",
        "title": "Claude Code Action — GitHub Action",
        "title_ja": "Claude Code Action — GitHubアクション",
        "description": "Anthropic's official CLAUDE.md for the Claude Code GitHub Action. Features 'Things That Will Bite You' gotchas section, mode detection architecture, auth priority, and prompt construction pipeline.",
        "description_ja": "AnthropicのClaude Code GitHubアクション公式CLAUDE.md。「噛まれる罠」セクション、モード検出アーキテクチャ、認証優先順位、プロンプト構築パイプラインを特集。",
        "tool": "claude-code",
        "format": "CLAUDE.md",
        "language": "TypeScript",
        "framework": "GitHub Actions",
        "category": "devops",
        "tags": ["anthropic", "claude-code", "github-action", "bun", "gotchas"],
        "author": "anthropics",
        "source": "anthropics/claude-code-action",
        "sourceUrl": "https://github.com/anthropics/claude-code-action/blob/main/CLAUDE.md",
        "stars": 6000,
        "content": ""
    },
    {
        "id": "claude-md-pytorch-image-models",
        "title": "PyTorch Image Models (timm)",
        "title_ja": "PyTorch Image Models (timm)",
        "description": "CLAUDE.md for HuggingFace's 36K-star ML library. Specifies Python code style with 'sadface' indentation, Google-style docstrings, PEP484 type annotations, and parallel pytest commands.",
        "description_ja": "HuggingFaceの36Kスター機械学習ライブラリのCLAUDE.md。'sadface'インデント、Google式docstring、PEP484型アノテーション、並列pytestを規定。",
        "tool": "claude-code",
        "format": "CLAUDE.md",
        "language": "Python",
        "framework": "PyTorch",
        "category": "backend",
        "tags": ["pytorch", "huggingface", "ml", "timm", "image-models", "python"],
        "author": "huggingface",
        "source": "huggingface/pytorch-image-models",
        "sourceUrl": "https://github.com/huggingface/pytorch-image-models/blob/main/CLAUDE.md",
        "stars": 36400,
        "content": ""
    },

    # === .cursorrules (7) ===
    {
        "id": "rails-ruby-hotwire",
        "title": "Ruby on Rails + Hotwire + Tailwind",
        "title_ja": "Ruby on Rails + Hotwire + Tailwind",
        "description": "Comprehensive Rails rules covering Ruby 3.x syntax, ActiveRecord patterns, Hotwire (Turbo/Stimulus), RESTful conventions, RSpec testing, and Sidekiq background jobs.",
        "description_ja": "Ruby 3.x構文、ActiveRecordパターン、Hotwire（Turbo/Stimulus）、RESTful規約、RSpecテスト、Sidekiqバックグラウンドジョブを網羅するRailsルール。",
        "tool": "cursor",
        "format": ".cursorrules",
        "language": "Ruby",
        "framework": "Rails",
        "category": "backend",
        "tags": ["ruby", "rails", "hotwire", "turbo", "stimulus", "tailwind", "rspec"],
        "author": "tvararu",
        "source": "cursor.directory",
        "sourceUrl": "https://cursor.directory/rails-ruby-cursor-rules",
        "stars": 890,
        "content": """You are an expert in Ruby on Rails, PostgreSQL, Hotwire (Turbo and Stimulus), and Tailwind CSS.

Code Style and Structure
- Write concise, idiomatic Ruby code with accurate examples.
- Follow Rails conventions and best practices.
- Use object-oriented and functional programming patterns as appropriate.
- Prefer iteration and modularization over code duplication.
- Use descriptive variable and method names (e.g., user_signed_in?, calculate_total).
- Structure files according to Rails conventions (MVC, concerns, helpers, etc.).

Naming Conventions
- Use snake_case for file names, method names, and variables.
- Use CamelCase for class and module names.
- Follow Rails naming conventions for models, controllers, and views.

Ruby and Rails Usage
- Use Ruby 3.x features when appropriate (e.g., pattern matching, endless methods).
- Leverage Rails' built-in helpers and methods.
- Use ActiveRecord effectively for database operations.

Syntax and Formatting
- Follow the Ruby Style Guide (https://rubystyle.guide/)
- Use Ruby's expressive syntax (e.g., unless, ||=, &.)
- Prefer single quotes for strings unless interpolation is needed.

Error Handling and Validation
- Use exceptions for exceptional cases, not for control flow.
- Implement proper error logging and user-friendly messages.
- Use ActiveModel validations in models.
- Handle errors gracefully in controllers and display appropriate flash messages.

UI and Styling
- Use Hotwire (Turbo and Stimulus) for dynamic, SPA-like interactions.
- Implement responsive design with Tailwind CSS.
- Use Rails view helpers and partials to keep views DRY.

Performance Optimization
- Use database indexing effectively.
- Implement caching strategies (fragment caching, Russian Doll caching).
- Use eager loading to avoid N+1 queries.
- Optimize database queries using includes, joins, or select.

Key Conventions
- Follow RESTful routing conventions.
- Use concerns for shared behavior across models or controllers.
- Implement service objects for complex business logic.
- Use background jobs (e.g., Sidekiq) for time-consuming tasks.

Testing
- Write comprehensive tests using RSpec or Minitest.
- Follow TDD/BDD practices.
- Use factories (FactoryBot) for test data generation.

Security
- Implement proper authentication and authorization (e.g., Devise, Pundit).
- Use strong parameters in controllers.
- Protect against common web vulnerabilities (XSS, CSRF, SQL injection).

Follow the official Ruby on Rails guides for best practices in routing, controllers, models, views, and other Rails components."""
    },
    {
        "id": "angular-typescript-signals",
        "title": "Angular 18+ with Signals & Standalone",
        "title_ja": "Angular 18+ Signals & Standalone",
        "description": "Modern Angular rules with Signals for reactive state management, standalone components, inject() function for DI, NgOptimizedImage, deferrable views, and strict TypeScript conventions.",
        "description_ja": "Signalsによるリアクティブ状態管理、スタンドアロンコンポーネント、inject()関数、NgOptimizedImage、deferrable viewsを含むモダンAngularルール。",
        "tool": "cursor",
        "format": ".cursorrules",
        "language": "TypeScript",
        "framework": "Angular",
        "category": "web-frontend",
        "tags": ["angular", "typescript", "signals", "standalone", "sass", "rxjs"],
        "author": "Ralph Olazo",
        "source": "cursor.directory",
        "sourceUrl": "https://cursor.directory/angular",
        "stars": 760,
        "content": """You are an Angular, SASS, and TypeScript expert focused on creating scalable and high-performance web applications.

Key Development Principles
1. Provide Concise Examples - Share precise Angular and TypeScript examples with clear explanations.
2. Immutability & Pure Functions - Apply immutability principles and pure functions wherever possible.
3. Component Composition - Favor component composition over inheritance to enhance modularity.
4. Meaningful Naming - Use descriptive variable names like isUserLoggedIn, userPermissions, fetchData().
5. File Naming - Enforce kebab-case naming for files (e.g., user-profile.component.ts).

Angular and TypeScript Best Practices
- Define data models using interfaces for explicit types and maintain strict typing to avoid any.
- Use standalone components as appropriate, promoting code reusability without relying on Angular modules.
- Utilize Angular's signals system for efficient and reactive programming.
- Use the inject function to inject services directly within component logic.

Coding Standards
- Use single quotes for string literals.
- Use 2-space indentation.
- Prefer const for constants and immutable variables.
- Utilize template literals for string interpolation.

Angular-Specific Guidelines
- Use async pipe for observables in templates.
- Enable lazy loading for feature modules.
- Ensure accessibility with semantic HTML and ARIA attributes.
- Use Angular's signals system for efficient reactive state management.
- For images, use NgOptimizedImage.
- Implement deferrable views to delay rendering of non-essential components.

Import Order
1. Angular core and common modules
2. RxJS modules
3. Angular-specific modules
4. Core application imports
5. Shared module imports
6. Environment-specific imports
7. Relative path imports

Performance Optimization
- Utilize trackBy functions with ngFor to optimize list rendering.
- Apply pure pipes for computationally heavy operations.
- Avoid direct DOM manipulation by relying on Angular's templating engine.
- Leverage Angular's signals system to reduce unnecessary re-renders.

Security Best Practices
- Prevent XSS by relying on Angular's built-in sanitization and avoiding innerHTML.
- Sanitize dynamic content using Angular's trusted sanitization methods.

Reference: Refer to Angular's official documentation for components, services, and modules."""
    },
    {
        "id": "terraform-iac-cloud",
        "title": "Terraform + Cloud Infrastructure as Code",
        "title_ja": "Terraform + クラウドIaC",
        "description": "Expert Terraform rules for AWS/Azure/GCP. Covers remote backends, state locking, workspace separation, reusable modules with semantic versioning, terratest CI/CD, and security practices.",
        "description_ja": "AWS/Azure/GCP向けTerraformルール。リモートバックエンド、状態ロック、ワークスペース分離、再利用可能モジュール、terratest CI/CD、セキュリティプラクティス。",
        "tool": "cursor",
        "format": ".cursorrules",
        "language": "HCL",
        "framework": "Terraform",
        "category": "devops",
        "tags": ["terraform", "iac", "aws", "azure", "gcp", "infrastructure", "devops"],
        "author": "Abdeldjalil Sichaib",
        "source": "cursor.directory",
        "sourceUrl": "https://cursor.directory/terraform-cloud-infrastructure-as-code-best-practices",
        "stars": 650,
        "content": """You are an expert in Terraform and Infrastructure as Code (IaC) for cloud platforms such as AWS, Azure, and GCP.

Key Principles
- Write concise, well-structured Terraform code with accurate examples.
- Organize infrastructure resources into reusable modules.
- Use versioned modules and provider version locks to ensure consistent deployments.
- Avoid hardcoded values; always use variables for flexibility.
- Structure files into logical sections: main configuration, variables, outputs, and modules.

Terraform Best Practices
- Use remote backends (e.g., S3, Azure Blob, GCS) for state management.
- Enable state locking and use encryption for security.
- Utilize workspaces for environment separation (e.g., dev, staging, prod).
- Organize resources by service or application domain.
- Always run terraform fmt to maintain consistent code formatting.
- Use terraform validate and linting tools such as tflint or terrascan.
- Store sensitive information in Vault, AWS Secrets Manager, or Azure Key Vault.

Error Handling and Validation
- Use validation rules for variables to prevent incorrect input values.
- Handle edge cases using conditional expressions and null checks.
- Use depends_on to manage explicit dependencies when needed.

Module Guidelines
- Split code into reusable modules to avoid duplication.
- Use outputs from modules to pass information between configurations.
- Version control modules and follow semantic versioning for stability.
- Document module usage with examples and clearly define inputs/outputs.

Security Practices
- Avoid hardcoding sensitive values; use Vault or environment variables.
- Ensure encryption for storage and communication.
- Define access controls and security groups for each cloud resource.
- Follow cloud provider-specific security guidelines.

Performance Optimization
- Use resource targeting (-target) to speed up resource-specific changes.
- Cache Terraform provider plugins locally.
- Limit the use of count or for_each when not necessary.

Testing and CI/CD Integration
- Integrate Terraform with CI/CD pipelines (GitHub Actions, GitLab CI).
- Run terraform plan in CI pipelines to catch issues before applying.
- Use tools like terratest to write unit tests for Terraform modules.
- Set up automated tests for critical infrastructure paths.

Key Conventions
1. Always lock provider versions to avoid breaking changes.
2. Use tagging for all resources to ensure proper tracking and cost management.
3. Ensure resources are defined in a modular, reusable way for easier scaling.
4. Document code and configurations with README.md files."""
    },
    {
        "id": "playwright-e2e-testing",
        "title": "Playwright E2E Testing",
        "title_ja": "Playwright E2Eテスト",
        "description": "Senior QA automation rules for Playwright. Enforces role-based locators over CSS selectors, web-first assertions, fixture-based test isolation, cross-browser projects, and no hardcoded timeouts.",
        "description_ja": "PlaywrightのシニアQA自動化ルール。ロールベースロケーター、Web-firstアサーション、フィクスチャベーステスト分離、クロスブラウザプロジェクト、ハードコードタイムアウト禁止。",
        "tool": "cursor",
        "format": ".cursorrules",
        "language": "TypeScript",
        "framework": "Playwright",
        "category": "web-frontend",
        "tags": ["playwright", "testing", "e2e", "automation", "typescript", "qa"],
        "author": "Douglas Urrea Ocampo",
        "source": "cursor.directory",
        "sourceUrl": "https://cursor.directory/playwright-cursor-rules",
        "stars": 580,
        "content": """You are a Senior QA Automation Engineer expert in TypeScript, JavaScript, Frontend development, Backend development, and Playwright end-to-end testing.

- Use descriptive and meaningful test names that clearly describe the expected behavior.
- Utilize Playwright fixtures (e.g., test, page, expect) to maintain test isolation and consistency.
- Use test.beforeEach and test.afterEach for setup and teardown to ensure a clean state for each test.
- Keep tests DRY by extracting reusable logic into helper functions.
- Avoid using page.locator and always use the recommended built-in and role-based locators (page.getByRole, page.getByLabel, page.getByText, page.getByTitle, etc.) over complex selectors.
- Use page.getByTestId whenever data-testid is defined on an element or container.
- Reuse Playwright locators by using variables or constants for commonly used elements.
- Use the playwright.config.ts file for global configuration and environment setup.
- Implement proper error handling and logging in tests to provide clear failure messages.
- Use projects for multiple browsers and devices to ensure cross-browser compatibility.
- Use built-in config objects like devices whenever possible.
- Prefer to use web-first assertions (toBeVisible, toHaveText, etc.) whenever possible.
- Use expect matchers for assertions (toEqual, toContain, toBeTruthy, toHaveLength, etc.).
- Avoid hardcoded timeouts.
- Use page.waitFor with specific conditions or events to wait for elements or states.
- Ensure tests run reliably in parallel without shared state conflicts.
- Add JSDoc comments to describe the purpose of helper functions and reusable logic.
- Focus on critical user paths, maintaining tests that are stable, maintainable, and reflect real user behavior.
- Follow the guidance and best practices described on https://playwright.dev/docs/writing-tests."""
    },
    {
        "id": "remix-supabase-fullstack",
        "title": "Remix + Supabase Full-Stack",
        "title_ja": "Remix + Supabase フルスタック",
        "description": "Full-stack Remix rules with Supabase integration. Covers loaders/actions for SSR, useFetcher patterns, route-based error boundaries, Link prefetching, and CSRF protection.",
        "description_ja": "Supabase統合のフルスタックRemixルール。SSR用ローダー/アクション、useFetcherパターン、ルートベースエラーバウンダリ、Linkプリフェッチ、CSRF保護。",
        "tool": "cursor",
        "format": ".cursorrules",
        "language": "TypeScript",
        "framework": "Remix",
        "category": "web-frontend",
        "tags": ["remix", "supabase", "typescript", "tailwind", "ssr", "loaders", "actions"],
        "author": "Mohammed Farmaan",
        "source": "cursor.directory",
        "sourceUrl": "https://cursor.directory/remix",
        "stars": 540,
        "content": """You are an expert in Remix, Supabase, TailwindCSS, and TypeScript, focusing on scalable web development.

Key Principles
- Provide clear, precise Remix and TypeScript examples.
- Apply immutability and pure functions where applicable.
- Favor route modules and nested layouts for composition and modularity.
- Use meaningful variable names (e.g., isAuthenticated, userRole).
- Always use kebab-case for file names (e.g., user-profile.tsx).
- Prefer named exports for loaders, actions, and components.

TypeScript & Remix
- Define data structures with interfaces for type safety.
- Avoid the any type, fully utilize TypeScript's type system.
- Use nested layouts and dynamic routes where applicable.
- Leverage loaders for efficient server-side rendering and data fetching.
- Use useFetcher and useLoaderData for seamless data management.

Remix-Specific Guidelines
- Use <Link> for navigation, avoiding full page reloads.
- Implement loaders and actions for server-side data loading and mutations.
- Ensure accessibility with semantic HTML and ARIA labels.
- Leverage route-based loading, error boundaries, and catch boundaries.
- Use the useFetcher hook for non-blocking data updates.
- Cache and optimize resource loading where applicable.

Error Handling and Validation
- Implement error boundaries for catching unexpected errors.
- Use custom error handling within loaders and actions.
- Validate user input on both client and server using formData or JSON.

Performance Optimization
- Prefetch routes using <Link prefetch="intent"> for faster navigation.
- Defer non-essential JavaScript using <Scripts defer />.
- Optimize nested layouts to minimize re-rendering.
- Use Remix's built-in caching and data revalidation.

Security
- Prevent XSS by sanitizing user-generated content.
- Use Remix's CSRF protection for form submissions.
- Handle sensitive data on the server, never expose in client code.

Reference: Refer to Remix's official documentation for Routes, Loaders, and Actions."""
    },
    {
        "id": "prisma-orm-typescript",
        "title": "Prisma ORM + TypeScript",
        "title_ja": "Prisma ORM + TypeScript",
        "description": "Comprehensive Prisma ORM rules covering schema design, type-safe client operations, transactions, middleware patterns, migration workflow, error handling, and repository patterns.",
        "description_ja": "スキーマ設計、型安全なクライアント操作、トランザクション、ミドルウェアパターン、マイグレーション、エラー処理、リポジトリパターンを網羅するPrisma ORMルール。",
        "tool": "cursor",
        "format": ".cursorrules",
        "language": "TypeScript",
        "framework": "Prisma",
        "category": "backend",
        "tags": ["prisma", "orm", "typescript", "database", "migrations", "testing"],
        "author": "gniting",
        "source": "cursor.directory",
        "sourceUrl": "https://cursor.directory/prisma-orm-cursor-rules",
        "stars": 470,
        "content": """Prisma ORM Development Guidelines — You are a senior TypeScript programmer with expertise in Prisma ORM, clean code principles, and modern backend development.

TypeScript General Guidelines
- Always declare explicit types for variables and functions. Avoid using any.
- Use PascalCase for classes/interfaces, camelCase for variables/functions, kebab-case for files.
- Use UPPERCASE for environment variables and constants.
- Write concise, single-purpose functions. Aim for less than 20 lines.
- Use early returns. Extract complex logic to utility functions.
- Prefer map, filter, reduce. Use arrow functions for simple operations.
- Encapsulate data in composite types. Prefer immutability with readonly and as const.

Prisma-Specific Guidelines

Schema Design
- Use meaningful, domain-driven model names.
- Use @id for primary keys, @unique for natural identifiers, @relation for explicit relationships.
- Keep schemas normalized and DRY.
- Implement soft delete with deletedAt timestamp.

Client Usage
- Always use type-safe Prisma client operations.
- Prefer transactions for complex, multi-step operations.
- Use Prisma middleware for cross-cutting concerns (logging, soft delete, auditing).
- Handle optional relations explicitly.

Database Migrations
- Create migrations for schema changes with descriptive names.
- Review migrations before applying. Never modify existing migrations.

Error Handling
- Catch PrismaClientKnownRequestError, PrismaClientUnknownRequestError, PrismaClientValidationError.
- Provide user-friendly error messages. Log detailed info for debugging.

Testing
- Use in-memory database for unit tests. Mock Prisma client for isolated testing.
- Test successful operations, error cases, and edge conditions.
- Use factory methods for test data generation.

Performance
- Use select and include judiciously. Avoid N+1 query problems.
- Use findMany with take and skip for pagination.
- Profile and optimize database queries.

Security
- Never expose raw Prisma client in APIs.
- Use input validation before database operations.
- Implement row-level security. Sanitize all user inputs."""
    },
    {
        "id": "devops-kubernetes-azure",
        "title": "DevOps + Kubernetes + Azure Pipelines",
        "title_ja": "DevOps + Kubernetes + Azure Pipelines",
        "description": "Senior DevOps rules covering Kubernetes (Helm, HPA, network policies), Azure Pipelines CI/CD, Bash scripting with shellcheck, Ansible playbooks with Vault, and Python automation with pytest.",
        "description_ja": "Kubernetes（Helm、HPA、ネットワークポリシー）、Azure Pipelines CI/CD、shellcheck付きBashスクリプト、Vault付きAnsible、pytestによるPython自動化を網羅するDevOpsルール。",
        "tool": "cursor",
        "format": ".cursorrules",
        "language": "YAML",
        "framework": "Kubernetes",
        "category": "devops",
        "tags": ["kubernetes", "azure", "devops", "ansible", "bash", "helm", "cicd", "terraform"],
        "author": "Ivan Barjaktarov",
        "source": "cursor.directory",
        "sourceUrl": "https://cursor.directory/devops",
        "stars": 420,
        "content": """You are a Senior DevOps Engineer with expertise in Kubernetes, Azure Pipelines, Python, Bash scripting, Ansible, and Azure Cloud Services.

General Guidelines
- Use English for all code, documentation, and comments.
- Prioritize modular, reusable, and scalable code.
- Avoid hard-coded values; use environment variables or configuration files.
- Apply Infrastructure-as-Code (IaC) principles where possible.
- Always consider the principle of least privilege in access and permissions.

Bash Scripting
- Write modular scripts with functions. Include comments for each major section.
- Validate all inputs using getopts or manual validation logic.
- Use shellcheck to lint scripts. Use trap for error handling.

Ansible Guidelines
- Follow idempotent design principles for all playbooks.
- Use group_vars and host_vars for environment-specific configurations.
- Validate all playbooks with ansible-lint. Use Ansible Vault for sensitive information.
- Use dynamic inventories for cloud environments.

Kubernetes Practices
- Use Helm charts or Kustomize to manage deployments.
- Follow GitOps principles to manage cluster state declaratively.
- Use workload identities for pod-to-service communications.
- Monitor with Prometheus, Grafana, and Falco.

Azure Cloud Services
- Use ARM templates or Terraform for provisioning.
- Use Azure Pipelines for CI/CD with reusable templates and stages.
- Integrate monitoring via Azure Monitor and Log Analytics.

DevOps Principles
- Automate repetitive tasks. Write modular, reusable CI/CD pipelines.
- Use containerized applications with secure registries.
- Manage secrets using Azure Key Vault.
- Build resilient systems with blue-green or canary deployment strategies.

Testing and Documentation
- Write meaningful unit, integration, and acceptance tests.
- Document solutions thoroughly in markdown. Use diagrams for architecture."""
    },
]

# Load existing rules
rules = json.loads(RULES_JSON.read_text())
existing_ids = {r["id"] for r in rules}

added = 0
for rule in new_rules:
    if rule["id"] in existing_ids:
        print(f"  SKIP (exists): {rule['id']}")
        continue
    # Ensure content is not empty placeholder for AGENTS.md/CLAUDE.md
    # We'll add a summary content for those without full content
    if not rule["content"]:
        rule["content"] = f"[Full content available at {rule['sourceUrl']}]"
    rules.append(rule)
    added += 1
    print(f"  ADD: {rule['id']} ({rule['tool']}) - {rule['title']}")

RULES_JSON.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n")
print(f"\nDone! Added {added} rules. Total: {len(rules)}")
