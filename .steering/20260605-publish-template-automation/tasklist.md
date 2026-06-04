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

- [ ] `workflow_dispatch` で手動実行し、`platform-harness-for-kiro` に内容が反映されることを確認する
  - [ ] `.kiro/` ディレクトリが含まれていることを確認する
  - [ ] `ONBOARDING.md`、`README.md` が含まれていることを確認する
- [ ] `gh release create` でリリースを作成し、ワークフローが自動実行されることを確認する

## フェーズ4: ドキュメント更新

- [ ] `docs/repository-structure.md` を更新する（新リポジトリ名・出力リポジトリを反映）
- [ ] `README.md` を更新する（リポジトリリネームを反映）
- [ ] 実装後の振り返りをこのファイルの下部に記録する

---

## 実装後の振り返り

### 実装完了日
{YYYY-MM-DD}

### 計画と実績の差分

**計画と異なった点**:
-

**新たに必要になったタスク**:
-

### 学んだこと

**技術的な学び**:
-

**プロセス上の改善点**:
-

### 次回への改善提案
-

### リリース判断

**前提条件の確認**:
- [ ] 全テスト通過（該当なし）
- [ ] ワークフロー動作確認済み
- [ ] リリースノートに記載すべき変更内容が整理されている

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | {Yes / No / 保留} |
| 未解決の重大バグはないか | {なし / あり: 内容} |
| 適切なバージョン種別 | {MAJOR / MINOR / PATCH / リリース不要} |

**提案**:
{リリース判断を記載}
