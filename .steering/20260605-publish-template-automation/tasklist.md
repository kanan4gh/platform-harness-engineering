# タスクリスト

## 🚨 タスク完全完了の原則

**このファイルの全タスクが完了するまで作業を継続すること**

---

## フェーズ1: リポジトリのセットアップ

- [x] このリポジトリを `platform-harness-engineering` にリネームする
  - [x] GitHub Settings → リポジトリ名を変更する
  - [x] ローカルの git remote を更新する（`git remote set-url origin`）
- [x] `platform-harness-for-kiro` 出力リポジトリを新規作成する
  - [x] `gh repo create` で作成する（Template repository として設定）
  - [x] README.md を初期コミットで追加する
- [x] PAT（Personal Access Token）を発行して Secret に登録する
  - [x] GitHub で Fine-grained PAT を発行する（`platform-harness-for-kiro` への Contents write 権限）
  - [x] `platform-harness-engineering` の Secrets に `PUBLISH_PAT` として登録する

## フェーズ2: ワークフローの実装

- [x] `.github/workflows/publish-template.yml` を作成する
  - [x] `release: types: [published]` トリガーを設定する
  - [x] `workflow_dispatch`（`template` 入力パラメータ付き）トリガーを設定する
  - [x] `kiro-template/` の内容を出力リポジトリに push するジョブを実装する
  - [x] PUBLISH_PAT を使った clone / push を実装する

## フェーズ3: 動作確認

- [x] `workflow_dispatch` で手動実行し、`platform-harness-for-kiro` に内容が反映されることを確認する
  - [x] `.kiro/` ディレクトリが含まれていることを確認する
  - [x] `ONBOARDING.md`、`README.md` が含まれていることを確認する
- [x] `gh release create` でリリースを作成し、ワークフローが自動実行されることを確認する

## フェーズ4: ドキュメント更新

- [x] `docs/repository-structure.md` を更新する（新リポジトリ名・出力リポジトリを反映）
- [x] `README.md` を更新する（リポジトリリネームを反映）
- [x] 実装後の振り返りをこのファイルの下部に記録する

---

## 実装後の振り返り

### 実装完了日
2026-06-05

### 計画と実績の差分

**計画と異なった点**:
- 特になし。設計通りに実装完了。

**新たに必要になったタスク**:
- `platform-harness-for-kiro` を Template repository に設定する（tasklist には明記されていなかった）

### 学んだこと

**技術的な学び**:
- GitHub API 経由（`gh api --method PUT`）で空リポジトリへの初期コミットが可能。clone 不要でシンプル。
- `rsync --delete` により、出力リポジトリから不要ファイルが消えることを確認。ドットディレクトリ（`.kiro/`）も確実にコピーされる。
- リリーストリガー（`release: types: [published]`）は `gh release create` 直後に自動起動することを確認。

**プロセス上の改善点**:
- 出力リポジトリの「Template repository 設定」はフェーズ1のタスクに最初から含めるべきだった。

### 次回への改善提案
- `codex-template/` 追加時は同じワークフローで対応できるので、新規ステアリングは不要。`template` パラメータを `codex` に変えるだけ。

### リリース判断

**前提条件の確認**:
- [x] 全テスト通過（該当なし）
- [x] ワークフロー動作確認済み（workflow_dispatch・release トリガー両方成功）
- [x] リリースノートに記載すべき変更内容が整理されている

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes |
| 未解決の重大バグはないか | なし |
| 適切なバージョン種別 | リリース不要（v0.3.0 として既にリリース済み） |

**提案**:
v0.3.0 としてリリース済み。今回のタスクはすべて完了。
