# タスクリスト

## 🚨 タスク完全完了の原則

**このファイルの全タスクが完了するまで作業を継続すること**

### 必須ルール
- **全てのタスクを`[x]`にすること**
- **完了マークは操作の実行後に付けること**(実行予定の段階で付けない)
- 「時間の都合により別タスクとして実施予定」は禁止
- 未完了タスク（`[ ]`）を残したまま作業を終了しない

### タスクスキップが許可される唯一のケース
技術的理由(実装方針変更・アーキテクチャ変更・依存関係変更)のみ:
```
- [x] ~~タスク名~~（実装方針変更により不要: 具体的な技術的理由）
```

---

## フェーズ1: ワークフローの実装

- [x] `determine-templates` ジョブを追加する(`*-template/` 走査・JSON配列出力・0件時は失敗)
- [x] `publish` ジョブをmatrix化する(`needs` + `fail-fast: false` + `matrix.template` 参照への置換)
- [x] `workflow_dispatch` の `template` 入力を更新する(既定値 `all`・description更新)
- [x] 配布先リリース作成ステップに既存タグのスキップ判定を追加する(再実行時の安全性)

## フェーズ2: ドキュメント整合

- [x] `docs/` に配布フロー(リリース時kiroのみ等)の記述がないかgrepで確認し、あれば更新する
  - **記録**: 「リリース時kiroのみ」という記述はdocsに存在しなかった(PRDの受け入れ条件L93「Codexが自動配布される」はむしろ今回の変更で実態が追いついた項目)。Post-MVP節L117の「publishワークフローを拡張できるようにする」を、動的導出により拡張不要になった旨に更新した

## フェーズ3: 検証(4段)

- [x] 段1: 静的検証
  - [x] ワークフローYAMLがパース可能である(jobs: determine-templates/publish、dispatch既定=all、fail-fast=false を確認)
  - [x] matrix導出ロジックをローカル実行し `["kiro","codex"]` が得られる(bashで3ケース検証: 全件`["codex","kiro"]` / 単一`["codex"]` / 0件`[]`→exit 1経路。jqはローカル未導入のため等価Pythonで代替。ubuntu-latestにはjq標準搭載)
  - [x] `uv run pytest` / `uv run ruff check` / `uv run basedpyright` がパスする(38 passed / All checks passed / 0 errors)
- [x] 段2: 実挙動検証
  - [x] ブランチ上で `gh workflow run publish-template.yml --ref feature/publish-all-templates -f template=codex` を実行し、単一テンプレート経路が成功することを確認する(run 29181143334: 両ジョブsuccess、`No changes to publish.` を出力。配布先の最新コミットはv0.6.0同期時のままで汚染なしを確認)
  - [x] 実行ログでmatrixジョブが1件だけ起動したことを確認する(`Publishing templates: ["codex"]` / ジョブは `publish (codex)` の1件のみ)
- [ ] 段3: `Skill('code-review')` を実行し、正当なfindingsを修正する
- [ ] 段4: `implementation-validator` を起動し、指摘に対応する

## フェーズ4: 振り返り・PR

- [ ] 実装後の振り返りを記録する(このファイル下部)
- [ ] 全変更をコミットする(Conventional Commits・`Closes #48`)
- [ ] ブランチをpushし、PRを作成してURLを報告する

---

## 実装後の振り返り

### 実装完了日
{YYYY-MM-DD}

### 計画と実績の差分

**計画と異なった点**:
- [記入]

**新たに必要になったタスク**:
- [記入]

**技術的理由でスキップしたタスク**（該当する場合のみ）:
- [タスク名]: [具体的な技術的理由]

### 学んだこと

**技術的な学び**:
- [記入]

**プロセス上の改善点**:
- [記入]

### 次回への改善提案
- [記入]

### リリース判断

**前提条件の確認**:
- [ ] 全テスト通過
- [ ] リントエラーなし

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | [Yes / No / 保留] |
| 未解決の重大バグはないか | [なし / あり: 内容] |
| 適切なバージョン種別 | [MAJOR / MINOR / PATCH / リリース不要] |

**提案**:
[記入]
