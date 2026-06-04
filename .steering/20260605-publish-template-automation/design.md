# 設計書

## アーキテクチャ概要

GitHub Actions ワークフローが `kiro-template/` の内容を出力リポジトリへ push するシンプルな発行パイプライン。

```
platform-harness-engineering（この作業場）
├── kiro-template/         ← 発行元
│   ├── .kiro/
│   ├── ONBOARDING.md
│   └── README.md
└── .github/workflows/
    └── publish-template.yml

        ↓ release published / workflow_dispatch

platform-harness-for-kiro（出力リポジトリ）
├── .kiro/
├── ONBOARDING.md
└── README.md
```

## コンポーネント設計

### 1. publish-template.yml

**責務**:
- `kiro-template/` の内容を `platform-harness-for-kiro` の main ブランチに push する
- トリガー: `release: types: [published]` と `workflow_dispatch`
- `workflow_dispatch` には `template` 入力パラメータを持たせ将来拡張に対応

**実装の要点**:
- `PUBLISH_PAT` Secret（Personal Access Token）で出力リポジトリに書き込む
- `git subtree` ではなく、出力リポジトリを checkout して `rsync` または `cp` でファイルをコピーし push する方式を採用
- `.kiro/` 等のドットディレクトリも確実にコピーする

### 2. PAT（Personal Access Token）

**責務**:
- ワークフローが `platform-harness-for-kiro` リポジトリへ push するための認証

**実装の要点**:
- Fine-grained PAT（特定リポジトリのみ書き込み権限）を推奨
- `platform-harness-engineering` リポジトリの Secrets に `PUBLISH_PAT` として登録

## データフロー

### release published / workflow_dispatch トリガー時
```
1. ワークフロー起動
2. platform-harness-engineering リポジトリを checkout（kiro-template/ が取得される）
3. platform-harness-for-kiro リポジトリを別ディレクトリに clone（PUBLISH_PAT 使用）
4. kiro-template/ の内容を platform-harness-for-kiro の作業ディレクトリにコピー
5. 変更を commit & push（コミットメッセージにリリースタグを含める）
```

## ワークフロー概要

```yaml
on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      template:
        description: 'Template name to publish (e.g. kiro, codex)'
        default: 'kiro'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - checkout this repo
      - clone output repo with PAT
      - rsync kiro-template/ → output repo root
      - commit & push to output repo
```

## 将来の拡張性

`workflow_dispatch` の `template` 入力を `kiro` → `codex` に変えるだけで `codex-template/` を `platform-harness-for-codex` に発行できる設計にする。

## セキュリティ考慮事項

- PAT は Fine-grained で出力リポジトリへの write 権限のみ付与
- PAT は GitHub Secrets に保存し、ワークフロー以外からアクセス不可

## ディレクトリ構造（変更後）

```
platform-harness-engineering/（リネーム後）
├── .github/
│   └── workflows/
│       └── publish-template.yml  ← 新規追加
├── .steering/
├── docs/
├── kiro-template/
│   ├── .kiro/
│   ├── ONBOARDING.md
│   └── README.md
└── CLAUDE.md
```

## 実装の順序

1. GitHub でこのリポジトリを `platform-harness-engineering` にリネーム
2. `platform-harness-for-kiro` 出力リポジトリを新規作成
3. PAT を発行し `PUBLISH_PAT` Secret に登録
4. `publish-template.yml` を実装
5. `workflow_dispatch` で手動テスト
6. 動作確認
