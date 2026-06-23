# タスクリスト

## 🚨 タスク完全完了の原則

**このファイルの全タスクが完了するまで作業を継続すること**

### 必須ルール
- **全てのタスクを`[x]`にすること**
- 「時間の都合により別タスクとして実施予定」は禁止
- 「実装が複雑すぎるため後回し」は禁止
- 未完了タスク（`[ ]`）を残したまま作業を終了しない

---

## フェーズ1: AGENTS.md（文脈注入ファイル）

- [x] `codex-template/AGENTS.md` を作成する
  - [x] プロセス原則セクションを実装する（`kiro-template/.kiro/steering/process.md` からフロントマターを除いて移植）
    - [x] SDD フロー（Issue → スペック → 実装 → PR）が記載されている
    - [x] `.steering/YYYYMMDD-xxx/` の使い方が記載されている
    - [x] tasklist.md 管理ルール（全タスク完了の原則・スキップ禁止）が記載されている
    - [x] PR・リリースフローが記載されている
  - [x] プロダクト定義セクションを実装する（`kiro-template/.kiro/steering/product.md` をセクション形式に変換）
    - [x] プロダクト名・ビジョン・目的のプレースホルダーが含まれる
    - [x] `docs/` 配下ドキュメント一覧のプレースホルダーが含まれる
    - [x] `<!-- 例: ... -->` 形式の記入ガイドが含まれる
  - [x] 技術スタックセクションを実装する（`kiro-template/.kiro/steering/tech.md` をセクション形式に変換）
    - [x] 技術スタックのプレースホルダーが含まれる
    - [x] OS 別セットアップ手順のプレースホルダーが含まれる
    - [x] `<!-- 例: ... -->` 形式の記入ガイドが含まれる
  - [x] リポジトリ構造セクションを実装する（`kiro-template/.kiro/steering/structure.md` をセクション形式に変換）
    - [x] リポジトリ構造のプレースホルダーが含まれる
    - [x] `<!-- 例: ... -->` 形式の記入ガイドが含まれる
  - [x] ワークフローセクションを実装する（`kiro-template/.kiro/hooks/*.json` の内容を Markdown テキストに変換）
    - [x] `setup-project` ワークフローが記述されている
    - [x] `add-feature` ワークフローが記述されている
  - [x] Kiro 固有の構文（`inclusion:` フロントマター等）が含まれていないことを確認する

## フェーズ2: .devcontainer/

- [x] `codex-template/.devcontainer/devcontainer.json` を作成する
  - [x] ベースイメージに `mcr.microsoft.com/devcontainers/universal:2` を使用している
  - [x] GitHub CLI feature（`ghcr.io/devcontainers/features/github-cli:1`）が含まれる
  - [x] `~/.codex` を `/home/vscode/.codex` にマウントしている
  - [x] 技術スタック固有の features（AWS CLI 等）がコメントアウトのプレースホルダーになっている
  - [x] `postCreateCommand` が `bash .devcontainer/postCreate.sh` を指定している
- [x] `codex-template/.devcontainer/postCreate.sh` を作成する
  - [x] Codex CLI のインストール（`npm install -g @openai/codex`）が含まれる
  - [x] `codex --version` でバージョン確認が含まれる
  - [x] `gh --version` でバージョン確認が含まれる
  - [x] 技術スタック固有のセットアップがコメントアウトのプレースホルダーになっている

## フェーズ3: .steering/_template/

- [x] `codex-template/.steering/_template/requirements.md` を作成する
  - [x] `kiro-template/.steering/_template/requirements.md` を流用し、Codex 固有の差分があれば調整する
- [x] `codex-template/.steering/_template/design.md` を作成する
  - [x] `kiro-template/.steering/_template/design.md` を流用し、Codex 固有の差分があれば調整する
- [x] `codex-template/.steering/_template/tasklist.md` を作成する
  - [x] `kiro-template/.steering/_template/tasklist.md` を流用し、Codex 固有の差分があれば調整する

## フェーズ4: docs/ テンプレート（6ファイル）

- [x] `codex-template/docs/product-requirements.md` を作成する（プレースホルダー付きテンプレート）
- [x] `codex-template/docs/functional-design.md` を作成する（プレースホルダー付きテンプレート）
- [x] `codex-template/docs/architecture.md` を作成する（プレースホルダー付きテンプレート）
- [x] `codex-template/docs/repository-structure.md` を作成する（プレースホルダー付きテンプレート）
- [x] `codex-template/docs/development-guidelines.md` を作成する（プレースホルダー付きテンプレート）
- [x] `codex-template/docs/glossary.md` を作成する（プレースホルダー付きテンプレート）

## フェーズ5: README.md

- [x] `codex-template/README.md` を作成する
  - [x] テンプレートの概要・ハーネスの説明が含まれる
  - [x] クイックスタート（テンプレート複製 → AGENTS.md 記入 → 最初の機能実装）が記載されている
  - [x] Claude Code ハーネスからの移行対応表が含まれる
  - [x] 「できること・できないこと」（hooks・agents 非対応など）が記述されている
  - [x] devcontainer の使い方が記述されている

## フェーズ6: ONBOARDING.md

