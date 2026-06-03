# 要求内容

## 概要

`docs/repository-structure.md` を Bootstrap フェーズの実際のリポジトリ構造に合わせて更新する。`kiro-template/` フォルダの導入と Claude Code 開発インフラの共存を正確に文書化する。

## 関連 Issue

https://github.com/kanan4gh/platform-harness-for-kiro/issues/4

## ユースケースの軸

このリポジトリの開発者（Bootstrap フェーズで作業するエンジニア）が `docs/repository-structure.md` を読んで、リポジトリの2層構造（Claude Code 開発インフラ／Kiro テンプレート成果物）を正確に把握できる。

## 実装対象の機能

### 1. Bootstrap フェーズのリポジトリ全体構造を追加

現在の `docs/repository-structure.md` は「テンプレートの完成形」（Kiro ユーザーが使う構造）のみを記述しているが、**このリポジトリ自体の実際の構造**（Bootstrap フェーズ）を先頭に追加する。

実際の構造:
- `kiro-template/` — Kiro テンプレート成果物
- `.claude/` — Claude Code 開発インフラ（スキル・コマンド・エージェント定義）
- `CLAUDE.md` — Claude Code 設定
- `.steering/YYYYMMDD-xxx/` — Claude Code 作業スペック（作業履歴）
- `docs/` — このプロジェクトの永続ドキュメント
- `.devcontainer/` — Claude Code 開発環境（Kiro テンプレートには含まれない）

### 2. kiro-template/ の内容説明を追加

`kiro-template/` フォルダが「Kiro ユーザーに展開される成果物」であることを明記し、その中身の構造を既存の「完成形」記述と結びつける。

### 3. 既存セクションの整合性更新

既存の「プロジェクト構造（完成形）」ツリーと各ディレクトリ詳細セクションのパスを `kiro-template/` 配下に修正する。

## 受け入れ条件

- [ ] Bootstrap フェーズのリポジトリ全体構造ツリーが記載されている
- [ ] `kiro-template/` が「Kiro テンプレートの成果物フォルダ」として説明されている
- [ ] `.devcontainer/` が「Claude Code 開発環境用（Kiro テンプレートには含まれない）」と明記されている
- [ ] 既存の「完成形」ツリーのパスが `kiro-template/` 配下を反映している
- [ ] 「テンプレートとしての使い方」セクションのカスタマイズ対象パスが更新されている

## スコープ外

- `docs/architecture.md` の更新（構造変更への言及は architecture.md にも必要だが別作業とする）
- `kiro-template/` の `docs/` 配下ドキュメントテンプレートの作成

## 参照ドキュメント

- `docs/repository-structure.md` — 更新対象
- `docs/architecture.md` — ブートストラップ戦略（フェーズ定義の参照元）
- `memory/project_output_folder.md` — kiro-template/ 導入の経緯
