# 要求内容

## 概要

PR #41でルート`.claude/`・CLAUDE.md汎用層に取り込んだ本家platform-harnessのハーネスコア改善(v0.4.0相当)を、`kiro-template/`にKiroのフォーマットで展開する。

## 背景

- 関連Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/42
- README.mdの開発フロー「3. Kiro・Codex向けに展開(各テンプレートに反映)」に基づく作業
- Project-uroboros → platform-harness → 本リポジトリルートと展開してきたSDDハーネス進化を、Kiro環境へ届ける最終区間
- `kiro-template/`はClaude Codeの`.claude/`とは機構が異なる(`.kiro/steering/`・`.kiro/agents/`・`.kiro/hooks/`・`.steering/_template/`)ため、単純コピーではなく「Kiroの機構で実現可能な範囲」への翻訳が必要

## ユースケースの軸

> **Kiroテンプレートの利用者が、Claude Code版ハーネスと同等のtasklist規律・承認ゲート・検証フローの下でスペック駆動開発できるようになる。**

## 事前調査の結果(Kiroフック機構)

Kiro公式ドキュメント(kiro.dev/docs/hooks/)の調査により、テンプレート作成当時の前提が変わっていることを確認した:

| 項目 | テンプレート作成時の前提 | 現在のKiro |
|------|----------------------|-----------|
| トリガー種別 | fileEdited / userTriggered 程度 | SessionStart / **Stop(agentStop)** / PreToolUse / PostToolUse / PreTaskExec / PostTaskExec / UserPromptSubmit / PostFileCreate / PostFileSave / PostFileDelete |
| アクション種別 | askAgent のみ | **agentプロンプト** と **シェルコマンド** の2種 |
| ブロック能力 | なし | PreToolUse / UserPromptSubmit / PreTaskExec はシェルコマンド非ゼロ終了でブロック可。**Stopトリガーのブロック能力は文書化されていない** |

→ Claude CodeのStopフック(機械的ブロック)の完全な等価物は未確認だが、**Stopトリガー+agentプロンプトで「未完了タスクがあれば継続を促す」注入**が可能であり、現状の`fileEdited`+askAgentより大幅に強化できる。

## 実装対象の機能

### 1. tasklist規律の強制強化(`.kiro/hooks/tasklist-check.json`)
- 現状の`fileEdited`+askAgent方式を、`Stop`(エージェント応答完了時)トリガー方式に強化する
- エージェントが応答を終えるたびに、最新ステアリングディレクトリのtasklist.mdの未完了タスク(`[ ]`)を確認させ、残っていれば作業継続を促す

### 2. 「完了マークは操作の実行後に付ける」規律の反映
- `kiro-template/.steering/_template/tasklist.md`の必須ルールに1行追記する(ルート版と同一文言)
- `.kiro/steering/skill-sdd-guide.md`のtasklist管理ルールにも同規律を反映する

### 3. distillスキル相当(`.kiro/steering/skill-distill.md`新設)
- ルートの`.claude/skills/distill/SKILL.md`をKiroのmanual steeringファイル(`inclusion: manual`、`#skill-distill`で呼び出し)として翻訳する
- Claude Code固有のツール表記(Glob等)はKiroで通じる表現に置き換える

### 4. add-featureワークフロー刷新(`.kiro/hooks/add-feature.json`)
- ルートの新add-feature.mdの骨格(計画承認ゲート1箇所・承認後は無停止・タスク分割/スキップ規律・多段検証・振り返り)をKiroのuserTriggeredフックのプロンプトに反映する
- worktree隔離はKiro GUI完結の指針(指針1)と相容れないため、「フィーチャーブランチ必須・mainで実装しない」に翻訳する
- 4段検証はKiroで実現可能な形(静的検証コマンド・実挙動確認・@implementation-validatorによるスペック準拠検証)に翻訳する

### 5. setup-project承認ゲート明示(`.kiro/hooks/setup-project.json`)
- 各ドキュメント作成後の承認確認(承認して次へ/修正を指示する/スキップ)を明示的にプロンプトへ反映する