- [x] `codex-template/ONBOARDING.md` を作成する
  - [x] 前提条件（Codex CLI インストール・GitHub アカウント等）が記載されている
  - [x] devcontainer を使ったセットアップ手順が含まれる
  - [x] AGENTS.md への記入手順が含まれる
  - [x] SDD ワンサイクル（requirements → design → tasklist → 実装 → PR）の手順が含まれる

## フェーズ7: 品質チェック

- [x] ファイル構造が design.md のディレクトリ構造と一致していることを確認する
  - [x] `find codex-template -type f | sort` で全ファイルを確認
- [x] requirements.md の受け入れ条件をすべて確認する
  - [x] AGENTS.md: Codex 固有構文のみ（フロントマターなし）
  - [x] AGENTS.md: 5セクション（プロセス原則・プロダクト定義・技術スタック・リポジトリ構造・ワークフロー）
  - [x] .steering/_template/: 3ファイル存在
  - [x] docs/: 6ファイル存在・プレースホルダー付き
  - [x] README.md: クイックスタート・移行対応表・できること/できないこと含む
  - [x] ONBOARDING.md: セットアップ〜SDDワンサイクルまで含む
  - [x] .devcontainer/: devcontainer.json + postCreate.sh 存在

## フェーズ8: PR 作成

- [x] フィーチャーブランチを作成する（`feat/codex-template`）
- [x] 変更をコミットする
- [x] PR を作成する（Issue #26 に紐づける）→ PR #27
- [x] 実装後の振り返りを記録する（このファイルの下部）

## フェーズ9: 受け入れテスト（動作確認）

> **認証方式**: OpenAI API キーではなく、ChatGPT Pro サブスクリプション（ブラウザ OAuth）を使用する

- [x] ステップ1: テスト用リポジトリを作成する
  - [x] `codex-template/` の内容を新リポジトリ `platform-harness-for-codex` にコピーする
    → https://github.com/kanan4gh/platform-harness-for-codex
- [x] ステップ2: ホストマシンで Codex CLI を認証する（devcontainer 起動前に実施）
  - [x] ローカルマシンに Codex CLI をインストールする（`npm install -g @openai/codex`）
  - [x] `codex` を起動し、ChatGPT Pro アカウントでブラウザ認証を完了する
  - [x] 認証トークンが `~/.codex/` に保存されていることを確認する
- [x] ステップ3: VS Code で devcontainer を起動する（ここから再開）
  - [x] `platform-harness-for-codex/` を VS Code で開き「Reopen in Container」を選択する
    ```bash
    git clone https://github.com/kanan4gh/platform-harness-for-codex
    code platform-harness-for-codex
    ```
  - [x] `codex --version` でインストール確認する
  - [x] 認証状態が引き継がれていることを確認する（`~/.codex` マウント済みのため）
- [x] ステップ4: ONBOARDING.md の確認3つを実施する
  - [x] 確認1: 「このプロジェクトの開発プロセスのルールを教えてください」→ SDD フローが返ってくる
  - [x] 確認2: 「このプロジェクトのターゲットユーザーを教えてください」→ プレースホルダーへの言及または記入を促す応答が返ってくる
  - [x] 確認3: 「add-feature を実行してください」→ 機能名のヒアリングが始まる

---

## 実装後の振り返り

### 実装完了日
2026-06-11

### 計画と実績の差分

**計画と異なった点**:
- `.devcontainer/` の追加はステアリング作成中にユーザーから指摘を受けて追加。設計時点では含まれていなかったが、Kiro との一貫性（CLIツール = devcontainer有効）の観点から妥当な追加だった

**新たに必要になったタスク**:
- `.devcontainer/` コンポーネントの設計・実装（design.md への追記、tasklist.md への追加）

### 学んだこと

**技術的な学び**:
- Kiro と Codex の最大の差異は「文脈注入の粒度」。Kiro は inclusion モードで always/auto/manual を使い分けられるが、Codex は AGENTS.md を常時読み込むだけ。この制約を「1ファイルのセクション構造」で解決した
- Kiro の hooks（JSON トリガー）に相当するワークフローは、AGENTS.md のワークフローセクションに Markdown テキストとして記述することで代替できる。ツールの制約を正直に示しつつ、最大限の代替を提供するアプローチが有効

**プロセス上の改善点**:
- ステアリング作成段階で「devcontainer はどうするか」を確認できたのは良かった。設計フェーズで漏れを発見するのが最もコストが低い

### 次回への改善提案
- Codex CLI での実際の動作確認（受け入れテスト）を別タスクとして計画する
- PRD の更新（リポジトリの実態：Claude Code ハーネス本体 + Kiro/Codex テンプレート展開）を別タスクとして計画する
- publish-template.yml への Codex テンプレートリリース追加も別タスクで対応する

### リリース判断

**前提条件の確認**:
- [x] ファイル構造確認済み
- [x] 受け入れ条件確認済み
- [x] リリースノートに記載すべき変更内容が整理されている

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes |
| 未解決の重大バグはないか | なし |
| 適切なバージョン種別 | MINOR |

**提案**:
PR #27 マージ後、`v0.4.0` へのバージョンアップを提案。理由: Codex CLI 向けテンプレートという新機能追加のため MINOR バージョンアップが適切。
