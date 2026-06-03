# 要求内容

## 概要

`kiro-template/` の残り3ファイル（`hooks/tasklist-check.json`・`settings/mcp.json`・`README.md`）を実装してテンプレートを完成させる。

## 関連 Issue

https://github.com/kanan4gh/platform-harness-for-kiro/issues/3

## ユースケースの軸

テンプレートを複製した Kiro ユーザーが、README.md を読むだけでプロジェクトをセットアップでき、hooks による自動化と MCP 設定の拡張基盤を即座に利用できるようになる。

## 実装対象の機能

### 1. tasklist-check.json（自動化フック）

- `tasklist.md` が保存された時に Kiro エージェントへ未完了タスクの確認を促す指示を送る
- kiro-cli を必要としない（エージェントへのプロンプト注入のみ）

### 2. mcp.json（MCP 設定ひな型）

- プロジェクト固有の MCP サーバーを追加できる空のひな型
- コメントでプラットフォーム共通 MCP はグローバル設定で管理する旨を示す

### 3. README.md（セットアップガイド）

- GUI 操作のみで完結するセットアップ手順（kiro-cli コマンドを一切含まない）
- ブートストラップ・リリース・自走フェーズの説明
- 必須カスタマイズ項目（product.md・tech.md・structure.md）の案内

## 受け入れ条件

### tasklist-check.json

- [ ] Kiro hooks の JSON 形式で記述されている
- [ ] `tasklist.md` の保存をトリガーとしている
- [ ] エージェントへの指示（prompt）が含まれている
- [ ] kiro-cli を必要とするコマンドが含まれていない

### mcp.json

- [ ] 有効な JSON 形式である
- [ ] プロジェクト固有 MCP サーバーを追加できる構造になっている
- [ ] コメント（または説明テキスト）でグローバル設定との使い分けが示されている

### README.md

- [ ] "Use this template" でのリポジトリ複製手順が記載されている
- [ ] steering ファイルのカスタマイズ手順が GUI 操作で完結している
- [ ] kiro-cli のコマンドが含まれていない
- [ ] ブートストラップ・リリース・自走フェーズの説明が含まれている
- [ ] `docs/architecture.md` のドキュメント品質チェックリスト項目を満たしている

## スコープ外

- `kiro-template/docs/` 配下のドキュメントプレースホルダー（初回リリース時点では不要と判断）
- Kiro フックの詳細な動作テスト（Kiro 実環境での受け入れテストで確認）

## 参照ドキュメント

- `docs/functional-design.md` — 設計指針1〜3、ワークフロー設計（フロー1: 新規プロジェクトセットアップ）
- `docs/architecture.md` — 自動化層・ブートストラップ戦略・受け入れテスト・ドキュメント品質チェックリスト
- `docs/development-guidelines.md` — フックファイル品質基準・初回リリースの条件
