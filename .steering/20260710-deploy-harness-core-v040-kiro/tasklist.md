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
以下の技術的理由に該当する場合のみスキップ可能:
- 実装方針の変更により、機能自体が不要になった
- アーキテクチャ変更により、別の実装方法に置き換わった
- 依存関係の変更により、タスクが実行不可能になった

スキップ時は必ず理由を明記:
```
- [x] ~~タスク名~~（実装方針変更により不要: 具体的な技術的理由）
```

### タスクが大きすぎる場合
- タスクをより小さなサブタスクに分割する
- 分割したサブタスクをこのファイルに追加する
- サブタスクを1つずつ完了させる

---

## フェーズ1: 規律系の小変更

- [x] `kiro-template/.steering/_template/tasklist.md` に「完了マークは操作の実行後に付ける」を1行追記する
- [x] `kiro-template/.kiro/steering/skill-sdd-guide.md` の「タスク開始時にマーク」を「完了時(実行後)にマーク」に修正し、実行後マーク規律を追記する
- [x] `kiro-template/.kiro/steering/process.md` のtasklist管理ルールを実行後マーク規律に修正する
- [x] `kiro-template/.kiro/steering/process.md` の「PR・リリースフロー」に「スタックPRの扱い」3項目を追記する(段4のスペック準拠検証で検出された分解漏れの是正)

## フェーズ2: フック刷新

- [x] `kiro-template/.kiro/hooks/tasklist-check.json` をagentStopトリガー方式に置き換える(version 2.0.0)
- [x] `kiro-template/.kiro/hooks/setup-project.json` に承認ゲート(承認して次へ/修正を指示する/スキップ、PRDはスキップ不可)を明示する(version 2.0.0)
- [x] `kiro-template/.kiro/hooks/add-feature.json` を`#skill-add-feature`参照方式に刷新する(version 2.0.0)

## フェーズ3: steeringファイル新設・追記

- [x] `kiro-template/.kiro/steering/skill-add-feature.md` を新設する(フィーチャーブランチ必須・計画承認ゲート1箇所・承認後無停止・実装ループとルールA/B・3段検証・振り返り・PR・完了条件)
- [x] `kiro-template/.kiro/steering/skill-distill.md` を新設する(環流3基準・処理手順・レポート形式・Kiro向け翻訳)
- [x] `kiro-template/.kiro/steering/skill-doc-writing.md` に「LLM向け定義ファイルの記述規約」を追記する

## フェーズ4: エージェント書き換え

- [x] `kiro-template/.kiro/agents/implementation-validator.md` をスペック準拠検証専任に書き換える(Kiro frontmatter維持・非責務は3段検証の表記に翻訳)

## フェーズ5: docs・README整合

- [x] `docs/functional-design.md` の概念マッピング表・フック一覧を実態に更新し、記憶層を適用しない判断を明文化する
- [x] `kiro-template/README.md` を確認し、変更と矛盾する箇所があれば最小限更新する(構成ツリー・add-featureフロー説明を更新)
- [x] `kiro-template/ONBOARDING.md` を確認し、変更と矛盾する箇所があれば最小限更新する(チートシート・確認5・4-2/4-3/4-4・FAQ tasklist-checkを更新)

## フェーズ6: 検証(4段)

- [x] 段1: 静的検証
  - [x] `uv run pytest` がパスする(26 passed)
  - [x] `uv run ruff check` がパスする(All checks passed)
  - [x] `uv run basedpyright` がパスする(0 errors)
  - [x] `.kiro/hooks/*.json` 全ファイルがJSONとしてパース可能である(3ファイルOK)
- [x] 段2: 実挙動検証の代替(Kiro IDE不在のため)
  - [x] フックのトリガー種別・アクション形式がKiro公式ドキュメントと整合していることを確認し、スキップと代替内容をこのファイルに記録する
    - **記録**: Kiro IDEでの実行観察は本環境では不可のためスキップ。代替: `agentStop`はkiro.dev/docs/hooks/types/に「エージェントが応答を完了した時」のトリガーとして文書化されていることを確認。`when/then`+`askAgent`形式は既存テンプレートで動作実績のある形式を維持。実機確認はマージ後にユーザーが実施(requirements.mdスコープ外に記載)
  - [x] skill-distill.mdの手順を本リポジトリの`.steering/`で机上トレースし、実行可能であることを確認する
    - **記録**: 手順1(distill-*.md不在→処理済みなし)、手順2(パターン`[0-9]*-*`が17個の日付ディレクトリに一致し`example/`を正しく除外、振り返り未記入の本作業ディレクトリは「未記入」扱いで処理済みに含めない)、手順3〜6が実行可能であることを確認
- [x] 段3: `Skill('code-review')` を実行し、正当なfindingsを修正する
  - **記録**: CONFIRMED 1件(agentStopフックがadd-featureの計画承認ゲートと衝突し、承認前に実装を開始してしまう経路)を検出し、tasklist-check.jsonのプロンプトに「ユーザーの回答を明示的に求めて応答を終えた場合は承認ゲートを迂回しない」除外条件を追加して修正。段1を再実行しパス。PLAUSIBLE 1件(agentStopの毎ターンLLM消費)は設計時に記録済みの既知トレードオフのため修正対象外
