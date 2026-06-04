# 要求内容

## 概要

`kiro-template/` の内容を GitHub Actions で `platform-harness-for-kiro` リポジトリに自動発行する仕組みを実装する。

## 背景

Kiro ハーネスはこの作業場リポジトリ（`platform-harness-for-kiro`、後に `platform-harness-engineering` にリネーム）で開発・育成している。Kiro ユーザーに配布するためのクリーンなテンプレートリポジトリ（`platform-harness-for-kiro`）に、自動的に内容を発行する仕組みが必要。

将来 Codex 向けハーネス（`codex-template/`）が追加されても同じワークフローで対応できる拡張可能な設計にする。

## ユースケースの軸

> **開発者がリリースを作成すると、`kiro-template/` の内容が自動的に `platform-harness-for-kiro` リポジトリへ発行される。**

## 実装対象の機能

### 1. リポジトリのリネーム

- このリポジトリを `platform-harness-for-kiro` から `platform-harness-engineering` にリネーム
- 作業場であることを名前で明示する

### 2. 出力リポジトリの作成

- `platform-harness-for-kiro` を新規作成（Kiro ユーザーが "Use this template" で複製する先）
- 初回は `kiro-template/` の内容で初期化する

### 3. GitHub Actions 自動発行ワークフロー

- `platform-harness-engineering` に `.github/workflows/publish-template.yml` を実装
- トリガー: `release published` + `workflow_dispatch`（手動実行）
- 認証: PAT（Personal Access Token）を GitHub Secret に登録
- `kiro-template/` の内容を `platform-harness-for-kiro` リポジトリのルートに push する
- 将来の `codex-template/` にも対応できるパラメータ化設計

## 受け入れ条件

### リポジトリリネーム
- [ ] このリポジトリが `platform-harness-engineering` という名前になっている
- [ ] 既存の git remote / gh コマンドが新リポジトリ名で動作する

### 出力リポジトリ
- [ ] `platform-harness-for-kiro` リポジトリが存在する
- [ ] Template repository として設定されている
- [ ] `kiro-template/` の内容（`.kiro/`, `ONBOARDING.md`, `README.md`）が含まれている

### 自動発行ワークフロー
- [ ] `workflow_dispatch` で手動実行でき、`platform-harness-for-kiro` に最新内容が反映される
- [ ] `gh release create` 後にワークフローが自動実行される
- [ ] ワークフローが成功・失敗を適切に報告する

## スコープ外

- `codex-template/` の実装（将来の別タスク）
- ワークフローのテスト自動化

## 参照ドキュメント

- GitHub Issue: https://github.com/kanan4gh/platform-harness-for-kiro/issues/17
- `docs/ideas/harness-engineering.md` - ハーネス設計の背景
