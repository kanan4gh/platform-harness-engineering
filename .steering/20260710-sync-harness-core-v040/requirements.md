# 要求内容

## 概要

本家 `platform-harness` に対して22コミット分遅れているハーネスコア改善(v0.4.0相当)を、本リポジトリのルート `.claude/`・`CLAUDE.md` 汎用層・`docs/ideas/harness-engineering.md` に取り込む。

関連Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/40

## 背景

README.md に記載された開発フロー「ハーネスの改善(本家起点)」は次の4ステップである。

```
1. platform-harness で改善・PR・マージ
2. 本リポジトリに改善を取り込む(CLAUDE.md・skills等を同期)
3. Kiro・Codex向けに展開(各テンプレートに反映)
4. gh release create でリリース
```

本家では以下がすでにマージ済み(ステップ1完了)だが、本リポジトリへの取り込み(ステップ2)が行われていなかった:

- ハーネスコアのv0.4.0相当同期(worktree・承認機構化・安全な既定・distill)
- steering規律の追補「完了マークは操作の実行後に付ける」
- 運用知見の環流(スタックPR教訓・定義記述規約・フック改善構想)
- 複製時チェックリストと `/harness-doctor` 構想

## ユースケースの軸

**このリポジトリ自体をエンジニアリングする開発者(ユーザー本人)が、次回 `/add-feature` や `/setup-project` 等の本ハーネスを使って作業する際に、本家で確立された安全な既定・機構的な規律強制・4段検証を使える状態になる。**

## 実装対象の機能

### 1. CLAUDE.md 汎用層の更新

- ドキュメント作成時の承認フローを「AskUserQuestionツール」方式に変更する記述に更新する
- 「### 記憶層の運用」セクションを新規追加する(ネイティブ永続メモリを使い、自作 `memory/` ディレクトリを作らない方針)
- 本リポジトリ固有のプロダクト固有層(「🚨 このリポジトリへの改善リクエストを受けたときの必須確認」セクション)は変更しない

### 2. .claude/settings.json の更新

- `defaultMode: bypassPermissions` を削除し、安全な既定(都度確認)に戻す
- `permissions.allow` に `Skill(distill)`・`Skill(steering)`・`Bash(uv run pytest*)`・`Bash(uv run ruff*)`・`Bash(uv run basedpyright*)`・`Bash(git status*)`・`Bash(git diff*)`・`Bash(git log*)` を追加する
- `hooks.Stop`・`hooks.PostToolUse` にフックを登録する

### 3. フック・distillスキル・テスト基盤の新規追加

- `.claude/hooks/check_tasklist_complete.py`(Stopフック: 未完了タスクが残っていればセッション終了をブロック)
- `.claude/hooks/remind_tasklist_update.py`(PostToolUseフック: 編集5回続いてもtasklist.md未更新ならリマインド)
- `.claude/skills/distill/SKILL.md`(蒸留スキル: ステアリング振り返りを横断収集し環流候補を分類)
- `tests/hooks/test_check_tasklist_complete.py`・`tests/hooks/test_remind_tasklist_update.py`
- `pyproject.toml`(フックのテスト実行基盤。本リポジトリのルートには未整備だったため新規追加)

### 4. コマンド・エージェント・スキルの更新

- `.claude/commands/add-feature.md`: worktree隔離(ステップ0)・Explore/Planエージェント委譲・計画承認ゲート(ステップ4.5)・4段検証(静的検証→実挙動検証→code-review→スペック準拠検証)・PR作成(ステップ8)を含む全面刷新版を採用する
- `.claude/commands/setup-project.md`: 各ドキュメント作成後にAskUserQuestionでの承認ゲートを明示する
- `.claude/agents/implementation-validator.md`: スペック準拠検証のみに責務を限定する簡素化版を採用する
- `.claude/skills/steering/SKILL.md`: 簡素化+「完了マークは操作の実行後に付ける」規律を追加する
- `.claude/README.md`: 上記の変更を反映した説明に更新する(モデル配分表を含む)

### 5. その他ファイルの更新

- `.gitignore`: `.steering/*`(`example/`は除く)・`.claude/hooks/state/` の除外を追加する
- `docs/ideas/harness-engineering.md`: 「/harness-doctor構想」「Stopフック改善構想」の2セクションを末尾に追記する

## 受け入れ条件

### CLAUDE.md 汎用層の更新
- [ ] ドキュメント承認フローがAskUserQuestion方式の記述になっている
- [ ] 「### 記憶層の運用」セクションが追加されている
- [ ] 「🚨 このリポジトリへの改善リクエストを受けたときの必須確認」セクションが変更されずに残っている

### settings.json・フック・distillスキル
- [ ] `defaultMode: bypassPermissions` が削除されている
- [ ] allowリストに新しい許可項目が追加されている
- [ ] Stop/PostToolUseフックがsettings.jsonに登録され、対応するPythonスクリプトが `.claude/hooks/` に存在する
- [ ] `.claude/skills/distill/SKILL.md` が存在する
- [ ] `uv run pytest` でフックのテストが全てパスする

### コマンド・エージェント・スキル
- [ ] `/add-feature` がworktree隔離・承認ゲート・4段検証を含む内容になっている
- [ ] `/setup-project` の各ステップに承認ゲートの記述がある
- [ ] `implementation-validator` がスペック準拠検証に限定された内容になっている
- [ ] `steering` スキルに「完了マークは操作の実行後に付ける」規律が明記されている

### その他
- [ ] `.gitignore` に `.steering/*`(exampleを除く)と `.claude/hooks/state/` の除外が追加されている
- [ ] `docs/ideas/harness-engineering.md` に2セクションが追記されている
- [ ] `kiro-template/`・`codex-template/` 配下は一切変更されていない(スコープ外)

## 成功指標

- 本家との差分(`git diff main upstream/main -- CLAUDE.md .claude docs/ideas/harness-engineering.md`)が、意図的に対象外とした項目を除きなくなること
- `uv run pytest`・`uv run ruff check`・`uv run basedpyright` が新規追加したフック・テストに対してパスすること

## スコープ外

以下はこのフェーズでは実装しません:

- `kiro-template/`・`codex-template/` への展開(README.mdの開発フロー「3. Kiro・Codex向けに展開」に相当。別Issueで対応)
- `README.md`・`docs/harness-guide.md`・`docs/{architecture,development-guidelines,functional-design,glossary,product-requirements,repository-structure}.md` の同期(本家自身のプロダクト固有ドキュメントのため対象外)
- `gh release create` によるリリース(取り込み完了後、別途ユーザー判断で実施)

## 参照ドキュメント

- `docs/repository-structure.md` - リポジトリ構造定義書
- `docs/ideas/harness-engineering.md` - ハーネスエンジニアリングの概念メモ
- `CLAUDE.md` - プロジェクトメモリ(汎用層・プロダクト固有層・技術スタック固有層)
