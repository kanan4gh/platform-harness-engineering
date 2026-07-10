# 設計書

## アーキテクチャ概要

本作業はコード実装ではなく、本家 `platform-harness`(upstream remote, fetch済み)との差分を検証済みのファイル単位で反映する「ドキュメント・設定ファイルの同期」である。各ファイルを次の2パターンに分類して扱う。

```
パターンA: 全面採用(upstreamの内容をそのまま採用してよいファイル)
  → git show upstream/main:<path> でupstreamの内容を取得し、そのまま書き込む(必要なら軽微な調整)

パターンB: 部分反映(本リポジトリ固有の内容と混在しており、差分ハンク単位で適用するファイル)
  → Editツールで該当ハンクのみを反映し、本リポジトリ固有部分は保持する
```

事前の差分精査により、CLAUDE.md・.gitignore・.claude/settings.json・docs/ideas/harness-engineering.mdの4ファイルは
「`git diff main upstream/main -- <path>` が差分の全量」であることを確認済み(=このリポジトリ固有の他の差分は存在しない)。
したがって部分反映(パターンB)でも、確認済みのハンクだけを適用すれば過不足なく同期できる。

## コンポーネント設計

### 1. CLAUDE.md(パターンB)

**責務**:
- 汎用層のドキュメント承認フロー記述をAskUserQuestion方式に更新する
- 「### 記憶層の運用」セクションを追加する

**実装の要点**:
- 「🚨 このリポジトリへの改善リクエストを受けたときの必須確認」セクションは本リポジトリ固有のプロダクト固有層であり、upstreamには存在しないだけで削除対象ではない。**このセクションは変更しない**
- 「### 記憶層の運用」セクションは「### 永続的ドキュメント一覧(`docs/`)」の直後・「### 初回セットアップ」の直前に挿入する(upstreamでの相対位置と同じ)

### 2. .claude/settings.json(パターンB)

**責務**:
- 安全な既定(`defaultMode`未設定)への変更
- allowリストの拡張
- Stop/PostToolUseフックの登録

**実装の要点**:
- 現状は `"hooks": {}` のみなので、upstreamのhooks定義をそのまま追加する
- JSON全体を書き直すのではなく、既存のSkill許可リストを保持したまま追記する(このリポジトリ固有の追加許可が将来増えても壊れないよう、Editで差分適用する)

### 3. フック本体・テスト・distillスキル(パターンA・新規追加)

**責務**:
- `.claude/hooks/check_tasklist_complete.py`: 最新の日付接頭辞ステアリングディレクトリの `tasklist.md` に `- [ ]` が残っていればStopをブロックする
- `.claude/hooks/remind_tasklist_update.py`: 実装ファイル編集が5回連続してもtasklist.mdが更新されなければ非強制のリマインドを注入する
- `.claude/skills/distill/SKILL.md`: `.steering/*/tasklist.md` の振り返りを横断収集し、環流3基準(普遍性・再現性・抽象性)で分類する
- `tests/hooks/test_*.py`: 上記2フックのユニットテスト

**実装の要点**:
- upstreamの内容をそのまま採用する(このリポジトリ固有の改変は不要)
- `.claude/hooks/state/` はフックの揮発状態の保存先であり、Git管理対象外にする(.gitignoreで対応)

### 4. pyproject.toml(パターンA・新規追加・軽微調整)

**責務**:
- `uv run pytest` / `uv run ruff check` / `uv run basedpyright` の実行基盤を提供する

**実装の要点**:
- upstreamの内容をベースに、`name` を `platform-harness-engineering`、`description` を本リポジトリの実態(テンプレートジェネレーター)に合わせて書き換える
- 依存関係(pytest/ruff/basedpyright)・pytest/ruff/basedpyright設定はupstreamのまま採用する
- `uv.lock` は直接コピーせず、`uv sync` で本リポジトリ用に再生成する(タスクリストの検証段で実行)

### 5. .claude/commands/add-feature.md(パターンA・全面採用)

**責務**:
- worktree隔離・Explore/Plan委譲・計画承認ゲート・4段検証・PR作成を含む新フローの提供

**実装の要点**:
- upstream版をそのまま採用する。検証コマンド(`uv run pytest`等)は既にこのリポジトリの技術スタック(CLAUDE.md技術スタック固有層)と一致しているため変更不要
- このコマンドは本リポジトリ自体のエンジニアリング作業(kiro-template/codex-template開発)で使うものであり、テンプレート内のadd-feature.md(kiro-template/codex-template配下)とは別物。今回はスコープ外である配下テンプレートには触れない

### 6. .claude/commands/setup-project.md(パターンA・全面採用)

**責務**:
- 各ドキュメント作成ステップに承認ゲート(AskUserQuestion)を明示する

**実装の要点**:
- upstreamとの差分は追記のみ(21 ins / 4 del)であり、他の差異がないことを確認済み。upstream版で上書きしてよい

### 7. .claude/agents/implementation-validator.md(パターンA・全面採用)

**責務**:
- スペック準拠検証(requirements/design/tasklistとの整合性)のみに責務を限定する

**実装の要点**:
- コード品質・テスト・セキュリティ・パフォーマンスの観点は4段検証の他段(静的検証・/verify・/code-review)に委ねる設計に変更されている。upstream版をそのまま採用する

### 8. .claude/skills/steering/SKILL.md(パターンA・全面採用)

**責務**:
- ステアリングファイル作成・実装・振り返りの3モードを提供し、「完了マークは操作の実行後に付ける」規律を明記する

