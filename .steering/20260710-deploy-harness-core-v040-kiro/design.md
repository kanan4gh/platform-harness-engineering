# 設計書

## アーキテクチャ概要

本作業はルート`.claude/`(v0.4.0相当)の改善を`kiro-template/`へ「Kiroの機構に翻訳して」反映するドキュメント・設定ファイル作業である。翻訳にあたり以下の対応原則を適用する。

```
Claude Code機構              → Kiro機構(翻訳先)
─────────────────────────────────────────────────
Stopフック(Python・ブロック)  → agentStopトリガー+agentプロンプト(継続を促す注入)
スラッシュコマンド(.md)       → userTriggeredフック(.json) + manual steering(詳細手順)
スキル(SKILL.md)             → .kiro/steering/skill-*.md (inclusion: manual)
サブエージェント(.claude/agents) → .kiro/agents/*.md (@名前で呼び出し)
worktree隔離                 → フィーチャーブランチ必須(Kiro Git統合UI・GUI完結の指針1)
4段検証(pytest/verify/code-review/validator) → 3段検証(静的検証/実挙動確認/@implementation-validator)
ネイティブ永続メモリ          → 適用しない(既存のsteering/docs代替設計を維持)
```

**翻訳の制約(事前調査で確定した事実)**:
- Kiroのフックアクションは「agentプロンプト」と「シェルコマンド」の2種。シェルコマンド非ゼロ終了によるブロックはPreToolUse / UserPromptSubmit / PreTaskExecのみ文書化されており、**agentStopのブロック能力は文書化されていない**。よってStopフック相当は「agentStop+agentプロンプトによる継続指示の注入」で実現する(機械的ブロックではないが、毎ターン終了時に確認が走る点でClaude CodeのStopフックと同じタイミング・同じ意図)
- Kiroに`/code-review`・`/verify`相当のビルトインスキルはないため、4段検証は3段に翻訳する
- フックJSONのスキーマは既存テンプレートで実績のある`{name, version, when: {type}, then: {type, prompt}}`形式を維持し、トリガー種別のみ`agentStop`を使う

## コンポーネント設計

### 1. `.kiro/hooks/tasklist-check.json`(置き換え)

**責務**: エージェントの応答完了(agentStop)のたびに、最新ステアリングディレクトリのtasklist.mdに未完了タスク(`[ ]`)が残っていないか確認させ、残っていれば作業継続を促す(ルートの`check_tasklist_complete.py` Stopフックの翻訳)。

**実装の要点**:
- `when.type`を`fileEdited`から`agentStop`に変更する(応答完了ごとに評価される方が、tasklist編集時のみの現行より網羅的)
- プロンプトに具体形を転記する: 「`.steering/`直下の`YYYYMMDD-`接頭辞ディレクトリのうち日付が最新のものの`tasklist.md`を確認」「`- [ ]`が残っていれば、タスクを完了させるか、ルールA(分割)/ルールB(技術的スキップ)を適用するまで作業を終了しない」
- ルート版と同じ除外条件を明記する: tasklist.md不在・全完了なら何もしない(ユーザーへの割り込みをしない)
- `version`を`2.0.0`に上げる

### 2. `.steering/_template/tasklist.md`(1行追記)

**責務**: 「完了マークは操作の実行後に付ける」規律のテンプレートへの反映。

**実装の要点**:
- 必須ルールの「全てのタスクを`[x]`にすること」の直後に、ルート版と同一文言で1行追加する:
  `- **完了マークは操作の実行後に付けること**(実行予定の段階で付けない)`

### 3. `.kiro/steering/skill-sdd-guide.md`(規律の修正+追記)

**責務**: tasklist管理ルールへの「実行後マーク」規律の反映。

**実装の要点**:
- 現行の「タスク**開始時**に `[ ]` → `[x]` へ**即座に**更新する」は新規律と矛盾する(開始時にマークすると実行前マークになる)。「タスク**完了時**に `[ ]` → `[x]` へ**即座に**更新する」に修正する
- 「完了マークは操作の実行後に付ける(実行予定の段階で付けない。コミット・PR作成など、マークの後に実行しがちな操作は特に注意)」を必須動作に追加する

### 4. `.kiro/steering/skill-distill.md`(新設)

**責務**: ルートdistillスキルのKiro翻訳。`.steering/`の振り返りから知見を抽出し、環流3基準(普遍性・再現性・抽象性)で分類してplatform-harnessへの環流候補を提示する。

**実装の要点**:
- frontmatter: `inclusion: manual`(`#skill-distill`で呼び出し)
- 処理手順(処理済み一覧→振り返り収集→知見抽出→3基準分類→レポート出力→報告)はルート版の構成を維持する
- Claude Code固有表記の翻訳:
  - `Glob('.steering/[0-9]*-*/tasklist.md')` → 「`.steering/`直下の`YYYYMMDD-`接頭辞ディレクトリ(パターン: `[0-9]*-*`)の`tasklist.md`を列挙する」(具体形パターンは保持し、ツール名のみ除去)
  - 「ネイティブ永続メモリへの保存を提案」→「`.kiro/steering/product.md`等への記録を提案」(Kiroのmemory代替設計に整合)
