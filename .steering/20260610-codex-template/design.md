# 設計書

## アーキテクチャ概要

Codex CLI テンプレートは、Kiro テンプレートの設計思想を継承しつつ、Codex CLI のネイティブメカニズム（`AGENTS.md`）に合わせて再構成する。

```
codex-template/
├── AGENTS.md                     # 文脈注入ファイル（4セクション + ワークフロー定義）
├── .steering/
│   └── _template/                # スペックテンプレート（Kiro と同一）
│       ├── requirements.md
│       ├── design.md
│       └── tasklist.md
├── docs/                         # 永続ドキュメントテンプレート（プレースホルダー付き）
│   ├── product-requirements.md
│   ├── functional-design.md
│   ├── architecture.md
│   ├── repository-structure.md
│   ├── development-guidelines.md
│   └── glossary.md
├── README.md
└── ONBOARDING.md
```

## コンポーネント設計

### 1. AGENTS.md（文脈注入ファイル）

**責務**:
- Codex エージェントへのプロジェクト文脈の注入
- SDD プロセス原則の伝達
- ワークフロー定義（hooks の代替）

**実装の要点**:

Kiro は4ファイルを役割ごとに分離していたが、Codex は `AGENTS.md` 1ファイルに統合する。ファイルをセクション構造で整理することで、役割の明確さを保つ。

```markdown
# [プロダクト名] - 開発ガイド

## 開発プロセス原則        ← Kiro の process.md 相当（編集不要）
...

## プロダクト定義          ← Kiro の product.md 相当（要カスタマイズ）
...

## 技術スタック             ← Kiro の tech.md 相当（要カスタマイズ）
...

## リポジトリ構造           ← Kiro の structure.md 相当（要カスタマイズ）
...

## ワークフロー             ← Kiro の hooks 相当（編集不要）
...
```

**Kiro との主な差異**:

| 観点 | Kiro | Codex CLI |
|---|---|---|
| ファイル数 | 4ファイル（process/product/tech/structure） | 1ファイル（セクション構造） |
| フロントマター | `inclusion: always/auto/manual` | なし（全セクション常時読み込み） |
| ワークフロー定義 | `.kiro/hooks/*.json` (JSON トリガー) | `AGENTS.md` 内のワークフローセクション |
| `setup-project` | フック起動 → エージェントに指示 | 「setup-project を実行して」→ AGENTS.md 内の手順に従う |

**ワークフローセクションの設計**:

Kiro の hooks（`setup-project.json`、`add-feature.json`）相当の内容を AGENTS.md のワークフローセクションに埋め込む。ユーザーが「setup-project を実行してください」と依頼した際に、Codex がこのセクションを参照してフローを実行する。

```markdown
## ワークフロー

### setup-project

「setup-project を実行してください」と依頼された場合：
1. プロダクトの概要・目的・ターゲットユーザーをヒアリング
2. docs/ 配下に 6 ファイルを順番に作成（各ファイルでユーザー確認あり）
3. AGENTS.md のプロダクト定義・技術スタック・リポジトリ構造セクションを更新

### add-feature

「add-feature を実行してください」と依頼された場合：
1. 実装したい機能の名前を確認する
2. GitHub Issue を作成する（`gh issue create` または Web UI）
3. `.steering/_template/` をコピーして `.steering/YYYYMMDD-[機能名]/` を作成する
4. `requirements.md` を記入する → ユーザーの確認を得てから次へ
5. `design.md` を記入する → ユーザーの確認を得てから次へ
6. `tasklist.md` を記入する → ユーザーの確認を得てから実装へ
7. フィーチャーブランチを作成し、tasklist.md のタスクを順番に実装する
8. PR を作成してマージする

各ステップで必ずユーザーの確認を得てから次に進む。tasklist.md の管理ルール（全タスク完了の原則・スキップ禁止等）は AGENTS.md のプロセス原則セクションに記載する。
```

### 2. .steering/_template/（スペックテンプレート）

**責務**:
- SDD フローにおける作業単位のスペック作成ガイド

**実装の要点**:
- Kiro テンプレートの `.steering/_template/` と実質同一
- `kiro-template/.steering/_template/` の3ファイルをそのまま流用する
- 差分があれば Codex CLI 固有の記述に調整する

### 3. docs/（永続ドキュメントテンプレート）

**責務**:
- プロジェクト全体の「何を作るか」「どう作るか」のテンプレート提供

**実装の要点**:

Kiro テンプレートでは `setup-project` フックが docs/ を動的に生成していたが、Codex テンプレートでは **プレースホルダー付きテンプレートファイルを事前配置する**。

理由: Codex にはフックによる自動生成メカニズムがないため、ユーザーが手動で編集できる状態で提供する。セットアップ体験はやや劣るが、ユーザーが何を記入すべきか明確になる。

各ファイルに `<!-- TODO: ... -->` / `<!-- 例: ... -->` 形式のガイドコメントを付与する。

### 4. README.md

**責務**:
- テンプレートの概要・クイックスタート・移行ガイドの提供

**実装の要点**:
- Kiro README の構成を踏襲しつつ Codex 固有の内容に置き換える
- 「できること・できないこと」を正直に記述する（hooks・agents 非対応など）
- Claude Code ハーネスからの移行対応表を含める

### 5. ONBOARDING.md

**責務**:
- セットアップから SDD ワンサイクル体験までのガイド

