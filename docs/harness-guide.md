# platform-harness-engineering について

Kiro ハーネス（[platform-harness-for-kiro](https://github.com/kanan4gh/platform-harness-for-kiro)）を設計・開発・発行するための作業場リポジトリです。

## このリポジトリについて

Claude Code を使ってスペック駆動開発（SDD）で Kiro ハーネスを育てるための環境です。

```
kiro-template/         ← ここを育てる
       ↓ gh release create
platform-harness-for-kiro  ← Kiro ユーザーが "Use this template" で使う
```

## 開発フロー

```
1. GitHub Issue を作成
2. /add-feature で機能実装（ステアリングファイル → 実装 → PR）
3. PR をマージ
4. gh release create でリリース（kiro-template/ が自動発行される）
```

詳細は `CLAUDE.md` を参照してください。

## 関連リポジトリ

| リポジトリ | 用途 |
|-----------|------|
| [platform-harness-engineering](https://github.com/kanan4gh/platform-harness-engineering)（本リポジトリ） | 作業場・開発環境 |
| [platform-harness-for-kiro](https://github.com/kanan4gh/platform-harness-for-kiro) | Kiro ユーザー向け配布テンプレート |

## 内部Kiroユーザー向け

このリポジトリ自体を Kiro で開いてハーネス改善作業をする方は [ONBOARDING.md](kiro-template/ONBOARDING.md) を参照してください（GHE へのデプロイ手順も記載）。
