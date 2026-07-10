# タスクリスト

## 🚨 タスク完全完了の原則

**このファイルの全タスクが完了するまで作業を継続すること**

### 必須ルール
- **全てのタスクを`[x]`にすること**
- 「時間の都合により別タスクとして実施予定」は禁止
- 「実装が複雑すぎるため後回し」は禁止
- 未完了タスク（`[ ]`）を残したまま作業を終了しない

---

## フェーズ0: 作業ブランチの準備

- [x] `feature/sync-harness-core-v040` ブランチを作成する
  - [x] `main` が最新であることを確認する(`git status`)
  - [x] `git checkout -b feature/sync-harness-core-v040`

## フェーズ1: 新規ファイルの追加(パターンA)

- [x] `.claude/hooks/check_tasklist_complete.py` を追加する(`git show upstream/main:.claude/hooks/check_tasklist_complete.py` の内容をそのまま書き込む)
- [x] `.claude/hooks/remind_tasklist_update.py` を追加する(同上)
- [x] `.claude/skills/distill/SKILL.md` を追加する(同上)
- [x] `tests/hooks/test_check_tasklist_complete.py` を追加する(同上)
- [x] `tests/hooks/test_remind_tasklist_update.py` を追加する(同上)
- [x] `pyproject.toml` を追加する
  - [x] upstream版の内容を取得する
  - [x] `name` を `platform-harness-engineering` に変更する
  - [x] `description` を本リポジトリの実態(SDDハーネスのマルチテンプレートジェネレーター)に合わせて書き換える
  - [x] dependency-groups・pytest/ruff/basedpyright設定はupstreamのまま採用する

## フェーズ2: 全面採用ファイルの更新(パターンA)

- [x] `.claude/commands/add-feature.md` をupstream版で上書きする
- [x] `.claude/commands/setup-project.md` をupstream版で上書きする
- [x] `.claude/agents/implementation-validator.md` をupstream版で上書きする
- [x] `.claude/skills/steering/SKILL.md` をupstream版で上書きする
- [x] `.claude/README.md` をupstream版で上書きする

## フェーズ3: 部分反映ファイルの更新(パターンB)

- [x] `CLAUDE.md` を更新する
  - [x] 「ドキュメント作成時」の承認待ちの記述をAskUserQuestion方式に更新する
  - [x] 「### 記憶層の運用」セクションを「### 永続的ドキュメント一覧」の後・「### 初回セットアップ」の前に追加する
  - [x] 「🚨 このリポジトリへの改善リクエストを受けたときの必須確認」セクションが変更されていないことを確認する
- [x] `.claude/settings.json` を更新する
  - [x] `defaultMode: bypassPermissions` を削除する
  - [x] `permissions.allow` に `Skill(distill)`・`Skill(steering)`・`Bash(uv run pytest*)`・`Bash(uv run ruff*)`・`Bash(uv run basedpyright*)`・`Bash(git status*)`・`Bash(git diff*)`・`Bash(git log*)` を追加する
  - [x] `hooks.Stop`・`hooks.PostToolUse` を登録する
  - [x] JSONとして正しくパースできることを確認する(`python3 -c "import json; json.load(open('.claude/settings.json'))"`)
- [x] `.gitignore` を更新する
  - [x] ~~`.steering/*` / `!.steering/example/` の除外を追加する~~（設計変更により不要: upstream自身のdocs記述で「この除外はテンプレート複製時向けであり、プロジェクト運用では解除すべき」と明記されている。本リポジトリは既存の`.steering/`履歴を保持する実運用プロジェクトのため、このルールは採用しない）
  - [x] `.claude/hooks/state/` の除外を追加する
- [x] `docs/ideas/harness-engineering.md` に2セクションを追記する
  - [x] 「/harness-doctor構想」セクション
  - [x] 「Stopフック改善構想」セクション
- [x] （フェーズ6の全体差分確認で発見・追加したタスク）`.claude/skills/` 配下の見落とし分を反映する
  - [x] `.claude/skills/development-guidelines/guides/implementation.md` に「LLM向け定義ファイルの記述規約」セクションを追記する
  - [x] `.claude/skills/development-guidelines/guides/process.md` に「スタックPRの扱い」セクションを追記する
  - [x] `.claude/skills/steering/templates/tasklist.md` に「完了マークは操作の実行後に付けること」の必須ルールを追記する

## フェーズ4: 依存関係セットアップと検証

- [x] `uv sync` を実行し `uv.lock` を生成する
- [x] `uv run pytest` を実行し、新規追加したフックのテストが全てパスすることを確認する(26 passed)
- [x] `uv run ruff check` を実行し、エラーがないことを確認する(All checks passed!)
- [x] `uv run basedpyright` を実行し、エラーがないことを確認する(0 errors, 0 warnings, 0 notes)
- [x] エラーが出た場合は修正し、再度この段を実行する（エラーなし、対応不要）

## フェーズ5: 実挙動確認

- [x] Stopフックの動作確認: 意図的に未完了タスク(`- [ ]`)を含むダミーのステアリングディレクトリ(または本ファイル自体が全タスク完了前の状態)に対してテストが期待通りブロック判定を返すことを、`tests/hooks/test_check_tasklist_complete.py` の実行結果で確認する(`test_check_incomplete_tasks_blocks`等が実際にblock判定を検証しPASS)
- [x] PostToolUseフックの動作確認: 同様に `tests/hooks/test_remind_tasklist_update.py` の実行結果で確認する(`test_check_threshold_reached_reminds_and_resets`等がPASS)
- [x] `.claude/settings.json` の hooks 登録パスが実ファイルと一致していることを目視確認する(`/harness-doctor`構想が指摘する不整合パターンの手動チェック)（Stop→check_tasklist_complete.py、PostToolUse→remind_tasklist_update.py いずれも実在を確認済み）