### 6. implementation-validatorの責務限定(`.kiro/agents/implementation-validator.md`)
- ルート版と同様に「スペック準拠検証(requirements/design/tasklistとの整合性)」のみに責務を限定した簡素版に書き換える
- コード品質・テスト・セキュリティ・パフォーマンスの観点は検証フローの他段に委ねる

### 7. development-guidelines追加分の反映
- 「LLM向け定義ファイルの記述規約」→ `.kiro/steering/skill-doc-writing.md`に追記
- 「スタックPRの扱い」→ `.kiro/steering/process.md`のPRフローセクションに追記

### 8. 記憶層の運用(適用しない判断の明文化)
- Kiroにはネイティブ永続メモリ機構がない(functional-design.mdで確認済み)ため、CLAUDE.mdの「記憶層の運用」セクションは適用しない
- 既存の代替設計(steering/docsへの記述)が既にfunctional-design.mdに定義されているため、変更不要とする

## 受け入れ条件

### tasklist規律の強制強化
- [ ] `.kiro/hooks/tasklist-check.json`がStopトリガー方式に更新されている
- [ ] フックのJSONが公式ドキュメントのスキーマに準拠し、パース可能である

### 完了マーク規律
- [ ] `_template/tasklist.md`と`skill-sdd-guide.md`に「完了マークは操作の実行後に付ける」が明記されている

### distill相当
- [ ] `.kiro/steering/skill-distill.md`が存在し、環流3基準(普遍性・再現性・抽象性)の分類手順を含む
- [ ] Claude Code固有のツール名・スキル名への参照が残っていない

### add-feature刷新
- [ ] 計画承認ゲートが1箇所であること、承認後は無停止であることがプロンプトに明記されている
- [ ] フィーチャーブランチ必須(mainで実装しない)が明記されている
- [ ] 多段検証(静的検証→実挙動→スペック準拠)が含まれている

### setup-project
- [ ] 各ドキュメント作成後の承認確認方法が明示されている

### implementation-validator
- [ ] スペック準拠検証のみに責務が限定され、他観点は検証フローの他段に委ねる旨が記載されている

### development-guidelines追加分
- [ ] skill-doc-writing.mdに「設計の具体形を転記する」「既存ファイルの用語に引っ張られない」が反映されている
- [ ] process.mdに「スタックPRの扱い」が反映されている

### 全体
- [ ] `kiro-template/README.md`・`ONBOARDING.md`が変更内容と矛盾していない(必要なら更新)
- [ ] `docs/functional-design.md`の概念マッピング表が実態(新フック等)を反映している

## 成功指標

- Issue #42のチェックリスト8項目すべてに対応(反映または「適用しない判断+根拠の記録」)が完了している
- Kiroテンプレート利用者がClaude Code版と同じSDD規律(タスク完全完了・承認ゲート・多段検証)を体験できる

## スコープ外

以下はこのフェーズでは実装しません:

- ルート`.claude/`側の変更(PR #41で完了済み)
- `codex-template/`への展開(Issue #43で別途対応)
- Kiro実機(IDE)でのフック動作確認(本環境にKiro IDEがないため、公式ドキュメント準拠とJSON妥当性検証まで。実機確認はマージ後にユーザーが行い、問題があれば追修正する)
- Pythonシェルスクリプトフック(check_tasklist_complete.py相当)のkiro-templateへの導入(Stopトリガーのブロック能力が文書上未確認のため、まずagentプロンプト方式で反映し、実機確認後に強化を検討する)

## 参照ドキュメント

- Issue #42: https://github.com/kanan4gh/platform-harness-engineering/issues/42
- PR #41: https://github.com/kanan4gh/platform-harness-engineering/pull/41
- `.steering/20260710-sync-harness-core-v040/` - ルート同期時のステアリング記録
- `docs/functional-design.md` - Kiro概念マッピング・設計指針(GUI完結/devcontainer非依存/built-in specs不使用)
- Kiro公式: https://kiro.dev/docs/hooks/ (トリガー・アクション仕様)
