# 要求内容

## 概要

OpenAI Codex CLI 向けのスペック駆動開発（SDD）ハーネステンプレートを `codex-template/` ディレクトリに作成する。

## 背景

このリポジトリは Claude Code 向け SDD ハーネスをオリジナルとして、他のAIツール向けにテンプレートを展開している。Kiro テンプレート（`kiro-template/`）に続き、Codex CLI 向けテンプレートを作成する。

Kiro 展開と同様のアプローチで、Codex CLI のネイティブ機能に各ハーネス要素を移植する。

## 関連 Issue

https://github.com/kanan4gh/platform-harness-engineering/issues/26

## ユースケースの軸

Codex CLI を使うエンジニアが、このテンプレートを "Use this template" で複製するだけで、`AGENTS.md` に自プロジェクト情報を記入することができ、Codex エージェントがプロジェクトの方針・技術スタック・構造を理解した状態で SDD フローを開始できるようになる。

## ハーネス要素の対応関係（設計の前提）

| Claude Code | Kiro | Codex CLI |
|---|---|---|
| `CLAUDE.md`（3層構造） | `.kiro/steering/*.md`（4ファイル） | `AGENTS.md`（1ファイル、セクション構造） |
| `skills/` + `/コマンド` | `.kiro/hooks/*.json` | `AGENTS.md` 内のワークフロー記述 |
| `settings.json` hooks | `.kiro/hooks/*.json` | シェルスクリプト（任意追加） |
| `memory/` | なし（代替手段を文書化） | `~/.codex/AGENTS.md`（個人設定） |
| `.steering/YYYYMMDD-xxx/` | `.steering/YYYYMMDD-xxx/` | `.steering/YYYYMMDD-xxx/`（同一構造） |
| `.mcp.json` | `.kiro/settings/mcp.json` | `~/.codex/config.toml`（グローバル設定） |

## 実装対象の機能

### 1. AGENTS.md（文脈注入ファイル）

Codex CLI の主要な文脈注入メカニズム。Claude Code の `CLAUDE.md` 3層構造を1ファイルのセクション構造で表現する。

- セクション1: 開発プロセス原則（Kiro の `process.md` 相当、ハーネス共通で編集不要）
- セクション2: プロダクト定義（`product.md` 相当、プレースホルダー付き）
- セクション3: 技術スタック（`tech.md` 相当、プレースホルダー付き）
- セクション4: リポジトリ構造（`structure.md` 相当、プレースホルダー付き）

### 2. .steering/_template/（スペックテンプレート）

Kiro テンプレートと同一構造。`requirements.md` / `design.md` / `tasklist.md` の3ファイル。

### 3. docs/（永続ドキュメントテンプレート）

Kiro テンプレートと同一の6ファイル構成。内容はプレースホルダー付きテンプレート。

### 4. README.md

テンプレートの使い方・クイックスタート・Claude Code ハーネスからの移行表を記載。

### 5. ONBOARDING.md

セットアップから SDD ワンサイクル体験までのガイド。

## 受け入れ条件

### AGENTS.md

- [ ] プロセス原則セクションが含まれる（SDD フロー・tasklist.md 管理ルール）
- [ ] プロダクト定義セクションにプレースホルダーが含まれる
- [ ] 技術スタックセクションにプレースホルダーが含まれる
- [ ] リポジトリ構造セクションにプレースホルダーが含まれる
- [ ] `<!-- 例: ... -->` 形式の記入ガイドが含まれる
- [ ] Codex CLI のネイティブ構文を使用している（フロントマター等の Kiro 固有構文を含まない）

### .steering/_template/

- [ ] `requirements.md` / `design.md` / `tasklist.md` の3ファイルが存在する
- [ ] Kiro テンプレートの同名ファイルと実質同一の品質・構造を持つ

### docs/

- [ ] 6ファイルのテンプレートが存在する（product-requirements / functional-design / architecture / repository-structure / development-guidelines / glossary）
- [ ] 各ファイルにプレースホルダーが含まれ、そのまま使える状態

### README.md

- [ ] クイックスタート（テンプレート複製 → AGENTS.md 記入 → 最初の機能実装）が記載されている
- [ ] Claude Code ハーネスからの移行対応表が含まれる
- [ ] 「できること・できないこと」（hooks/skills 非対応など）が正直に記述されている

### ONBOARDING.md

- [ ] セットアップ手順が step-by-step で記述されている
- [ ] SDD ワンサイクル（requirements → design → tasklist → 実装 → PR）の手順が含まれる

## スコープ外

以下はこのフェーズでは実装しない:

- PRD の更新（codex-template 追加に伴う scope 反映）← 別タスクで対応
- publish-template.yml への Codex テンプレートリリース追加 ← 別タスクで対応
- Codex CLI での実際の動作検証（テンプレート作成後に別途）
- カスタムエージェント（Kiro の `.kiro/agents/` 相当）← Post-MVP

## 参照ドキュメント

- `docs/product-requirements.md` - プロダクト要求定義書
- `docs/functional-design.md` - 機能設計書
- `kiro-template/` - Kiro テンプレート（移植元・参考実装）
- `kiro-template/README.md` - Kiro README（構成参考）
- `kiro-template/ONBOARDING.md` - Kiro オンボーディング（構成参考）
- `kiro-template/.kiro/steering/process.md` - プロセス原則（AGENTS.md に移植）