**実装の要点**:
- upstream版は大幅に簡素化されており、フック(hooks/)による機械的強制を前提とした記述になっている。upstream版をそのまま採用する

### 9. .claude/README.md(パターンA・全面採用)

**責務**:
- `.claude/` 配下の構成・設定・モデル配分方針の説明

**実装の要点**:
- 上記1〜8の変更を正しく反映した内容になっているため、upstream版をそのまま採用する

### 10. .gitignore(パターンB)

**責務**:
- `.steering/*`(`example/`を除く)の除外
- `.claude/hooks/state/` の除外

**実装の要点**:
- 既存の内容(Python関連の除外・settings.local.json)は保持したまま末尾に追記する

### 11. docs/ideas/harness-engineering.md(パターンB)

**責務**:
- 「/harness-doctor構想」「Stopフック改善構想」の2セクションを追記する

**実装の要点**:
- ファイル末尾にそのまま追記する(upstreamでの追記内容と同一)

## データフロー

### 同期作業全体の流れ
```
1. パターンAのファイル(新規追加・全面採用)を先に反映する
   - 新規ファイルはgit show upstream/main:<path>で取得して書き込む
   - 全面採用ファイルも同様にupstream内容で上書きする
2. パターンBのファイル(部分反映)をEditツールで反映する
   - CLAUDE.md / .claude/settings.json / .gitignore / docs/ideas/harness-engineering.md
3. pyproject.toml作成後、uv syncを実行してuv.lockを生成する
4. uv run pytest / uv run ruff check / uv run basedpyright で新規フック・テストを検証する
5. git diff main upstream/main で対象ファイルの差分が(対象外ファイルを除き)解消されたことを確認する
```

## エラーハンドリング戦略

該当なし(コード実装を伴わないドキュメント・設定同期のため)。ただしフックスクリプト自体はupstreamの設計(fail-open: 例外時はブロックせず終了)をそのまま踏襲する。

## テスト戦略

### ユニットテスト
- `tests/hooks/test_check_tasklist_complete.py`(upstreamのテストをそのまま採用し、`uv run pytest` でパスすることを確認)
- `tests/hooks/test_remind_tasklist_update.py`(同上)

### 統合テスト(実挙動確認)
- Stopフック: 意図的に `- [ ]` を含むダミーのステアリングディレクトリを用意し、Stopイベントをシミュレートしてブロックされることを確認する(または既存テストの実行結果で代替する)
- 設定の妥当性: `.claude/settings.json` がJSONとしてパース可能であることを確認する

## 依存ライブラリ

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
    "ruff>=0.8",
    "basedpyright>=1.20",
]
```

upstreamと同一。本リポジトリのルートに初めて導入する。

## ディレクトリ構造

```
platform-harness-engineering/
├── CLAUDE.md                          [変更: パターンB]
├── .gitignore                         [変更: パターンB]
├── pyproject.toml                     [新規: パターンA(軽微調整)]
├── uv.lock                            [新規: uv syncで生成]
├── .claude/
│   ├── README.md                      [変更: パターンA]
│   ├── settings.json                  [変更: パターンB]
│   ├── hooks/
│   │   ├── check_tasklist_complete.py [新規: パターンA]
│   │   └── remind_tasklist_update.py  [新規: パターンA]
│   ├── commands/
│   │   ├── add-feature.md             [変更: パターンA]
│   │   └── setup-project.md           [変更: パターンA]
│   ├── agents/
│   │   └── implementation-validator.md [変更: パターンA]
│   └── skills/
│       ├── steering/SKILL.md          [変更: パターンA]
│       └── distill/SKILL.md           [新規: パターンA]
├── tests/
│   └── hooks/
│       ├── test_check_tasklist_complete.py [新規: パターンA]
│       └── test_remind_tasklist_update.py  [新規: パターンA]
└── docs/
    └── ideas/
        └── harness-engineering.md      [変更: パターンB]
```

(kiro-template/・codex-template/ 配下は変更しない)

## 実装の順序

1. 新規ファイル(パターンA)を一括追加: hooks/*.py・distill/SKILL.md・tests/hooks/*.py・pyproject.toml
2. 全面採用ファイル(パターンA)を上書き: add-feature.md・setup-project.md・implementation-validator.md・steering/SKILL.md・.claude/README.md
3. 部分反映ファイル(パターンB)をEdit: CLAUDE.md・.claude/settings.json・.gitignore・docs/ideas/harness-engineering.md
4. `uv sync` で `uv.lock` を生成
5. `uv run pytest` / `uv run ruff check` / `uv run basedpyright` で検証
6. `git diff main upstream/main -- CLAUDE.md .claude docs/ideas/harness-engineering.md .gitignore` で残差分が意図した対象外のみであることを確認
7. コミット・PR作成(フィーチャーブランチ `feature/sync-harness-core-v040` )

## セキュリティ考慮事項

- 新規フックは標準ライブラリのみを使用し外部通信を行わない(upstreamの設計方針を踏襲)
- `defaultMode: bypassPermissions` の削除により、書き込み・外部操作系のパーミッション確認が既定で有効化される(安全性向上)

## パフォーマンス考慮事項

該当なし。

## 将来の拡張性

- 今回の同期完了後、`kiro-template/`・`codex-template/` への展開(README.md開発フロー「3.」)を別Issue・別ステアリングとして実施する
- `docs/ideas/harness-engineering.md` に追記される `/harness-doctor` 構想は、将来的にスキル化する際の起点になる
