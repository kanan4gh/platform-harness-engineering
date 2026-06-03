# リポジトリ構造定義書 (Repository Structure Document)

## このリポジトリの構造（Bootstrap フェーズ）

Bootstrap フェーズでは、このリポジトリ自体が「Claude Code を使って Kiro ハーネスを設計・実装する」作業環境となっています。2 つの層が共存しています。

```
platform-harness-for-kiro/                    # リポジトリルート
├── .claude/                                  # Claude Code 開発インフラ
│   ├── agents/                              # サブエージェント定義
│   ├── commands/                            # スラッシュコマンド定義
│   └── skills/                              # スキル定義
├── .devcontainer/                            # Claude Code 開発環境（Kiro テンプレートには含まれない）
├── .steering/                                # Claude Code 作業スペック（作業履歴）
│   ├── YYYYMMDD-[タスク名]/                 # 作業単位ごとのスペック
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasklist.md
│   └── example/
├── docs/                                     # このプロジェクトの永続ドキュメント
│   ├── ideas/                               # 壁打ち・ブレインストーミング
│   ├── product-requirements.md
│   ├── functional-design.md
│   ├── architecture.md
│   ├── repository-structure.md              # 本ドキュメント
│   ├── development-guidelines.md
│   └── glossary.md
├── kiro-template/                            # Kiro テンプレート成果物フォルダ
│   ├── .kiro/
│   ├── .steering/
│   └── README.md
├── .gitignore
├── .mcp.json.example
├── CLAUDE.md                                 # Claude Code 設定
└── README.md
```

**2層構造の説明**:

| 層 | ディレクトリ | 説明 |
|---|---|---|
| Claude Code 開発インフラ | `.claude/`, `.devcontainer/`, `.steering/`, `CLAUDE.md` | Bootstrap フェーズの作業環境。Kiro ユーザーには配布しない |
| Kiro テンプレート成果物 | `kiro-template/` | Kiro ユーザーに展開される成果物。このフォルダの中身がテンプレートとして配布される |
| 共有 | `docs/`, `README.md`, `.gitignore` | このリポジトリの永続ドキュメントおよびルートファイル |

---

## kiro-template/ の構造（Kiro テンプレートの成果物）

`kiro-template/` は、Kiro ユーザーが "Use this template" でリポジトリを複製した際に得られる成果物フォルダです。

```
kiro-template/                                # Kiro テンプレート成果物フォルダ
├── .kiro/                                    # Kiro IDE 設定（文脈層・自動化層）
│   ├── steering/                             # 常時参照コンテキスト
│   │   ├── process.md                       # 開発プロセス原則
│   │   ├── product.md                       # プロダクト固有定義
│   │   ├── tech.md                          # 技術スタック・環境設定
│   │   └── structure.md                     # リポジトリ構造定義（要約版）
│   ├── hooks/                                # 自動化フック
│   │   └── tasklist-check.json              # タスクリスト更新時フック
│   └── settings/                             # Kiro 設定
│       └── mcp.json                         # MCP サーバー設定（ひな型）
├── .steering/                                # プロジェクトハーネス層
│   └── _template/                           # 作業単位スペックのテンプレート
│       ├── requirements.md                  # 要求仕様テンプレート
│       ├── design.md                        # 設計テンプレート
│       └── tasklist.md                      # タスクリストテンプレート
└── README.md                                 # セットアップガイド
```

> `docs/` はこのリポジトリの永続ドキュメントとして `kiro-template/` 外に配置しています。Kiro テンプレートとして配布する際、Kiro ユーザーは自分のプロジェクト用に `docs/` を新規作成します。

## ディレクトリ詳細

### `kiro-template/.kiro/steering/`（文脈層）

**役割**: Kiro エージェントの全会話コンテキストに常時注入されるマークダウンファイル群。Claude CLI の CLAUDE.md を役割ごとに分割したもの。

| ファイル | 役割 | inclusionMode | 更新契機 |
|---------|------|--------------|---------|
| `process.md` | 開発プロセス原則（普遍的ルール） | always | ハーネス改善時 |
| `product.md` | プロダクト概要・目的・docs/ 一覧 | always | プロダクト定義変更時 |
| `tech.md` | 技術スタック・環境設定・OS別セットアップ手順 | always | 技術スタック変更時 |
| `structure.md` | リポジトリ構造の要約（本ドキュメントの簡略版） | always | 構造変更時 |

