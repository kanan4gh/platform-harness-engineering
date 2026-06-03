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

- [ ] `kiro-template/` を Kiro プロジェクトに展開する
- [ ] Kiro エージェントにカスタムエージェント frontmatter の仕様を確認する（`model` 等のサポート状況）
  - [ ] `model` がサポートされていれば両エージェントファイルに `model: sonnet` を追記する
- [ ] `@implementation-validator` を呼び出して正常動作を確認する
- [ ] `@doc-reviewer` を呼び出して正常動作を確認する
- [ ] `#skill-sdd-guide` をチャットで参照し、SDD ルールが読み込まれることを確認する（Phase 2 検証）

## フェーズ3: 振り返り

- [ ] 振り返りをこのファイルの下部に記録する

---

## 実装後の振り返り

### 実装完了日
[記入]

### 計画と実績の差分
- [記入]

### 学んだこと
- [記入]

### 次回への改善提案
- [記入]

### リリース判断

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | [Yes / No / 保留] |
| 未解決の重大バグはないか | [なし / あり: 内容] |
| 適切なバージョン種別 | [MAJOR / MINOR / PATCH / リリース不要] |

**提案**: [記入]