- 環流候補の変更対象パスはplatform-harness(Claude Code版)の構造で書く点はルート版と同じ(環流先はClaude Codeハーネスであるため)

### 5. `.kiro/hooks/add-feature.json` + `.kiro/steering/skill-add-feature.md`(刷新+新設)

**責務**: ルート新add-feature.mdの骨格(計画承認ゲート1箇所・承認後無停止・タスク規律・多段検証・振り返り・PR)のKiro翻訳。

**実装の要点**:
- 詳細手順はJSON文字列に押し込めず、`.kiro/steering/skill-add-feature.md`(inclusion: manual)に置く。フックのプロンプトは「機能名の確認→`#skill-add-feature`の手順に従う」への誘導に絞る(既存の`#skill-sdd-guide`参照方式と同じパターン)
- skill-add-feature.mdの構成(ルート版のステップをKiroに翻訳):
  - ステップ0: フィーチャーブランチ作成(Kiro Git統合UI)。**mainブランチ上で実装を始めない**。worktreeは使わない(GUI完結の指針1)
  - ステップ1-3: Issue確認/作成 → `.steering/_template/`複製 → docs/読み込みと既存パターン調査
  - ステップ4: requirements.md / design.md / tasklist.mdの生成
  - ステップ4.5: **計画承認ゲート(唯一の承認ゲート)**。design.mdの要点とtasklist.mdのタスク一覧を提示し、ユーザーの承認を得る。修正指示があれば反映して再度承認を求める。**承認後は完了まで無停止**
  - ステップ5: 実装ループ(全タスク`[x]`まで。ルールA: 分割/ルールB: 技術的スキップのみ許可。禁止事項もルート版と同一)
  - ステップ6: 3段検証(段1: tech.mdの静的検証コマンド実行 / 段2: 実挙動確認(変更種別に応じ観察、純ドキュメントはスキップを記録) / 段3: `@implementation-validator`によるスペック準拠検証)。各段の失敗は修正して同じ段を再実行、実装変更時は段1からやり直す
  - ステップ7: 振り返り記入とdocs/更新判断
  - ステップ8: PR作成(フィーチャーブランチ→main。Kiro Git統合UIまたはGitHub Web UI)
- 完了条件リストもルート版に準じて記載する

### 6. `.kiro/hooks/setup-project.json`(承認ゲート明示)

**責務**: 各ドキュメント作成後の承認確認方法の明示(ルート版setup-project.mdの承認ゲート翻訳)。

**実装の要点**:
- プロンプトに承認ゲートの選択肢を明記する: 「承認して次へ / 修正を指示する / このドキュメントをスキップ」の3択を各ドキュメント作成後に提示する
- PRDのみスキップ選択肢を提示しない(以降すべての土台のため)——ルート版と同じ
- `version`を`2.0.0`に上げる

### 7. `.kiro/agents/implementation-validator.md`(責務限定への書き換え)

**責務**: スペック準拠検証(requirements / design / tasklistと実装の整合性)のみに責務を限定する。

**実装の要点**:
- ルート新版の内容(責務と非責務・3観点・レポート形式・検証の姿勢)をベースに全面書き換えする
- frontmatterはKiro形式を維持する(`name` / `description` / `model: claude-sonnet-4` / `tools: ["read"]`)
- 非責務の委譲先表記を3段検証に翻訳する: 「コード品質・テスト・実挙動・セキュリティ/パフォーマンスは検証フローの他段(静的検証・実挙動確認)が担う」(/code-review・/verifyというClaude Code固有名は使わない)

### 8. `.kiro/steering/skill-doc-writing.md`(追記)

**責務**: 「LLM向け定義ファイルの記述規約」の反映。

**実装の要点**:
- 末尾に新セクション「LLM向け定義ファイルの記述規約」を追加する(対象: フック・steeringファイル・エージェント定義)
- ルート版の2規約を反映する: 「設計の具体形を転記する」(良い例/悪い例含む)・「既存ファイルの用語に引っ張られない」

### 9. `.kiro/steering/process.md`(追記+規律の修正)

**責務**: 「スタックPRの扱い」の反映と、tasklist管理ルールの実行後マーク規律への整合。

**実装の要点**:
- 「PR・リリースフロー」セクションに「スタックPRの扱い」(ルート版process.mdの3項目)を追加する
- 「tasklist.md の管理ルール」の「タスク開始時に `[ ]` → `[x]` へ更新する」を「タスク完了時(操作の実行後)に `[ ]` → `[x]` へ更新する」に修正する

### 10. `docs/functional-design.md`(概念マッピング表の更新)

**責務**: Kiro概念マッピング表・フック設計を実態に合わせる。

