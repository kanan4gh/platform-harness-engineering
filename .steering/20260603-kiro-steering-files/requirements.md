# 要求内容

## 概要

Kiro IDE のエージェントコンテキストに常時注入される4つの steering ファイルを実装する。`.kiro/steering/` 配下に `process.md`・`product.md`・`tech.md`・`structure.md` をテンプレートとして作成する。

## 背景

このリポジトリは Kiro 向けのハーネステンプレートである。ハーネスの最重要コンポーネントである「文脈層」（`.kiro/steering/`）が存在しないと、Kiro エージェントはプロジェクト固有の方針・制約・構造を知らないまま動作することになる。

Claude CLI における `CLAUDE.md` の役割を Kiro の steering ファイルに移植することで、Kiro ユーザーが複製したリポジトリで即座に SDD（スペック駆動開発）を開始できるようになる。

## 関連 Issue

https://github.com/kanan4gh/platform-harness-for-kiro/issues/1

## ユースケースの軸

Kiro でこのテンプレートを複製したユーザーが、`.kiro/steering/` の4ファイルに自プロジェクト情報を記入するだけで、Kiro エージェントがプロジェクトの方針・技術スタック・構造を理解した状態で開発を支援できるようになる。

## 実装対象の機能

### 1. process.md（開発プロセス原則）

- SDD の基本フロー・ルールを定義するファイル
- ハーネス共通のため、テンプレートを複製したプロジェクトは原則として直接編集しない
- `inclusion: always` で常時コンテキストに注入

### 2. product.md（プロダクト定義）

- プロダクト概要・目的・`docs/` 一覧を記入するファイル
- プロジェクト開始時に必ず記入する必須ファイル
- `inclusion: always` で常時コンテキストに注入

### 3. tech.md（技術スタック・環境設定）

- 技術スタック・OS 別セットアップ手順を記入するファイル
- devcontainer の代替として、バージョン固定ファイルと OS 別手順を含むプレースホルダーを提供
- `inclusion: always` で常時コンテキストに注入

### 4. structure.md（リポジトリ構造）

- リポジトリ構造の要約（`docs/repository-structure.md` の簡略版）を記入するファイル
- プロジェクト開始時に必ず更新する
- `inclusion: always` で常時コンテキストに注入

## 受け入れ条件

### process.md

- [ ] `inclusion: always` フロントマターが設定されている
- [ ] SDD の基本フロー（ドキュメント → スペック → 実装 → 検証 → 更新）が記載されている
- [ ] `.steering/YYYYMMDD-xxx/` の使い方が記載されている
- [ ] kiro-cli 不使用・built-in specs 不使用の方針が記載されている
- [ ] プロジェクト固有の値を含まない（ハーネス共通のため記入ガイド不要）

### product.md

- [ ] `inclusion: always` フロントマターが設定されている
- [ ] プロダクト名・ビジョン・目的のプレースホルダーが含まれている
- [ ] `docs/` 配下のドキュメント一覧のプレースホルダーが含まれている
- [ ] `<!-- 例: ... -->` 形式の記入ガイドが含まれている

### tech.md

- [ ] `inclusion: always` フロントマターが設定されている
- [ ] 技術スタックのプレースホルダーが含まれている
- [ ] macOS・Windows・Linux それぞれのセットアップ手順プレースホルダーが含まれている
- [ ] バージョン固定ファイル（`.python-version`・`.nvmrc`・`.tool-versions` 等）への言及がある
- [ ] `<!-- 例: ... -->` 形式の記入ガイドが含まれている

### structure.md

- [ ] `inclusion: always` フロントマターが設定されている
- [ ] リポジトリ構造のプレースホルダーが含まれている
- [ ] `<!-- 例: ... -->` 形式の記入ガイドが含まれている

## 成功指標

- テンプレートを複製した Kiro ユーザーが、4ファイルに記入するだけで Kiro エージェントへのコンテキスト注入が完了する
- `docs/development-guidelines.md` の「Steering ファイルの品質基準」を全て満たすこと

## スコープ外

以下はこのフェーズでは実装しない:

- `.kiro/hooks/` 配下のフックファイル（別スペックで対応）
- `.kiro/settings/mcp.json`（別スペックで対応）
- `.steering/_template/` 配下のスペックテンプレート（別スペックで対応）
- `README.md`（別スペックで対応）

## 参照ドキュメント

- `docs/product-requirements.md` - プロダクト要求定義書
- `docs/functional-design.md` - 機能設計書（設計指針1〜3、コンポーネント設計）
- `docs/architecture.md` - アーキテクチャ設計書（steering ファイル設計、環境設定戦略）
- `docs/repository-structure.md` - リポジトリ構造定義書
