# 設計書

## アーキテクチャ概要

kiro展開(`.steering/20260710-deploy-harness-core-v040-kiro/design.md`)の翻訳原則対応表をCodex CLI向けに更新して適用する。kiroとの最大の違いは、CodexのフックがClaude Codeとほぼ同一プロトコルのため**プロンプト翻訳ではなく機構移植**ができる点。

```
Claude Code機構              → Codex CLI機構(移植先)
─────────────────────────────────────────────────
Stopフック(Python・ブロック)  → .codex/hooks.json Stop + Pythonスクリプト(decision: blockで継続強制)
PostToolUseリマインド         → 移植しない(Stopフックで担保。ペイロード仕様未確認)
スラッシュコマンド            → .agents/skills/*/SKILL.md($メンション/自動選択) + AGENTS.mdから誘導
スキル(SKILL.md)             → .agents/skills/*/SKILL.md(ほぼ同形式)
サブエージェント              → .codex/agents/*.toml
worktree隔離                 → フィーチャーブランチ必須(Codexにworktreeツールなし)
4段検証                      → 3段検証(静的検証/実挙動確認/implementation-validator)
ネイティブ永続メモリ          → Memories機構(運用方針をAGENTS.mdに記載)
```

## コンポーネント設計

### 1. `.codex/hooks/check_tasklist_complete.py`(新設・ルートから適合移植)

**責務**: Stopイベント時、最新ステアリングディレクトリのtasklist.mdに`- [ ]`が残っていれば`{"decision": "block", "reason": ...}`で継続を強制する。

**実装の要点**(ルート版からの変更点のみ):
- プロジェクトルート解決: `CLAUDE_PROJECT_DIR`環境変数 → stdinペイロードの`cwd`フィールド(なければ`Path.cwd()`)
- ループ防止: `stop_hook_active`フィールドの代わりに、状態ファイル(`.codex/hooks/state/stop_guard.json`)で「同一tasklist内容(SHA-256)に対する連続ブロック回数」を記録し、3回に達したらfail-open(ブロックしない)。tasklist内容が変わればカウンタをリセット
- それ以外(検出正規表現・日付接頭辞パターン・reason文言・fail-open方針)はルート版と同一

### 2. `.codex/hooks.json`(新設)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .codex/hooks/check_tasklist_complete.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

- 相対パスはcwd(プロジェクトルート)基準。実機で解決されない場合に備え、実機確認を残す

### 3. `tests/hooks/test_codex_check_tasklist_complete.py`(新設・本リポジトリのテスト)

- ルートの`test_check_tasklist_complete.py`をベースに、codex版の差分(cwdフィールド解決・連続ブロックガード)のテストを追加
- ガードのテスト: 同一内容3回でblockが止まる / 内容変更でカウンタリセット

### 4. `.agents/skills/add-feature/SKILL.md`(新設)

**責務**: 計画承認ゲート1箇所・承認後無停止のSDDワークフロー。

**実装の要点**:
- frontmatter: `name: add-feature`、`description`(起動条件を明記: 「add-featureを実行して」「新機能を追加して」等)
- 構成はkiro版skill-add-feature.mdと同一の8ステップ(ブランチ→Issue→スペック→計画承認→実装ループ→3段検証→振り返り→PR)。Codex固有の調整:
  - ブランチ作成・Issue作成は`git`/`gh`コマンドをエージェント自身が実行する(CodexはCLI環境)
  - 段3のスペック準拠検証は「`.codex/agents/implementation-validator.toml`のエージェントに委譲する。サブエージェント機構が利用できない環境では、同ファイルの検証観点をメインエージェントが自分で適用する」とフォールバックを明記
  - 承認ゲートは「承認して実装開始 / 修正を指示する / 中止する」のテキスト3択提示

### 5. `.agents/skills/setup-project/SKILL.md`(新設)

- ルート版setup-project.mdの承認ゲート(3択、PRDはスキップ不可)を反映。6ドキュメント作成→AGENTS.mdの3セクション更新の流れは現行AGENTS.mdワークフローセクションを継承

### 6. `.agents/skills/distill/SKILL.md`(新設)

- ルート版distillの処理手順・環流3基準・レポート形式を維持
- 翻訳: `Glob(...)` → 「`.steering/`直下の`YYYYMMDD-`接頭辞ディレクトリ(パターン: `[0-9]*-*`)を列挙」/ 「ネイティブ永続メモリへの保存を提案」→「Memories機構が有効ならその記憶に委ね、無効環境ではAGENTS.mdプロダクト定義セクションへの記録を提案」

### 7. `.codex/agents/implementation-validator.toml`(新設)

```toml
name = "implementation-validator"
description = "実装と作業スペック(requirements/design/tasklist)の整合性を検証するスペック準拠検証エージェント"
developer_instructions = """(ルート新版implementation-validator.mdの本文: 責務と非責務・3観点・レポート形式・検証の姿勢。非責務の委譲先は3段検証表記)"""
```

- `model`は指定しない(利用者の既定を継承)

### 8. `AGENTS.md`(更新)

