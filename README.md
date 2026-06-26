# platform-harness-engineering

[platform-harness](https://github.com/kanan4gh/platform-harness)（Claude Code 向け本家ハーネス）から派生した作業場リポジトリです。Kiro・Codex など各 AI ツール向けのプラットフォームハーネスを設計・開発・発行します。

## リポジトリの位置づけ

```
platform-harness          ← 本家（Claude Code 向け・すべての元）
       ↓ upstream sync
platform-harness-engineering（本リポジトリ・ジェネレーター専用）
       ├── kiro-template/   → platform-harness-for-kiro（Kiro ユーザーが使う）
       └── codex-template/  → platform-harness-for-codex（Codex ユーザーが使う）
```

### 改善の責務分担

| リポジトリ | 改善の方針 |
|-----------|-----------|
| `platform-harness` | ハーネスのコアな改善はすべてここで行う |
| `platform-harness-engineering` | 固有の改善は行わない。本家の改善を取り込み、各ツール向けに展開するだけ |
| `platform-harness-for-kiro` | Kiro 固有の改善のみ。本家への環流は行わない |
| `platform-harness-for-codex` | Codex 固有の改善のみ。本家への環流は行わない |

## ハーネスとは何か

> **「エンジンを動かすために必要な、エンジン以外のすべて」**

AI 駆動開発において、LLM（Claude）がエンジンだとすれば、ハーネスは LLM を有効に動かすすべての仕組みです。

| 要素 | 具体例 | 役割 |
|------|--------|------|
| **文脈の注入** | CLAUDE.md、requirements.md | LLM が何をすべきかを定義する |
| **プロセスの型** | steering スキル、tasklist.md | 作業手順を強制する |
| **記憶** | memory/ | セッションをまたぐ一貫性を保つ |
| **検証** | テスト、リンター | 出力の品質を保証する |
| **ツール** | MCP サーバー | LLM の手の届く範囲を広げる |

## 開発フロー

### ハーネスの改善（本家起点）

ハーネスのコアな改善は [platform-harness](https://github.com/kanan4gh/platform-harness)（Claude Code 向け本家）で行います。

```
1. platform-harness で改善・PR・マージ
2. 本リポジトリに改善を取り込む（CLAUDE.md・skills 等を同期）
3. Kiro・Codex 向けに展開（各テンプレートに反映）
4. gh release create でリリース
```

本家の変更を検知するには upstream remote を使います：

```bash
# 初回セットアップ（clone 直後に一度だけ実行）
git remote add upstream https://github.com/kanan4gh/platform-harness.git

# 本家の変更を確認する
git fetch upstream
git log upstream/main..main --oneline   # 本家が先行しているコミット
git diff upstream/main -- CLAUDE.md     # 特定ファイルの差分確認
```

### 各テンプレートの個別改善

Kiro・Codex 固有の変更は本リポジトリで直接行います。

```
1. GitHub Issue を作成
2. /add-feature で機能実装（ステアリングファイル → 実装 → PR）
3. PR をマージ
4. gh release create でリリース（各テンプレートが自動発行される）
```

詳細は `CLAUDE.md` を参照してください。

## 関連リポジトリ

| リポジトリ | 用途 |
|-----------|------|
| [platform-harness](https://github.com/kanan4gh/platform-harness) | 本家・Claude Code 向けハーネス |
| [platform-harness-engineering](https://github.com/kanan4gh/platform-harness-engineering)（本リポジトリ） | 作業場・開発環境 |
| [platform-harness-for-kiro](https://github.com/kanan4gh/platform-harness-for-kiro) | Kiro ユーザー向け配布テンプレート |
| [platform-harness-for-codex](https://github.com/kanan4gh/platform-harness-for-codex) | Codex ユーザー向け配布テンプレート |

## 内部Kiroユーザー向け

このリポジトリ自体を Kiro で開いてハーネス改善作業をする方は [ONBOARDING.md](kiro-template/ONBOARDING.md) を参照してください（GHE へのデプロイ手順も記載）。
