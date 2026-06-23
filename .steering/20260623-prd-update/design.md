# 設計書

## アプローチ

`docs/product-requirements.md` を書き直す。ゼロから書き直すのではなく、既存の構造を活かしながら以下の観点で修正・加筆する。

## 変更箇所の設計

### 1. プロダクト概要セクション

**変更前**:
- プロダクト名: `platform-harness-for-kiro`
- コンセプト: Claude CLI ハーネスを Kiro に移植する
- ビジョン: Kiro ユーザー向け

**変更後**:
- プロダクト名: `platform-harness-engineering`
- コンセプト: 複数の AI ツール（Kiro / Codex CLI 等）向けハーネステンプレートを設計・管理・配布するプラットフォーム
- ビジョン: どの AI ツールを使うエンジニアでも、SDD（スペック駆動開発）ハーネスを即座に使い始められるようにする

### 2. ターゲットユーザーセクション

**変更点**:
- プライマリーペルソナを「Claude CLI ハーネス経験者」から「SDD ハーネスを整備・運用したいエンジニア」に拡張
- セカンダリーペルソナを「使用ツールを問わず SDD を始めたい新規ユーザー」に変更

### 3. 機能要件セクション

**構造**:

```
コア機能（MVP）
  ├── Kiro テンプレート（既存・整理）
  ├── Codex CLI テンプレート（新規追加）
  └── テンプレート配布自動化（新規追加）

将来的な機能（Post-MVP）
  ├── 新ツール向けテンプレートの追加プロセス（新規）
  └── 既存 Post-MVP 項目の見直し
```

**Codex CLI テンプレート要件（新規）**:
- `codex-template/` 配下に AGENTS.md・.devcontainer/・.steering/_template/・docs/ が存在する
- SDD フロー（setup-project / add-feature）のワークフローが AGENTS.md に記述されている
- devcontainer で Codex CLI + GitHub CLI がセットアップされている

**テンプレート配布自動化要件（新規）**:
- GitHub Actions ワークフローで各テンプレートを対応リポジトリに自動配布できる
- 配布先: `platform-harness-for-kiro`、`platform-harness-for-codex`

### 4. 将来的な機能セクション

追加:
- **新ツール向けテンプレートの追加プロセス**: 新しい AI ツールが登場したとき、`{tool}-template/` を追加し publish ワークフローを拡張する標準プロセスを定義する

## ディレクトリ構造（変更なし）

```
docs/
  product-requirements.md  ← このタスクで更新
```

## 実装の順序

1. プロダクト概要・ビジョンを書き直す
2. ターゲットユーザーを更新する
3. 機能要件に Codex テンプレートを追加する
4. 機能要件にテンプレート配布自動化を追加する
5. 将来的な機能を更新する
6. 成功指標・非機能要件・スコープ外を見直す
