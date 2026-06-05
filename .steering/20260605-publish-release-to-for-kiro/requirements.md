# 要求内容

## 概要

publish-template ワークフローに、platform-harness-for-kiro への GitHub Release 作成ステップを追加する。

## 背景

現在のワークフローは kiro-template のコンテンツを platform-harness-for-kiro の main ブランチに push するのみ。GitHub Release が作成されないため、Kiro ユーザーが ONBOARDING.md に記載の Releases ページから zip をダウンロードできない状態になっている。

関連 Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/20

## ユースケースの軸

> platform-harness-engineering で新しいバージョンをリリースすると、platform-harness-for-kiro にも同バージョンの GitHub Release が自動作成され、Kiro ユーザーが Releases ページから最新 zip をダウンロードできる。

## 実装対象の機能

### 1. publish-template.yml へのリリース作成ステップ追加

- コンテンツ push 後、`gh release create` で platform-harness-for-kiro に Release を作成する
- タグ・タイトルは本リポジトリと同一（例: `v0.3.2`）
- リリースノートはシンプルな定型文でよい（詳細は本リポジトリ側に記載のため）
- `workflow_dispatch` 手動実行時はリリース作成をスキップする（タグが存在しないため）
- コンテンツに差分がなくスキップされた場合もリリース作成をスキップする

## 受け入れ条件

- [ ] release イベント時に platform-harness-for-kiro に同バージョンの GitHub Release が作成される
- [ ] workflow_dispatch 手動実行時はリリース作成がスキップされる
- [ ] コンテンツ差分なしでスキップされた場合もリリース作成がスキップされる
- [ ] PUBLISH_PAT に `repo` スコープがあれば追加権限不要（gh CLI は同トークンを使用）

## スコープ外

- リリースノートの自動生成・差分サマリ
- platform-harness-for-kiro 以外のテンプレートへの対応

## 参照ドキュメント

- `.github/workflows/publish-template.yml` — 修正対象
