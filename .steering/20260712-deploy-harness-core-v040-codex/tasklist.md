# タスクリスト

## 🚨 タスク完全完了の原則

**このファイルの全タスクが完了するまで作業を継続すること**

### 必須ルール
- **全てのタスクを`[x]`にすること**
- **完了マークは操作の実行後に付けること**(実行予定の段階で付けない)
- 「時間の都合により別タスクとして実施予定」は禁止
- 「実装が複雑すぎるため後回し」は禁止
- 未完了タスク（`[ ]`）を残したまま作業を終了しない

### タスクスキップが許可される唯一のケース
技術的理由(実装方針変更・アーキテクチャ変更・依存関係変更)のみ。スキップ時:
```
- [x] ~~タスク名~~（実装方針変更により不要: 具体的な技術的理由）
```

### タスクが大きすぎる場合
サブタスクに分割してこのファイルに追加し、1つずつ完了させる。

---

## フェーズ1: フック(機械的強制)

- [x] `codex-template/.codex/hooks/check_tasklist_complete.py` を新設する(ルート版から適合移植: cwd解決・連続ブロックガード)
- [x] `codex-template/.codex/hooks.json` を新設する(Stopイベント登録)
- [x] `codex-template/.gitignore` を新設する(`.codex/hooks/state/` の除外)
- [x] `tests/hooks/test_codex_check_tasklist_complete.py` を新設する(block判定・ガード動作・cwd解決のテスト。11件パス)

## フェーズ2: スキル3種

- [x] `codex-template/.agents/skills/add-feature/SKILL.md` を新設する(計画承認ゲート1箇所・承認後無停止・フィーチャーブランチ必須・実装ループとルールA/B・3段検証・振り返り・PR・完了条件)
- [x] `codex-template/.agents/skills/setup-project/SKILL.md` を新設する(承認3択・PRDスキップ不可)
- [x] `codex-template/.agents/skills/distill/SKILL.md` を新設する(環流3基準・Codex向け翻訳)

## フェーズ3: エージェント定義

- [x] `codex-template/.codex/agents/implementation-validator.toml` を新設する(スペック準拠検証専任・3観点)

## フェーズ4: AGENTS.md・テンプレート

- [x] `AGENTS.md` のtasklist管理ルールを実行後マーク規律+フック担保の説明に更新する
- [x] `AGENTS.md` のPR・リリースフローに「スタックPRの扱い」を追記する
- [x] `AGENTS.md` のプロセス原則に「LLM向け定義ファイルの記述規約」を追記する
- [x] `AGENTS.md` に「記憶層の運用」セクションを追加する(Memories機構・地域制限の注意)
- [x] `AGENTS.md` のワークフローセクションをスキルへの誘導に簡素化する(distillへの誘導も追加)
- [x] `codex-template/.steering/_template/tasklist.md` に実行後マーク規律を1行追記する

## フェーズ5: README・ONBOARDING

- [x] `codex-template/README.md` を更新する(構成ツリー・trust要件・新フロー説明・できること表・移行対応表)
- [x] `codex-template/ONBOARDING.md` を更新する(trust手順ステップ2.5・Stopフック動作確認=確認4・新フロー4-2/4-3・チートシート。FAQは確認4内の注記で代替)

## フェーズ6: 検証(4段)

- [x] 段1: 静的検証
  - [x] `uv run pytest` がパスする(37 passed、新テスト11件含む)
  - [x] `uv run ruff check` がパスする(All checks passed)
  - [x] `uv run basedpyright` がパスする(0 errors)
  - [x] `hooks.json` のJSONパースと `implementation-validator.toml` のTOMLパースが通る
- [x] 段2: 実挙動検証
  - [x] フックスクリプトをstdinシミュレートで実起動し、3ケース(未完了あり→block / 未完了なし→無出力 / 同一内容3回→ガードでfail-open)の実挙動を観察する(scratchpad上で全ケース期待どおり動作)
  - [x] SKILL.md群のfrontmatter(name/description)を検証する(3スキルOK)
  - [x] Codex実機での確認はスコープ外である旨をこのファイルに記録する
    - **記録**: Codex CLI実機での確認(Stopフックのペイロード実仕様・スキル認識・trustフロー・サブエージェント起動)は本環境では不可のためスコープ外。フックのstdin/stdoutプロトコルは公式ドキュメント記載(learn.chatgpt.com/docs/hooks)に準拠して実装し、スクリプト単体の実挙動は観察済み。実機確認はマージ後にユーザーが実施(ONBOARDING.md確認1〜4がその手順を兼ねる)