**実装の要点**:
- 概念マッピング表の更新: フック行(トリガー種別の拡充: agentStop等)・スラッシュコマンド行/スキル行/サブエージェント行(🔲未実装→✅実装済み)・memory行(適用しない判断と根拠)
- 「定義するフック(案)」表を実際に定義したフック(tasklist-check / add-feature / setup-project)に置き換える
- 記憶層を適用しない判断の根拠(Kiroにネイティブメモリ機構がない・既存代替設計で充足)を明文化する

### 11. `kiro-template/README.md`・`ONBOARDING.md`(整合確認)

**責務**: 変更内容(新フック・新steering)との矛盾解消。

**実装の要点**:
- ファイル一覧・使い方の記述が今回の変更と矛盾する箇所のみ最小限更新する(全面書き換えはしない)

## データフロー

### 実装全体の流れ
```
1. 規律系の小変更(コンポーネント2, 3, 9の修正部分)
2. フック刷新(コンポーネント1, 5, 6)
3. steering新設・追記(コンポーネント4, 5のskill-add-feature, 8)
4. エージェント書き換え(コンポーネント7)
5. docs・README整合(コンポーネント10, 11)
6. 検証(下記テスト戦略)
7. コミット・PR作成
```

## エラーハンドリング戦略

該当なし(コード実装を伴わないテンプレートファイルの翻訳作業)。フックはKiro側の機構で実行されるため、プロンプト内に「対象ファイルがない場合は何もしない」等のフェイルセーフ指示を含める。

## テスト戦略

### 段1: 静的検証
- `uv run pytest` / `uv run ruff check` / `uv run basedpyright`(ルートの既存テストが壊れていないことの確認)
- `.kiro/hooks/*.json`全ファイルのJSONパース検証(`python3 -c "import json; json.load(...)"`)

### 段2: 実挙動検証
- 本変更はKiro IDE上で動くテンプレート定義(JSON/Markdown)であり、本環境にKiro IDEがないため**実行観察は不可**。代替として以下を行い、tasklist.mdにスキップと代替内容を記録する:
  - フックのトリガー種別・アクション形式がKiro公式ドキュメントの記載と整合していることの確認
  - skill-distill.mdの手順を本リポジトリの`.steering/`に対して机上トレースし、手順が実行可能であることの確認

### 段3: コードレビュー
- `Skill('code-review')`を実行し、正当なfindingsを修正する

### 段4: スペック準拠検証
- `implementation-validator`と`doc-reviewer`(docs/functional-design.mdを変更するため)を並列起動する

## 依存ライブラリ

追加なし。

## ディレクトリ構造

```
kiro-template/
├── .kiro/
│   ├── hooks/
│   │   ├── tasklist-check.json      [置き換え: agentStopトリガー化]
│   │   ├── add-feature.json         [刷新: skill-add-feature参照方式]
│   │   └── setup-project.json       [更新: 承認ゲート明示]
│   ├── agents/
│   │   └── implementation-validator.md [書き換え: スペック準拠検証に限定]
│   └── steering/
│       ├── skill-add-feature.md     [新設: add-featureフロー詳細手順]
│       ├── skill-distill.md         [新設: 蒸留手順]
│       ├── skill-sdd-guide.md       [修正+追記: 実行後マーク規律]
│       ├── skill-doc-writing.md     [追記: LLM向け定義ファイル記述規約]
│       └── process.md               [追記+修正: スタックPR・実行後マーク]
├── .steering/_template/
│   └── tasklist.md                  [1行追記: 実行後マーク規律]
├── README.md                        [整合確認・必要時のみ更新]
└── ONBOARDING.md                    [整合確認・必要時のみ更新]

docs/
└── functional-design.md             [更新: 概念マッピング表・フック一覧・記憶層判断]
```

## 実装の順序

1. コンポーネント2, 3, 9(規律系の小変更)
2. コンポーネント1, 6(既存フックの更新)
3. コンポーネント5(add-feature.json + skill-add-feature.md)
4. コンポーネント4(skill-distill.md)
5. コンポーネント7(implementation-validator.md)
6. コンポーネント8(skill-doc-writing.md)
7. コンポーネント10, 11(docs/README整合)
8. 検証(段1〜4)
9. 振り返り・コミット・PR作成

## セキュリティ考慮事項

- シェルコマンドアクションのフックは今回導入しない(agentプロンプトのみ)。外部通信・ローカル実行を伴う変更はない

## パフォーマンス考慮事項

- agentStopフックは応答完了ごとに発火しエージェントループを消費する(Kiroのクレジット消費に留意)。プロンプトに「未完了タスクがない場合は何もしない」を明記し、無駄なループを避ける

## 将来の拡張性

- KiroがagentStopトリガーのブロック能力(シェルコマンド非ゼロ終了での継続強制)を文書化したら、ルートの`check_tasklist_complete.py`相当のスクリプト方式に強化できる(Issue #42の調査結果として記録)
- codex-templateへの展開(Issue #43)では本設計の翻訳原則(コマンド→フック・スキル→steering等の対応表)が再利用できる
