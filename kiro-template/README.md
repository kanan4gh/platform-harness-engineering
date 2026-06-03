# Kiro ハーネステンプレート

Kiro IDE 向けのスペック駆動開発（SDD）ハーネスです。このテンプレートを複製することで、Kiro エージェントがプロジェクトの方針・技術スタック・構造を理解した状態で開発を支援できる環境を即座に構築できます。

## このテンプレートについて

### ハーネスとは

「エンジンを動かすために必要な、エンジン以外のすべて」。Kiro（LLM エンジン）を有効に動かすための文脈注入・プロセス定義・自動化の仕組みを指します。

### 構成

```
.kiro/
├── steering/          # Kiro エージェントへの常時コンテキスト注入
│   ├── process.md    # 開発プロセス原則（編集不要）
│   ├── product.md    # プロダクト定義（要カスタマイズ）
│   ├── tech.md       # 技術スタック・環境設定（要カスタマイズ）
│   └── structure.md  # リポジトリ構造（要カスタマイズ）
├── hooks/             # 定型作業の自動化
└── settings/
    └── mcp.json      # MCP サーバー設定（任意）
.steering/
└── _template/         # 機能実装時にコピーして使うスペックテンプレート
    ├── requirements.md
    ├── design.md
    └── tasklist.md
docs/                  # プロジェクト永続ドキュメント
    ├── product-requirements.md
    ├── functional-design.md
    ├── architecture.md
    ├── repository-structure.md
    ├── development-guidelines.md
    └── glossary.md
```

## クイックスタート

### 1. テンプレートを複製する

GitHub の **"Use this template"** ボタンをクリックして、新しいリポジトリを作成します。

### 2. Kiro でフォルダを開く

作成したリポジトリを Kiro IDE で開きます。`.kiro/steering/` が自動的に読み込まれます。

### 3. steering ファイルをカスタマイズする（必須）

Kiro のファイルエクスプローラーから以下のファイルを編集します：

**`.kiro/steering/product.md`**
- プロダクト名・ビジョン・目的を記入
- `docs/` 配下のドキュメント一覧を更新

**`.kiro/steering/tech.md`**
- 技術スタック（言語・フレームワーク・ツール）を記入
- OS 別セットアップ手順を記入

**`.kiro/steering/structure.md`**
- プロジェクトのディレクトリ構造を記入

> `.kiro/steering/process.md` はハーネス共通のルールブックです。通常は編集不要です。

### 4. 最初の機能スペックを作成する

1. GitHub で Issue を作成する（Web UI）
2. `.steering/_template/` を Kiro GUI でコピーし `YYYYMMDD-[機能名]/` として配置
3. `requirements.md` → `design.md` → `tasklist.md` の順で記入
4. Kiro エージェントにスペックファイルを示して実装を開始

## 注意事項

- **kiro-cli は使いません**: 全操作を Kiro IDE の GUI 内で完結させます
- **Kiro built-in specs は使いません**: Kiro が「Spec mode に切り替えますか？」と提案した場合は断ってください。`.steering/YYYYMMDD-xxx/` を引き続き使用します
- **Docker / devcontainer は不要**: 環境構築は `tech.md` に OS 別手順として記述します

## MCP サーバーの追加（任意）

プロジェクト固有の MCP サーバーは `.kiro/settings/mcp.json` に追加します。

```json
{
  "mcpServers": {
    "your-server": {
      "command": "...",
      "args": [...]
    }
  }
}
```

> GitHub・ファイルシステム等のプラットフォーム共通 MCP は、Kiro のユーザーグローバル設定で管理することを推奨します（リポジトリに含めない）。

## このリポジトリのメタ構造について

このリポジトリ自体が「Claude CLI を使って Kiro ハーネスを設計・実装する」というブートストラップ構造を持っています。

| フェーズ | 説明 |
|---------|------|
| **Bootstrap** | Claude CLI でハーネスを設計・実装する（現在） |
| **動作確認** | Kiro を開いて受け入れテストを実施する |
| **リリース** | Kiro ユーザーがテンプレートを使い始める |
| **自走** | Kiro ハーネス自体の改善を Kiro 上で行う |

> **重要**: Kiro ユーザーがテンプレートを使い始められるのは「動作確認フェーズ合格後」です。「Claude CLI 環境（`.claude/` 等）の削除」は自走フェーズ移行後の任意のタイミングで行います。

## Claude CLI ハーネスから移行する場合

Claude CLI（CLAUDE.md）でスペック駆動開発をしていた方向けの対応表です。

| Claude CLI 要素 | Kiro での対応先 |
|----------------|----------------|
| `CLAUDE.md` 汎用層（開発プロセス原則） | `.kiro/steering/process.md`（編集不要） |
| `CLAUDE.md` プロダクト固有層 | `.kiro/steering/product.md` |
| `CLAUDE.md` 技術スタック固有層 | `.kiro/steering/tech.md` |
| `.steering/YYYYMMDD-xxx/` 作業スペック | `.steering/YYYYMMDD-xxx/`（構造は同一） |
| `settings.json` hooks | `.kiro/hooks/` |
| `.mcp.json` | `.kiro/settings/mcp.json` |
| `CLAUDE.md` に記載していたリポジトリ構造 | `.kiro/steering/structure.md` |

詳細な概念マッピングは `docs/functional-design.md` を参照してください。

## ライセンス

MIT