**ファイルフォーマット**:
```markdown
---
inclusion: always
---

# [タイトル]

[内容]
<!-- 例: ... --> 形式の記入ガイドを含める
```

**配置ルール**:
- テンプレート状態では各ファイルに `<!-- 例: ... -->` 形式の記入ガイドを含める
- プロジェクト固有の値（プロダクト名・技術スタック等）をプレースホルダーで示す
- `process.md` はハーネス共通のため、プロジェクトが直接編集しないことを推奨

---

### `kiro-template/.kiro/hooks/`（自動化層）

**役割**: Kiro のトリガー機能を使った定型作業の自動化。エンジニアが手動 CLI 実行することを前提としない。

**配置ファイル**:

| ファイル | トリガー | 目的 |
|---------|---------|------|
| `tasklist-check.json` | `tasklist.md` 保存時 | 未完了タスクの確認を促す |

**配置ルール**:
- テンプレートに含めるフックは最小限（動作確認済みのもののみ）
- プロジェクト固有フックはプロジェクト側で追加する
- フック API は Kiro のバージョンに依存するため、テンプレートのフックはシンプルな構成にとどめる

---

### `kiro-template/.kiro/settings/`（Kiro 設定）

**役割**: Kiro IDE の設定ファイル群。

**配置ファイル**:

| ファイル | 内容 |
|---------|------|
| `mcp.json` | MCP サーバー設定のひな型（実際のサーバー設定はプロジェクト側で記入） |

**配置ルール**:
- `mcp.json` はテンプレート状態では空のひな型のみ含める
- プラットフォーム共通 MCP（GitHub 等）はユーザーのグローバル設定で管理する（リポジトリには含めない）

---

### `kiro-template/.steering/`（プロジェクトハーネス層）

**役割**: 作業単位のスペックファイル群。「今回の作業で何を・どう・どの順で実装するか」を定義する。Claude CLI ハーネスの `.steering/` と同一構造。

> **重要**: Kiro の built-in specs 機能（`.kiro/specs/`）は使用しない（`docs/functional-design.md` 設計指針3を参照）。

**ディレクトリ構造**:
```
kiro-template/.steering/
├── _template/                  # テンプレート（直接編集しない）
│   ├── requirements.md
│   ├── design.md
│   └── tasklist.md
├── 20250115-add-login/         # 作業単位（_template/ をコピーして作成）
│   ├── requirements.md
│   ├── design.md
│   └── tasklist.md
└── 20250120-fix-auth-bug/
    └── ...
```

**命名規則**:
- `YYYYMMDD-[タスク名（英小文字・ハイフン区切り）]`
- 例: `20250115-add-user-profile`, `20250120-fix-login-bug`

**`_template/` 各ファイルの必須構成**:

| ファイル | 必須項目 |
|---------|---------|
| `requirements.md` | 関連 GitHub Issue URL・ユーザーストーリー・受け入れ条件・スコープ外 |
| `design.md` | 実装アプローチ・変更対象ファイル一覧・技術的判断と根拠 |
| `tasklist.md` | チェックリスト形式タスク・完了基準（実装 → テスト → ドキュメント更新の順） |

**使い方**:
1. GitHub Issue を作成する
2. `_template/` を Kiro GUI でコピーし、`YYYYMMDD-[タスク名]/` として配置する
3. `requirements.md` → `design.md` → `tasklist.md` の順で記入する
4. Kiro エージェントに対して対象スペックファイルを明示的に指示して実装を開始する

**Git 管理**:
- `.steering/` はバージョン管理対象とする（意思決定の履歴として保持）
- `_template/` は直接編集しない（改善は環流プロセスで対応）

---

### `docs/`（永続ドキュメント層）

**役割**: プロジェクト全体の「何を作るか」「どう作るか」を定義する。頻繁に更新されない「北極星」ドキュメント群。

**配置ドキュメント**:

| ファイル | 役割 | 更新契機 |
|---------|------|---------|
| `product-requirements.md` | プロダクト要求定義書 | プロダクトの方向性変更時 |
| `functional-design.md` | 機能設計書・設計指針 | 機能追加・設計方針変更時 |
| `architecture.md` | 技術仕様書 | 技術スタック・アーキテクチャ変更時 |
| `repository-structure.md` | 本ドキュメント | リポジトリ構造変更時 |
| `development-guidelines.md` | 開発ガイドライン | 開発プロセス変更時 |
| `glossary.md` | ユビキタス言語定義 | 新しいドメイン用語が生まれた時 |

**`docs/ideas/`**:
- 壁打ち・ブレインストーミングの成果物を自由形式で保管
- 正式ドキュメントへの昇格前の草稿置き場
- `.gitkeep` で空ディレクトリを Git 管理する

---

### ルートファイル

| ファイル | 役割 |
|---------|------|
| `kiro-template/README.md` | セットアップガイド（GUI 操作のみで記述・kiro-cli 手順は含めない） |
| `.gitignore` | Git 除外設定 |

## ファイル配置規則

### 配置判断フロー

```
新しいファイルを作る場合:
│
├─ Kiro の常時コンテキストとして注入したい
│   → kiro-template/.kiro/steering/ に配置
│
├─ 特定のトリガーで自動実行したい
│   → kiro-template/.kiro/hooks/ に配置
│
├─ 作業単位のスペック（今回の作業用）
│   → kiro-template/.steering/YYYYMMDD-xxx/ に配置
│
├─ プロジェクト全体の永続的な定義
│   → docs/ に配置
│
└─ ブレインストーミング・草稿
    → docs/ideas/ に配置
```

### 命名規則

| 種別 | 規則 | 例 |
|------|------|----|
| steering ファイル | `[役割].md`（英小文字） | `process.md`, `tech.md` |
| フックファイル | `[目的].json`（kebab-case） | `tasklist-check.json` |
| 作業スペックディレクトリ | `YYYYMMDD-[タスク名]`（英小文字・ハイフン区切り） | `20250115-add-login` |
| ドキュメント | `[種別].md`（kebab-case） | `product-requirements.md` |

## 除外設定（`.gitignore`）

```gitignore
# 環境固有ファイル
.env
.env.local
.env.*.local

# OS 生成ファイル
.DS_Store
Thumbs.db

# エディタ設定（Kiro・VS Code 以外）
.idea/
*.swp

# ランタイム・ビルド成果物（プロジェクト固有）
__pycache__/
*.pyc
node_modules/
dist/
build/
*.egg-info/
.pytest_cache/
```

**`.steering/` を `.gitignore` に含めない理由**:
作業スペックは「開発の意思決定履歴」として価値があるため、バージョン管理対象とする。

## テンプレートとしての使い方

### 必須変更（プロジェクト開始時）

| 対象 | 作業内容 |
|------|---------|
| `kiro-template/.kiro/steering/product.md` | プロダクト概要・目的・docs/ 一覧を記入 |
| `kiro-template/.kiro/steering/tech.md` | 技術スタック・OS 別セットアップ手順を記入 |
| `kiro-template/.kiro/steering/structure.md` | プロジェクトのディレクトリ構造を反映 |
| `docs/product-requirements.md` | PRD を作成 |
| `kiro-template/README.md` | プロジェクト固有のセットアップ手順に書き換え |

### 任意変更（プロジェクトの必要に応じて）

| 対象 | 作業内容 |
|------|---------|
| `kiro-template/.kiro/settings/mcp.json` | プロジェクト固有 MCP サーバーを追加 |
| `kiro-template/.kiro/hooks/` | プロジェクト固有フックを追加 |
| `docs/` 残り 5 ドキュメント | 機能設計・アーキテクチャ等を作成 |

### 変更しないもの

| 対象 | 理由 |
|------|------|
| `kiro-template/.kiro/steering/process.md` | ハーネス共通の開発プロセス原則。改善は環流プロセスで対応 |
| `kiro-template/.steering/_template/` | テンプレートは直接編集しない。改善は環流プロセスで対応 |
