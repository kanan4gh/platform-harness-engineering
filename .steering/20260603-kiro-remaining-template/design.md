# 設計書

## 実装アプローチ

3ファイルを独立して実装する。依存関係はなく並行実装可能。

```
kiro-template/
├── .kiro/
│   ├── hooks/
│   │   └── tasklist-check.json   # 新規作成
│   └── settings/
│       └── mcp.json              # 新規作成
└── README.md                     # 新規作成
```

## 変更対象ファイル

| ファイル | 変更種別 | 内容 |
|---------|---------|------|
| `kiro-template/.kiro/hooks/tasklist-check.json` | 新規作成 | tasklist.md 保存時フック |
| `kiro-template/.kiro/settings/mcp.json` | 新規作成 | MCP 設定ひな型 |
| `kiro-template/README.md` | 新規作成 | セットアップガイド |

## 各ファイルの設計

### tasklist-check.json

`docs/architecture.md` のフックフォーマット仕様に従う:

```json
{
  "name": "tasklist-check",
  "description": "tasklist.md が更新された時に未完了タスクの確認を促す",
  "trigger": {
    "event": "file_save",
    "filePattern": "**/.steering/**/tasklist.md"
  },
  "prompt": "tasklist.md が更新されました。未完了タスク（[ ]）が残っていないか確認し、全タスクが完了するまで実装を継続してください。"
}
```

**注意**: Kiro の hooks API は仕様変更リスクがある。`trigger.event` や `filePattern` の値は Kiro の実際の仕様に依存するため、テンプレートには「動作確認済みの最小構成」として位置付け、受け入れテストで確認する。

### mcp.json

JSON では仕様上コメントを記述できない。代わりに空の `mcpServers` オブジェクトを提供し、README または process.md でグローバル設定との使い分けを説明する。

```json
{
  "mcpServers": {}
}
```

プロジェクト固有 MCP を追加する場合の記入例をコメントアウト形式で README に示す（JSON ファイル自体には書けないため）。

### README.md

`docs/architecture.md` のドキュメント品質チェックリストを全て満たす構成:

```
# [プロジェクト名]（またはテンプレートとしてのタイトル）

## このテンプレートについて
- ハーネスの概念説明（簡潔に）
- kiro-template/ フォルダの説明

## クイックスタート
1. "Use this template" でリポジトリを複製
2. Kiro でフォルダを開く
3. steering ファイルをカスタマイズ（GUI 操作）
4. 最初の機能スペックを作成

## セットアップ詳細
### 必須カスタマイズ（プロジェクト開始時）
### 推奨カスタマイズ

## ブートストラップ・フェーズについて
（このリポジトリのメタ構造説明）

## ライセンス（任意）
```

## 技術的判断と根拠

| 判断 | 根拠 |
|------|------|
| mcp.json を空の `{"mcpServers": {}}` にする | JSON はコメント不可。最小限の有効な JSON を提供し、使い方は README で説明する |
| hooks の filePattern に `**/.steering/**/tasklist.md` を使う | `.steering/` はルート直下にあり、どの深さにある tasklist.md も対象にする |
| README をテンプレートとして汎用的に書く | このリポジトリ自体が Kiro ハーネステンプレートなので、テンプレートとしての使い方を説明する README にする |

## 実装の順序

1. `kiro-template/.kiro/hooks/` ディレクトリを作成して `tasklist-check.json` を実装
2. `kiro-template/.kiro/settings/` ディレクトリを作成して `mcp.json` を実装
3. `kiro-template/README.md` を実装

<!-- この順序を tasklist.md のフェーズ1タスクに展開してください -->
