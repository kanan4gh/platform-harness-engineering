# 設計書

## 実装アプローチ

Claude Code の `.claude/agents/` 定義を Kiro のカスタムエージェント形式（`.kiro/agents/*.md`）に移植する。
各エージェントの「検証観点」と「出力フォーマット」は維持しつつ、Claude Code 固有の要素（npm コマンド・TypeScript コード例）を除去してツール非依存に整理する。

## 変更対象ファイル

| ファイル | 変更種別 | 内容 |
|---------|---------|------|
| `kiro-template/.kiro/agents/implementation-validator.md` | 新規作成 | 実装検証エージェント |
| `kiro-template/.kiro/agents/doc-reviewer.md` | 新規作成 | ドキュメントレビューエージェント |

## Kiro エージェントのフォーマット

```markdown
---
name: エージェント名（@呼び出し時の識別子）
description: エージェントの役割説明（1行）
---

# エージェント本体の指示
...
```

- `name`: `@name` で呼び出す識別子
- `description`: Kiro が用途を判断するためのサマリー
- `model` 指定は Kiro の公式ドキュメントで未確認のため省略（受け入れテスト時に Kiro エージェントへ直接確認し、サポートされていれば追記する）

## 移植方針：Claude Code → Kiro

| Claude Code 要素 | Kiro での扱い |
|---|---|
| `model: sonnet` frontmatter | 省略（Kiro 未確認） |
| npm lint/typecheck/test 実行 | 省略（ツール依存のため） |
| TypeScript コード例（命名規則・エラーハンドリング） | 省略（言語非依存化） |
| 検証観点・チェックリスト・評価基準 | そのまま維持 |
| 検証プロセス（ステップ定義） | そのまま維持 |
| 検証結果の出力フォーマット（マークダウン表） | そのまま維持 |
| ドキュメント種別ごとの追加チェック項目 | そのまま維持 |

## 各エージェントの構成

### implementation-validator.md

```
# 実装検証エージェント

## 目的
## 検証観点（5つ）
  - スペック準拠
  - コード品質
  - テストカバレッジ
  - セキュリティ
  - パフォーマンス
## 検証プロセス（ステップ定義）
## 検証結果の報告フォーマット
## 検証の姿勢
```

### doc-reviewer.md

```
# ドキュメントレビューエージェント

## 目的
## レビュー観点（5つ）
  - 完全性
  - 明確性
  - 一貫性
  - 実装可能性
  - 測定可能性
## レビュープロセス（ステップ定義）
## ドキュメント種別ごとの追加チェック項目（6種）
## レビュー結果の出力フォーマット
## レビューの姿勢
```

## 実装の順序

1. `kiro-template/.kiro/agents/` ディレクトリを作成
2. `implementation-validator.md` を作成
3. `doc-reviewer.md` を作成