## フェーズ6: 差分確認とドキュメント整合性チェック

- [x] `git diff main upstream/main -- CLAUDE.md .claude docs/ideas/harness-engineering.md .gitignore` を実行し、残る差分が意図的な対象外(このリポジトリ固有のプロダクト固有層セクション等)のみであることを確認する（計画時の分析漏れとして `.claude/skills/development-guidelines/guides/{implementation,process}.md`・`.claude/skills/steering/templates/tasklist.md` の3ファイルに未反映の差分を発見し、追加で反映した。反映後は `.claude`・`tests` 配下の全差分が解消され、残るのは `.gitignore`(4行, 意図的不採用)・`CLAUDE.md`(11行, 本リポジトリ固有セクション)・`pyproject.toml`(name/description調整)・`uv.lock`(依存解決の実体差)のみであることを確認済み）
- [x] `.claude/README.md` の記述(ファイル一覧・設定の意味・モデル配分表)が実際のファイル構成と一致していることを確認する
- [x] `CLAUDE.md` の「🚨 このリポジトリへの改善リクエストを受けたときの必須確認」セクションが引き続き存在し、内容が変わっていないことを確認する

## フェーズ7: コミットとPR作成

- [ ] 変更をコミットする(Conventional Commits形式、本文に `Closes #40` を含める)
- [ ] ブランチをpushする
- [ ] `gh pr create --repo kanan4gh/platform-harness-engineering` でPRを作成する(本文: 概要・変更理由・変更内容・テスト結果・関連Issue)
- [ ] PRのURLをユーザーに報告する

## フェーズ8: 振り返り

- [x] 実装後の振り返り(このファイルの下部に記録)

---

## 実装後の振り返り

### 実装完了日
2026-07-10

### 計画と実績の差分

**計画と異なった点**:
- `.gitignore` の `.steering/*` 除外は計画時にはupstream版をそのまま採用する想定だったが、upstream自身のdocs(旧harness-guide.md、現README.mdに統合済み)が「この除外はテンプレート複製時向けであり、実際のプロジェクト運用では解除すべき」と明記していたため、採用しないことに設計変更した。本リポジトリは既存の`.steering/`履歴(20260603〜)を保持する実運用リポジトリであり、upstream(テンプレート)とは前提が異なるため

**新たに必要になったタスク**:
- フェーズ6の全体差分確認で、当初のrequirements.md/design.mdでは把握していなかった3ファイルの差分を発見した: `.claude/skills/development-guidelines/guides/implementation.md`(LLM向け定義ファイルの記述規約)・`process.md`(スタックPRの扱い)・`.claude/skills/steering/templates/tasklist.md`(完了マーク規律)。CLAUDE.md汎用層が「`.claude/skills/`・steeringテンプレート」を明示的にハーネスコアの改善対象としているため、スコープ内と判断し追加で反映した

**技術的理由でスキップしたタスク**（該当する場合のみ）:
- なし(上記の`.gitignore`除外は「スキップ」ではなく設計変更として記録)

### 学んだこと

**技術的な学び**:
- `git diff <ref1> <ref2> -- <path>` は2つのコミット間の比較であり、作業ツリーの未コミット変更は反映されない。新規追加した未トラッキングファイルを検証する際は `git diff <ref> -- <path>`(作業ツリーと比較)を使うか、先に `git add` してから比較する必要がある
- 事前調査で個別ファイルを名指しで診断すると、名指ししなかった関連ファイル(同じスキル配下の別ガイドファイル等)の差分を見落とすリスクがある。`git diff --stat <ref1> <ref2>` のような網羅的な差分一覧を先に取ってから絞り込む方が確実

**プロセス上の改善点**:
- requirements.md・design.mdでの事前承認により、実装中に発見した想定外の差分(gitignoreの設計変更・development-guidelinesの見落とし)についても「何が計画と違うか」を明確に切り分けて記録でき、場当たり的な対応にならずに済んだ
- 本家(upstream)自身が「テンプレート vs プロジェクト」の運用差をdocsに明記していたことが、`.gitignore`の設計判断の根拠として非常に役立った。本家の関連ドキュメントも合わせて読む価値がある

### 次回への改善提案
- 今後同様の本家同期を行う際は、対象ディレクトリ全体(`.claude/` 配下全ファイル)の `git diff --stat` を最初に取得し、個別ファイル診断はその後の絞り込みとして使う
- `kiro-template/`・`codex-template/` への展開(README.md開発フロー「3.」)は別Issue・別ステアリングで行う

### リリース判断

> Claude が評価・提案し、プロジェクトオーナーが最終決定する。

**前提条件の確認**:
- [x] 全テスト通過(`uv run pytest` 26 passed)
- [x] リントエラーなし(`uv run ruff check` All checks passed / `uv run basedpyright` 0 errors)
- [x] リリースノートに記載すべき変更内容が整理されている

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes |
| 未解決の重大バグはないか | なし |
| 適切なバージョン種別 | MINOR |

**提案**:
`vX.Y.0`(現行バージョンのMINORアップ)を提案。理由: 新しいフック機構(規律の機械的強制)・distillスキル・4段検証フローという新機能の追加であり、後方互換を壊す変更ではないためMINORが適切。PRマージ後、リリースコマンド実行前に本Issue(#40)をクローズすること。
