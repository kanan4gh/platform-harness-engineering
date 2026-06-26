# 設計書

## アーキテクチャ概要

ファイル操作のみ。コードの変更なし。

```
README.md          現在の内容 → プレースホルダーに差し替え
docs/harness-guide.md  新規作成（現在のREADME内容を移動）
```

## コンポーネント設計

### 1. docs/harness-guide.md（新規）

**責務**:
- このハーネス（platform-harness-engineering）の説明を保持する
- 開発フロー・関連リポジトリ・内部向け情報を記録する

**内容**:
- 現在の README.md の内容をそのままコピー
- タイトルを「platform-harness-engineering について」等に変更

### 2. README.md（差し替え）

**責務**:
- テンプレート利用者が自分のプロジェクト用に育てる起点
- ハーネスガイドへのリンクを提供する

**内容（最小構成）**:
```markdown
# [Project Name]

プロジェクトの説明をここに書いてください。

---

このリポジトリは platform-harness を使用しています。
ハーネスの使い方: [docs/harness-guide.md](docs/harness-guide.md)
```

## 実装の順序

1. 現在の README.md の内容を `docs/harness-guide.md` として作成
2. README.md をプレースホルダーに差し替え

## ディレクトリ構造

```
docs/
  harness-guide.md   ← 新規（現在のREADME内容）
README.md            ← 差し替え（プレースホルダー）
```
