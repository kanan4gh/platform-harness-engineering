# platform-harness-engineering

Kiro ハーネス（[platform-harness-for-kiro](https://github.com/kanan4gh/platform-harness-for-kiro)）を設計・開発・発行するための作業場リポジトリです。

## ハーネスとは何か

> **「エンジンを動かすために必要な、エンジン以外のすべて」**

AI 駆動開発において、LLM（Claude）がエンジンだとすれば、ハーネスは LLM を有効に動かすすべての仕組みです。

| 要素 | 具体例 | 役割 |
|------|--------|------|
| **文脈の注入** | CLAUDE.md、requirements.md | LLM が何をすべきかを定義する |
| **プロセスの型** | steering スキル、tasklist.md | 作業手順を強制する |
| **記憶** | memory/ | セッションをまたぐ一貫性を保つ |
| **検証** | テスト、リンター | 出力の品質を保証する |
| **ツール** | MCP サーバー | LLM の手の届く範囲を広げる |

## 2層構造

```
┌──────────────────────────────────────────┐
│        プラットフォームハーネス           │
│  プロジェクト横断・再利用・継続的に進化   │
├──────────────────────────────────────────┤
│        プロジェクトハーネス              │
│  プロジェクト固有・スペックそのもの      │
└──────────────────────────────────────────┘
```

**プラットフォームハーネス**（このリポジトリが提供するもの）:
- `CLAUDE.md` 汎用層 — スペック駆動開発の原則
- `.claude/skills/` — `steering`、`add-feature` 等のスキル
- `.claude/skills/steering/templates/` — requirements / design / tasklist のテンプレート
- `memory/` — セッションをまたぐ知識

**プロジェクトハーネス**（各テンプレートを使うプロジェクトが育てるもの）:
- `CLAUDE.md` プロダクト固有層・技術スタック固有層
- `.steering/YYYYMMDD-xxx/` — 作業単位の要求・設計・タスクリスト
- `docs/` — プロダクトの永続ドキュメント

## このリポジトリについて

Claude Code を使ってスペック駆動開発（SDD）で Kiro ハーネスを育てるための環境です。

```
kiro-template/         ← ここを育てる
       ↓ gh release create
platform-harness-for-kiro  ← Kiro ユーザーが "Use this template" で使う
```

## 開発フロー

```
1. GitHub Issue を作成
2. /add-feature で機能実装（ステアリングファイル → 実装 → PR）
3. PR をマージ
4. gh release create でリリース（kiro-template/ が自動発行される）
```

詳細は `CLAUDE.md` を参照してください。

## 関連リポジトリ

| リポジトリ | 用途 |
|-----------|------|
| [platform-harness-engineering](https://github.com/kanan4gh/platform-harness-engineering)（本リポジトリ） | 作業場・開発環境 |
| [platform-harness-for-kiro](https://github.com/kanan4gh/platform-harness-for-kiro) | Kiro ユーザー向け配布テンプレート |

## 内部Kiroユーザー向け

このリポジトリ自体を Kiro で開いてハーネス改善作業をする方は [ONBOARDING.md](kiro-template/ONBOARDING.md) を参照してください（GHE へのデプロイ手順も記載）。