- **tasklist管理ルール**: 「開始時マーク」→「完了時(実行後)マーク」修正+実行後マーク規律+「Stopフックによる機械的担保」の説明追加
- **PR・リリースフロー**: 「スタックPRの扱い」3項目を追記
- **プロセス原則に小セクション追加**: 「LLM向け定義ファイルの記述規約」(設計の具体形を転記/既存用語に引っ張られない)
- **記憶層の運用セクション追加**(プロダクト定義の後): Memories機構の運用方針(書くべき/書かないもの・EEA/UK/スイスでは利用不可のためAGENTS.md記載で代替)
- **ワークフローセクション**: add-feature/setup-projectの手順詳細を削除し、`.agents/skills/`への誘導+「承認ゲートは計画の承認1箇所」の要点のみに簡素化
- 冒頭コメントの「セクション5(ワークフロー)は編集不要」等の案内は実態に合わせて維持

### 9. `_template/tasklist.md`(1行追記)

- ルート版と同一文言の実行後マーク規律

### 10. `README.md`・`ONBOARDING.md`(更新)

- 構成ツリーに`.codex/`(hooks/agents)・`.agents/skills/`を追加
- **「初回にプロジェクトをtrustする」手順と、trustしないと`.codex/`層(フック・エージェント)がロードされない旨を明記**
- add-featureフロー説明を「計画承認1箇所・承認後無停止」に更新
- Stopフック(tasklist規律の機械的強制)の説明とトラブルシュートFAQを追加

### 11. `.gitignore`調整

- ルートリポジトリの`.gitignore`に`codex-template/.codex/hooks/state/`は不要(テンプレート内で完結)→ codex-template側にstate除外の`.gitignore`を新設(`.codex/hooks/state/`)

## データフロー

### Stopフックの動作
```
1. Codexが応答を終えようとする(Stopイベント)
2. hooks.jsonに登録されたcheck_tasklist_complete.pyがstdinでペイロード(session_id/cwd/...)を受け取る
3. cwd基準で最新の.steering/YYYYMMDD-*/tasklist.mdを特定
4. `- [ ]`が残存 → 連続ブロックガードを確認 → 3回未満なら {"decision": "block", "reason": 未完了一覧} を出力(継続を強制)
5. 未完了なし/tasklist不在/ガード発動 → 何も出力せずexit 0(通常終了を許可)
```

## エラーハンドリング戦略

- フックはfail-open(例外時はブロックせず終了)をルート版から踏襲
- 連続ブロックガードにより、エージェントがタスクを消化できない異常時にも無限ループしない

## テスト戦略

- **段1**: `uv run pytest`(新テスト含む)/ `ruff check` / `basedpyright` / hooks.jsonのJSONパース / implementation-validator.tomlのTOMLパース(`tomllib`)
- **段2**: フックスクリプトを実際に起動(未完了あり/なし/ガード発動の3ケースをstdinシミュレートで実挙動観察)。SKILL.md群は成果物の目視+frontmatter検証。Codex実機確認はスコープ外(マージ後)
- **段3**: `Skill('code-review')`
- **段4**: `implementation-validator`+`doc-reviewer`(READMEなどドキュメント変更のため)

## 依存ライブラリ

追加なし(フックは標準ライブラリのみ)。

## ディレクトリ構造

```
codex-template/
├── .codex/
│   ├── hooks.json                      [新設]
│   ├── hooks/
│   │   └── check_tasklist_complete.py  [新設(ルートから適合移植)]
│   └── agents/
│       └── implementation-validator.toml [新設]
├── .agents/
│   └── skills/
│       ├── add-feature/SKILL.md        [新設]
│       ├── setup-project/SKILL.md      [新設]
│       └── distill/SKILL.md            [新設]
├── .gitignore                          [新設: .codex/hooks/state/]
├── .steering/_template/tasklist.md     [1行追記]
├── AGENTS.md                           [更新: 規律・スタックPR・記述規約・記憶層・ワークフロー簡素化]
├── README.md                           [更新]
└── ONBOARDING.md                       [更新]

tests/hooks/
└── test_codex_check_tasklist_complete.py [新設]
```

## 実装の順序

1. フック本体+hooks.json+テスト(コンポーネント1〜3)
2. スキル3種(4〜6)
3. implementation-validator.toml(7)
4. AGENTS.md・_template(8〜9)
5. README/ONBOARDING/.gitignore(10〜11)
6. 検証(段1〜4)
7. 振り返り・コミット・PR

## セキュリティ考慮事項

- フックは標準ライブラリのみ・外部通信なし(ルート方針踏襲)
- `.codex/`層はtrustが前提であることをREADMEに明記(利用者が意図せず未知のフックを実行しない設計はCodex側のtrust機構が担保)

## パフォーマンス考慮事項

- Stopフックはローカルスクリプト実行のみでLLM呼び出しを伴わない(kiroのagentStop+askAgent方式より低コスト)

## 将来の拡張性

- PostToolUseリマインドフックは、Codexのペイロード仕様確認後に追加可能(hooks.jsonへの1エントリ追加)
- Codexの`/review`等のビルトインが検証フローに組み込める場合、3段→4段への拡張余地がある
