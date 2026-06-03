# タスクリスト

## 🚨 タスク完全完了の原則

**全タスクが `[x]` になるまで作業を継続すること**

---

## フェーズ1: カスタムエージェントの実装

- [x] `kiro-template/.kiro/agents/` ディレクトリを作成する
- [x] `kiro-template/.kiro/agents/implementation-validator.md` を作成する
  - [x] frontmatter（`name`, `description`）を設定する
  - [x] 目的・検証観点5つ・検証プロセス・出力フォーマット・検証の姿勢を記述する
  - [x] Claude Code 固有要素（npm コマンド・TypeScript コード例）を除去する
- [x] `kiro-template/.kiro/agents/doc-reviewer.md` を作成する
  - [x] frontmatter（`name`, `description`）を設定する
  - [x] 目的・レビュー観点5つ・レビュープロセス・ドキュメント種別ごとのチェック項目・出力フォーマット・レビューの姿勢を記述する
  - [x] Claude Code 固有要素を除去する

## フェーズ2: 受け入れテスト（Kiro で実施）

- [x] `kiro-template/` を Kiro プロジェクトに展開する
- [x] Kiro エージェントにカスタムエージェント frontmatter の仕様を確認する（`model` 等のサポート状況）
  - [x] `model` がサポートされていれば両エージェントファイルに `model: claude-sonnet-4` を追記する（`claude-sonnet-4-5` は無効、`claude-sonnet-4` が正しいことを受け入れテストで確認）
- [x] `@implementation-validator` を呼び出して正常動作を確認する
- [x] `@doc-reviewer` を呼び出して正常動作を確認する
- [x] `#skill-sdd-guide` をチャットで参照し、SDD ルールが読み込まれることを確認する（Phase 2 検証）

## フェーズ3: 振り返り

- [x] 振り返りをこのファイルの下部に記録する

---

## 実装後の振り返り

### 実装完了日
2026-06-04

### 計画と実績の差分
- `model: claude-sonnet-4-5` が Kiro で無効だった。受け入れテスト中に Kiro が自動修正し `claude-sonnet-4` が正しいと判明。リポジトリ側も修正した。
- `@doc-reviewer` のテストは `docs/` が存在しないため README.md で代替したが、動作確認として十分だった。
- それ以外は計画通り。

### 学んだこと
- Kiro カスタムエージェントの frontmatter で使えるフィールド: `name`, `description`, `model`, `tools`, `includeMcpJson`, `includePowers`
- 有効なモデル名は `claude-sonnet-4`（`claude-sonnet-4-5` は無効）
- `tools: ["read"]` で読み取り専用エージェントを適切にスコープできる
- `#skill-sdd-guide` の manual steering は期待通り動作した（Phase 2 の動作も確認完了）
- `@agent-name` の呼び出しは、Kiro がファイル存在チェックなどの前処理をしてからエージェントに委譲するケースがある

### 次回への改善提案
- `docs/architecture.md` に Kiro エージェント frontmatter の確定仕様（`model`, `tools` 等）を追記する
- `tools` の適切な組み合わせをエージェントの用途別に整理してドキュメント化する

### リリース判断

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes |
| 未解決の重大バグはないか | なし |
| 適切なバージョン種別 | MINOR |

**提案**: Phase 1〜3 がすべて揃い、Kiro ハーネスの三層構造（hooks・manual steering・agents）が完成した。Phase 2・3 の受け入れテストも通過済みのため MINOR リリースを推奨。