**実装の要点**:
- Kiro ONBOARDING.md の構成を踏襲する
- Codex CLI 固有の操作手順（CLI コマンド、設定ファイルの場所など）に差し替える
- 前提条件として Codex CLI のインストールを含める

### 6. .devcontainer/（開発環境定義）

**責務**:
- Codex CLI がインストール済みの再現可能な開発環境の提供

**実装の要点**:

Kiro テンプレートは「devcontainer 非依存」方針だったが（Kiro がIDEとして完結するため）、Codex CLI はターミナルツールであり、このリポジトリ自体が Claude Code 用 devcontainer を持つのと同様に、Codex テンプレートも devcontainer を提供する。

このリポジトリの `.devcontainer/` を以下の方針で Codex 向けに改変する：

| 項目 | このリポジトリ（Claude Code） | codex-template（Codex CLI） |
|---|---|---|
| AIツール | `claude-code` devcontainer feature | Codex CLI を npm でインストール |
| ベースイメージ | `python:3.12-bookworm` | `universal:2`（技術スタック汎用） |
| マウント | `~/.aws`, `~/.claude`, `~/obsidian` | `~/.codex`（Codex 個人設定） |
| AWS/Python固有 | あり（このリポジトリ専用） | プレースホルダー化（汎用テンプレート） |
| GitHub CLI | あり | あり（`gh` コマンドは SDD フローで使用） |

**devcontainer.json の設計**:
- ベースイメージ: `mcr.microsoft.com/devcontainers/universal:2`（Python/Node/その他を含む汎用イメージ）
- Codex CLI: `postCreateCommand` で `npm install -g @openai/codex` によりインストール
- マウント: `~/.codex` を `/home/vscode/.codex` にマウント（個人設定・認証情報の引き継ぎ）
- GitHub CLI: `ghcr.io/devcontainers/features/github-cli:1` feature を使用
- 技術スタック固有の features（AWS CLI など）はコメントアウトしてプレースホルダーとして残す

**postCreate.sh の設計**:
- Codex CLI のインストール（`npm install -g @openai/codex`）
- GitHub CLI の動作確認
- バージョン確認（`codex --version`、`gh --version`）
- 技術スタック固有のセットアップはコメントアウトしてプレースホルダーとして残す

## データフロー

### テンプレート複製 → 初回セットアップ

```
1. GitHub "Use this template" でリポジトリ複製
2. Codex CLI でフォルダを開く
3. AGENTS.md を開き、プロダクト定義・技術スタック・リポジトリ構造を記入
   （または「setup-project を実行してください」で対話的に設定）
4. docs/ 配下の6ファイルを記入（または setup-project フローで自動作成）
5. 最初の機能実装: 「add-feature を実行してください」
```

### add-feature フロー（AGENTS.md 内ワークフローとして定義）

```
1. GitHub Issue を作成
2. .steering/_template/ をコピーして YYYYMMDD-[機能名]/ を作成
3. requirements.md 記入 → ユーザー確認
4. design.md 記入 → ユーザー確認
5. tasklist.md 記入 → ユーザー確認 → 実装開始
6. フィーチャーブランチ → PR → マージ
```

## ディレクトリ構造

```
codex-template/
├── AGENTS.md
├── .devcontainer/
│   ├── devcontainer.json
│   └── postCreate.sh
├── .steering/
│   └── _template/
│       ├── requirements.md
│       ├── design.md
│       └── tasklist.md
├── docs/
│   ├── product-requirements.md
│   ├── functional-design.md
│   ├── architecture.md
│   ├── repository-structure.md
│   ├── development-guidelines.md
│   └── glossary.md
├── README.md
└── ONBOARDING.md
```

## 実装の順序

1. AGENTS.md（文脈注入の核心・最優先）
2. .devcontainer/（環境定義）
3. .steering/_template/（kiro-template から流用・調整）
4. docs/（プレースホルダー付きテンプレート6ファイル）
5. README.md
6. ONBOARDING.md

## Kiro テンプレートとの対応表（実装時の参考）

| Codex テンプレートファイル | Kiro テンプレートファイル | 対応方針 |
|---|---|---|
| `AGENTS.md`（プロセス原則セクション） | `.kiro/steering/process.md` | 内容を移植、フロントマター除去 |
| `AGENTS.md`（プロダクト定義セクション） | `.kiro/steering/product.md` | セクション形式に変換 |
| `AGENTS.md`（技術スタックセクション） | `.kiro/steering/tech.md` | セクション形式に変換 |
| `AGENTS.md`（リポジトリ構造セクション） | `.kiro/steering/structure.md` | セクション形式に変換 |
| `AGENTS.md`（ワークフローセクション） | `.kiro/hooks/*.json` | JSON → Markdown テキストに変換 |
| `.steering/_template/` | `.steering/_template/` | そのまま流用（差分のみ調整） |
| `docs/*.md`（6ファイル） | （Kiro は setup-project で動的生成） | プレースホルダー付きテンプレートとして事前配置 |
| `README.md` | `README.md` | 構成踏襲、Codex 固有内容に差し替え |
| `ONBOARDING.md` | `ONBOARDING.md` | 構成踏襲、Codex 固有内容に差し替え |
| `.devcontainer/` | なし（devcontainer 非依存方針） | 新規作成（CLI ツールのため devcontainer 有効） |

## 将来の拡張性

- Codex CLI がフックやエージェント定義をネイティブサポートした際、`AGENTS.md` のワークフローセクションを専用ファイルに分離できる
- `docs/` テンプレートは他のツール向けテンプレートと共通化できる可能性がある
