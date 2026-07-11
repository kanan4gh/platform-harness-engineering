# 要求内容

## 概要

PR #41でルートに取り込んだハーネスコア改善(v0.4.0相当)を、`codex-template/`にCodex CLIの機構で展開する。

## 背景

- 関連Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/43
- kiro-template展開(Issue #42、v0.5.0)に続く、README.md開発フロー「3. Kiro・Codex向けに展開」の最終区間
- テンプレート作成時(2026-06)のCodex CLIは「AGENTS.mdのみ」が前提だったが、事前調査(公式ドキュメント learn.chatgpt.com/docs/*)により機構が大幅に拡充されていることを確認した

## ユースケースの軸

> **Codexテンプレートの利用者が、Claude Code版ハーネスと同等のtasklist規律(機械的強制を含む)・承認ゲート・検証フローの下でスペック駆動開発できるようになる。**

## 事前調査の結果(Codex CLI機構、2026-07時点)

| 機構 | 内容 | 移植への影響 |
|------|------|------------|
| フック | `.codex/hooks.json`(プロジェクトレベル)。イベントはStop/PreToolUse/PostToolUse/SessionStart等。**Stopフックは`{"decision": "block", "reason": ...}`で継続を強制でき、exit code 2のstderrも継続理由になる**(Claude Codeとほぼ同一のプロトコル) | ルートのStopフック(Python)を**ほぼ1:1移植可能**(機械的強制が実現できる) |
| スキル | `.agents/skills/**/SKILL.md`(リポジトリレベル)。frontmatterは`name`/`description`。`$`メンションまたは自動選択で起動 | distill等をスキルとして移植可能 |
| サブエージェント | `.codex/agents/<名前>.toml`(プロジェクトレベル)。`name`/`description`/`developer_instructions`等 | implementation-validator相当を定義可能 |
| ネイティブメモリ | Memories機構(v0.128+)。`generate_memories`/`use_memories`設定。EEA/UK/スイスでは利用不可 | 記憶層の運用方針をAGENTS.mdに反映可能 |
| セキュリティ | プロジェクトの`.codex/`層は**プロジェクトをtrustした場合のみロード**される | ONBOARDINGへの明記が必要 |

## 実装対象の機能

### 1. tasklist規律の機械的強制(`.codex/hooks.json`+Pythonフック)
- ルートの`check_tasklist_complete.py`をCodexのペイロード仕様に適合させて`codex-template/.codex/hooks/`に移植し、`hooks.json`でStopイベントに登録する
- Codex側に`stop_hook_active`相当のループ防止フィールドがあるか不明なため、状態ファイルによる連続ブロックガード(同一tasklist内容でのブロックがN回続いたらfail-open)を実装する
- PostToolUseリマインドフックは移植しない(Stopフックで規律は機械的に担保され、CodexのPostToolUseペイロードのフィールド仕様が未確認のため。kiro展開と同じ判断)

### 2. 「完了マークは操作の実行後に付ける」規律
- `_template/tasklist.md`に1行追記(ルート版と同一文言)
- `AGENTS.md`のtasklist管理ルールを「完了時(実行後)にマーク」に修正し、フックによる担保の説明を追加

### 3. distillスキル(`.agents/skills/distill/SKILL.md`)
- ルートのdistillスキルをCodexのSKILL.md形式で移植(環流3基準・レポート形式維持。Globツール表記は具体形パターンを保った記述に、メモリ保存提案はMemories/AGENTS.mdへの記録提案に翻訳)

### 4. add-featureワークフロー刷新(`.agents/skills/add-feature/SKILL.md`)
- 計画承認ゲート1箇所・承認後無停止・フィーチャーブランチ必須・実装ループとルールA/B・3段検証(静的検証/実挙動確認/implementation-validator)・振り返り・PRのフローをスキルとして新設
- `AGENTS.md`のワークフローセクションはスキルへの誘導に簡素化

### 5. setup-project承認ゲート明示(`.agents/skills/setup-project/SKILL.md`)
- 各ドキュメント作成後の承認3択(PRDはスキップ不可)を明示したスキルとして新設し、`AGENTS.md`側は誘導に簡素化

### 6. implementation-validator(`.codex/agents/implementation-validator.toml`)
- スペック準拠検証(3観点)専任のプロジェクトエージェントを新設(ルート新版の内容をTOMLの`developer_instructions`に反映)

### 7. development-guidelines追加分
- 「LLM向け定義ファイルの記述規約」「スタックPRの扱い」を`AGENTS.md`のプロセス原則/PRフローに反映

### 8. 記憶層の運用
- CodexにはネイティブMemories機構があるため、ルートCLAUDE.mdの「記憶層の運用」に相当するセクションを`AGENTS.md`に追加(書くべきもの/書かないもの/地域制限の注意)

### 9. README・ONBOARDING整合
- 新ディレクトリ(`.codex/`・`.agents/`)の説明、**プロジェクトのtrustが必要**な旨、新フローとの矛盾解消

## 受け入れ条件

### tasklist規律の機械的強制
- [ ] `.codex/hooks.json`がStopイベントにフックを登録し、JSONとしてパース可能である
- [ ] フックスクリプトが未完了タスク検出時に`{"decision": "block", "reason": ...}`を出力する(ユニットテストで検証)
- [ ] 連続ブロックガードが機能する(ユニットテストで検証)
- [ ] スクリプトを実際に起動しstdin/stdoutの実挙動を観察している(段2)

### 完了マーク規律
- [ ] `_template/tasklist.md`と`AGENTS.md`に実行後マーク規律が明記されている

### スキル3種
- [ ] `.agents/skills/{distill,add-feature,setup-project}/SKILL.md`が存在し、frontmatterに`name`/`description`を持つ
- [ ] add-featureに計画承認ゲート1箇所・承認後無停止・フィーチャーブランチ必須・3段検証が含まれる
- [ ] Claude Code固有のツール名・機構名への参照が残っていない

### implementation-validator
- [ ] `.codex/agents/implementation-validator.toml`がTOMLとしてパース可能で、スペック準拠検証専任の指示を含む

### その他
- [ ] AGENTS.mdにスタックPRの扱い・LLM向け定義ファイル記述規約・記憶層の運用が反映されている
- [ ] README/ONBOARDINGがtrust要件と新構成を説明している

## 成功指標

- Issue #43のチェックリスト8項目すべてに対応が完了している
- kiroでは実現できなかった「tasklist規律の機械的強制」がCodexでは実現されている

## スコープ外

- ルート`.claude/`・kiro-template/の変更(完了済み)
- Codex CLI実機での動作確認(マージ後にユーザーが実施。特にフックのペイロードフィールド・スキル認識・trustフロー)
- PostToolUseリマインドフックの移植(上記1の判断根拠を参照。実機確認後に必要なら追加)

## 参照ドキュメント

- Issue #43 / PR #41 / v0.5.0リリース
- `.steering/20260710-deploy-harness-core-v040-kiro/`(翻訳原則対応表)
- Codex公式: learn.chatgpt.com/docs/hooks, /docs/build-skills
