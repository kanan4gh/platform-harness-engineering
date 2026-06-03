---
inclusion: always
---

# 技術スタック・環境設定

## 技術スタック

<!-- 例:
- 言語: Python 3.12
- パッケージマネージャー: uv
- テスト: pytest
- 型チェック: basedpyright
- リンター: ruff
-->
[言語・フレームワーク・主要ライブラリ・ツールを記入]

## バージョン管理

<!-- プロジェクトで使用するバージョン固定ファイルを記入してください -->
<!-- 例: .python-version（Python バージョン固定）、.nvmrc（Node.js バージョン固定）、.tool-versions（asdf 用） -->

バージョン固定ファイル: [使用するファイルを記入（例: `.python-version`）]

## セットアップ手順

### macOS

```bash
# 例: Python のインストール（pyenv を使用）
# brew install pyenv
# pyenv install 3.12
# pyenv local 3.12
```

<!-- macOS 向けのセットアップ手順を記入 -->

### Windows

<!-- Windows 向けのセットアップ手順を記入 -->
<!-- PowerShell や winget を使った手順を記載 -->

### Linux

<!-- Linux 向けのセットアップ手順を記入 -->
<!-- apt / yum / dnf 等を使った手順を記載 -->

## 依存関係のインストール

```bash
# 例（プロジェクトのパッケージマネージャーに応じて変更）
# uv sync      # Python (uv)
# npm install  # Node.js
```

<!-- 依存関係のインストールコマンドを記入 -->

## 主要コマンド

```bash
# 例（プロジェクトに応じて変更）
# uv run pytest           # テスト実行
# uv run ruff check .     # リント
# uv run basedpyright     # 型チェック
```

<!-- ビルド・テスト・リント・型チェック等の主要コマンドを記入 -->