- [x] 段3: `Skill('code-review')` を実行し、正当なfindingsを修正する
  - **記録**: PLAUSIBLE 2件を検出し両方修正: (1) ONBOARDING確認4のテスト用ディレクトリ名が固定日付で、既存作業スペックがあると最新判定されずフックが発火しない→「今日の日付・最新になる名前」の指示に修正 (2) 全完了時に状態ファイルを無条件書き込みしクリーンな環境を汚す→ブロック履歴がある場合のみリセットに修正+テスト追加(38 passed)。段1再実行パス
- [x] 段4: `implementation-validator` と `doc-reviewer` を並列起動し、指摘に対応する
  - **記録**: implementation-validator=⚠️要記録1件(ONBOARDING確認4の削除手順に固定日付が残存=段3修正の適用漏れ)→修正。doc-reviewer=必須1件(AGENTS.mdのスペック作成手順3ゲートとadd-featureの1ゲートの内部矛盾)→add-feature使用時は計画承認1箇所に統合される旨の例外注記を追加。実務指摘(`__pycache__`のコミット混入リスク)→pycache削除+テンプレート.gitignoreに除外追加。「粒度別コンテキスト注入行の削除」は新設の「オンデマンドの手順書読込」行が代替であるため意図的と判断し変更なし

## フェーズ7: 振り返り・PR

- [x] 実装後の振り返りを記録する(このファイル下部)
- [x] 全変更をコミットする(Conventional Commits・`Closes #43`)
- [x] ブランチをpushし、PRを作成してURLを報告する(https://github.com/kanan4gh/platform-harness-engineering/pull/47)

---

## 実装後の振り返り

### 実装完了日
2026-07-12

### 計画と実績の差分

**計画と異なった点**:
- 段3(code-review)でPLAUSIBLE 2件を検出・修正: ONBOARDING確認4のテスト用ディレクトリ固定日付問題 / 全完了時の状態ファイル無条件書き込み
- 段4で3件対応: 段3修正の適用漏れ(削除手順の固定日付) / AGENTS.md内の承認ゲート記述の内部矛盾(スペック作成手順3ゲートvs add-feature 1ゲート)への例外注記 / `__pycache__`混入防止(.gitignore拡張)

**新たに必要になったタスク**:
- テンプレート.gitignoreへの`__pycache__/`除外追加(段4の実務指摘)

**技術的理由でスキップしたタスク**:
- なし

### 学んだこと

**技術的な学び**:
- Codex CLIのフックプロトコル(Stopイベント・`decision: block`・exit code 2・stdinペイロード)はClaude Codeとほぼ同一で、Pythonフックの機構移植が成立した。**移植先の機構がソースとどれだけ同型かで「翻訳」(kiro)と「移植」(codex)を使い分ける**のが展開作業の基本判断
- 機械的ブロックをプラットフォーム外の状態で制御する場合、ソース側のループ防止フィールド(`stop_hook_active`)が移植先に存在しないことがある。**状態ファイルによる連続ブロックガード(同一内容N回でfail-open)は、プロトコル差異に依存しない汎用的なループ防止手段**として機能する
- ドキュメント内の同一情報の重複箇所(作成手順と削除手順のディレクトリ名等)は、片方だけ修正する適用漏れが起きやすい。修正時は同じ値を参照する全箇所をgrepで洗うべき

**プロセス上の改善点**:
- kiro展開の教訓(定義ファイルの認識条件を設計前に実例確認)を最初のタスクに置いたことで、kiroで起きた「実機で拡張子問題が発覚」のような手戻りを設計段階で回避できた(スキルは`.agents/skills/**/SKILL.md`のみ認識・`.codex/`層はtrust必須、を事前に反映)
- 「1タスク=1ファイル1変更」の粒度でtasklistを作った結果、kiro展開で起きた分解漏れは発生しなかった

### 次回への改善提案
- 本Issueでv0.4.0相当の全テンプレート展開が完了。次の展開サイクルでは、今回確立した「事前調査→翻訳原則対応表→add-featureフロー→実機確認ゲート→リリース」のパターンをそのまま再利用する
- 環流候補: 「連続ブロックガード付きStopフック」はplatform-harness本家のフックにも有用な可能性がある(Claude Codeのstop_hook_activeは1回スキップのみで、恒常的に消化不能なtasklistでは毎ターンブロックが再発する)。distill実行時に検討する

### リリース判断

**前提条件の確認**:
- [x] 全テスト通過(uv run pytest: 38 passed)
- [x] リントエラーなし(ruff / basedpyright: 0 errors)

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes(codex-template利用者がv0.4.0相当のSDD規律一式+機械的強制を使えるようになる) |
| 未解決の重大バグはないか | なし(Codex実機でのフック発火・スキル認識は未検証だが、既知の残確認事項としてスコープ外に記録済み) |
| 適切なバージョン種別 | MINOR(テンプレートへの機能追加・後方互換) |

**提案**:
PRマージ後、Codex実機での確認(ONBOARDING確認1〜4相当)を経てからリリースを作成する(kiro展開v0.5.0と同じ運用)。