- [x] 段4: `implementation-validator` と `doc-reviewer` を並列起動し、指摘に対応する
  - **記録**: implementation-validatorが乖離1件(process.mdへの「スタックPRの扱い」追記漏れ=tasklistの分解漏れ)を検出→タスク追加のうえ追記して是正、段1再実行パス。doc-reviewerの推奨指摘4件(マッピング表の網羅性・明確さ: review-docsの扱い/スキル統合の説明/4段→3段の対応関係/PostToolUseフック対応外の明記)をすべて反映。凡例追加の軽微な補足は表現統一で足りるため見送り(既存行の「完全移植/移植済み」表現は今回のスコープ外)

## フェーズ7: 振り返り・PR

- [x] 実装後の振り返りを記録する(このファイル下部)
- [ ] 全変更をコミットする(Conventional Commits・`Closes #42`)
- [ ] ブランチをpushし、PRを作成してURLを報告する

---

## 実装後の振り返り

### 実装完了日
2026-07-11

### 計画と実績の差分

**計画と異なった点**:
- 段3(code-review)でCONFIRMED 1件を検出: agentStopフックがadd-featureの計画承認ゲートと衝突する経路(承認待ちで応答を終えるとフックが「作業継続」を注入し、承認前に実装が始まる)。tasklist-check.jsonに「ユーザーの回答を明示的に求めて終えた場合は何もしない」除外条件を追加して解消した
- 段4(implementation-validator)で乖離1件を検出: design.mdコンポーネント9のうちprocess.mdへの「スタックPRの扱い」追記を、tasklist作成時にフェーズ1タスクへ分解し損ねて未実装だった。タスク追加のうえ是正した
- 段4(doc-reviewer)の推奨指摘4件(概念マッピング表の網羅性・明確さ)を反映した

**新たに必要になったタスク**:
- `kiro-template/.kiro/steering/process.md` への「スタックPRの扱い」追記(分解漏れの是正)

**技術的理由でスキップしたタスク**:
- なし(段2の実挙動検証はKiro IDE不在のため代替検証に置換し、内容を記録済み)

### 学んだこと

**技術的な学び**:
- Kiroのフック機構はテンプレート初期作成時から大幅に拡充されていた(agentStop/PreToolUse/PostToolUse/UserPromptSubmit等のトリガー、シェルコマンドアクション、PreToolUse等での非ゼロ終了ブロック)。**移植先プラットフォームの機能は「前回調査時の結論」を信用せず、着手前に公式ドキュメントを再調査すべき**。今回それにより「askAgentのみ」前提だった設計をStopフック相当まで引き上げられた
- 「エージェントに継続を促す」タイプのフック(agentStop+プロンプト注入)は、**承認ゲートと本質的に競合する**。承認待ちで応答を終えるのは正当な停止であり、フック側に「ユーザーの回答を明示的に求めて終えた場合は何もしない」除外条件が必須。これは機械的ブロック方式(Claude CodeのStopフック)からプロンプト注入方式へ翻訳する際の一般的な落とし穴
- 機能ギャップの翻訳原則(コマンド→フック+manual steering、スキル→manual steering、worktree→フィーチャーブランチ、4段→3段検証)を対応表として設計書に先に固定すると、個々のファイル翻訳の判断が迷わない。codex-template展開(Issue #43)でも再利用できる

**プロセス上の改善点**:
- design.mdの1コンポーネントに複数ファイルの変更が含まれる場合、tasklist化の際にファイル単位へ分解しないと漏れる(今回: コンポーネント9の2ファイル目を落とした)。**tasklistのタスクは「1タスク=1ファイル1変更」の粒度で design.md の実装の要点を機械的に列挙して作る**とよい
- スペック準拠検証(implementation-validator)がこの分解漏れを実際に検出した。4段検証の段構成(静的→実挙動→レビュー→スペック準拠)が異なる種類の欠陥をそれぞれ拾うことを実地で確認できた

### 次回への改善提案
- codex-template展開(Issue #43)では、本ステアリングの翻訳原則対応表を出発点にし、Codex側の機構調査(公式ドキュメント再確認)を最初のタスクに置く
- kiro-template利用者によるKiro実機でのフック動作確認(特にagentStopトリガー名の実機検証)をマージ後のフォローアップとして実施する

### リリース判断

**前提条件の確認**:
- [x] 全テスト通過(uv run pytest: 26 passed)
- [x] リントエラーなし(uv run ruff check / basedpyright: エラーなし)

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes(kiro-template利用者がv0.4.0相当のSDD規律一式を使えるようになる) |
| 未解決の重大バグはないか | なし(agentStopトリガー名の実機未検証は既知の残リスクとしてスコープ外に記録済み) |
| 適切なバージョン種別 | MINOR(テンプレートへの機能追加・後方互換) |

**提案**:
PR マージ後、Kiro実機でのフック動作確認を経てからリリースを作成する(実機確認で問題があれば追修正をまとめてリリース)。
