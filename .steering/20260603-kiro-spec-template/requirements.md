# 要求内容

## 概要

`kiro-template/.steering/_template/` 配下に3つのスペックテンプレートファイルを実装する。Kiro ユーザーが機能実装時にコピーして使う `requirements.md`・`design.md`・`tasklist.md` のひな型を作成する。

## 背景

`kiro-template/.kiro/steering/process.md` に「`.steering/_template/` をコピーして作業単位スペックを作成する」と定義したが、テンプレート自体がまだ存在しない。テンプレートがなければ Kiro ユーザーはスペック駆動開発を開始できない。

## 関連 Issue

https://github.com/kanan4gh/platform-harness-for-kiro/issues/2

## ユースケースの軸

Kiro ユーザーが新機能の実装を開始する際に、`.steering/_template/` をコピーして `YYYYMMDD-xxx/` を作成し、プレースホルダーを埋めるだけでスペックが完成する。

## 実装対象の機能

### 1. requirements.md テンプレート

- 関連 GitHub Issue URL の記入欄（必須）
- ユーザーストーリー形式の要求定義プレースホルダー
- 受け入れ条件チェックリスト
- スコープ外の明示欄

### 2. design.md テンプレート

- 実装アプローチのプレースホルダー
- 変更対象ファイル一覧の記入欄
- 技術的判断と根拠の記入欄

### 3. tasklist.md テンプレート

- タスク完全完了の原則セクション（ルール明示）
- フェーズ分けされたチェックリスト形式タスク
- 実装 → 品質チェック → ドキュメント更新の順序
- 実装後の振り返りセクション

## 受け入れ条件

### requirements.md

- [ ] GitHub Issue URL の記入欄が含まれている（必須項目として明示）
- [ ] ユーザーストーリー（「〜として、〜のために、〜が欲しい」形式）のプレースホルダーがある
- [ ] 受け入れ条件がチェックリスト形式（`- [ ]`）で記述できる構造になっている
- [ ] スコープ外の記入欄がある
- [ ] `<!-- 例: ... -->` 形式の記入ガイドが含まれている

### design.md

- [ ] 実装アプローチの記入欄がある
- [ ] 変更対象ファイル一覧の記入欄がある
- [ ] 技術的判断と根拠の記入欄がある
- [ ] `<!-- 例: ... -->` 形式の記入ガイドが含まれている

### tasklist.md

- [ ] タスク完全完了の原則（全タスク `[x]` 必須・スキップ禁止）が明記されている
- [ ] フェーズ分けされた `- [ ]` チェックリスト形式になっている
- [ ] 実装後の振り返りセクション（完了日・差分・学び・次回への提案）がある
- [ ] リリース判断セクションがある

## スコープ外

- `kiro-template/docs/` のドキュメントテンプレート群（別スペックで対応）
- `kiro-template/.kiro/hooks/`（別スペックで対応）
- `kiro-template/.kiro/settings/mcp.json`（別スペックで対応）
- `kiro-template/README.md`（別スペックで対応）

## 参照ドキュメント

- `docs/functional-design.md` - プロジェクトハーネス層のコンポーネント設計
- `docs/architecture.md` - `.steering/` のディレクトリ構造・各ファイルの必須要素
- `docs/development-guidelines.md` - スペックテンプレートの品質基準
- `kiro-template/.kiro/steering/process.md` - Kiro 向けプロセス定義（テンプレートの使い方が記載）
