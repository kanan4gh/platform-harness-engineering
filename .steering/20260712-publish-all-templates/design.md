# 設計書

## アーキテクチャ概要

単一ジョブ(`publish`)を、**テンプレート一覧を導出するジョブ**と**それをmatrixで受けて配布するジョブ**の2段構成に変える。

```
現行:
  publish (単一ジョブ)
    └ Determine template name → kiro固定(release時) / inputs.template(dispatch時)

変更後:
  determine-templates (軽量ジョブ)
    └ *-template/ を走査して JSON配列を出力
        - release            → ["kiro","codex"](全件)
        - dispatch (all)     → ["kiro","codex"](全件)
        - dispatch (kiro等)  → ["kiro"](単一)
  ↓ needs + matrix
  publish (matrix: template ∈ 上記配列, fail-fast: false)
    └ 既存の clone → rsync → commit/push → 配布先リリース作成 をテンプレートごとに実行
```

## コンポーネント設計

### 1. `determine-templates` ジョブ(新設)

**責務**: 配布対象テンプレート名のJSON配列をmatrix用に出力する。

**実装の要点**:
- `actions/checkout@v4` でリポジトリを取得する(ディレクトリ走査のため必要)
- 全件導出: `for d in *-template/; do ...; done` でディレクトリ名から `-template` を除去した名前を集め、`jq -R -s -c 'split("\n") | map(select(length > 0))'` でJSON配列化する
- 分岐:
  - `github.event_name == 'workflow_dispatch'` かつ `inputs.template != 'all'` → その単一テンプレートのみの配列 `["<name>"]`
  - それ以外(release / dispatch の `all`) → 全件
- 出力: `outputs.templates`(JSON文字列)
- テンプレートが1つも見つからない場合は `exit 1` で失敗させる(サイレントに何も配布しない事故を防ぐ)

### 2. `publish` ジョブ(matrix化)

**責務**: 1テンプレートを配布先リポジトリへ同期し、リリース時は配布先にもリリースを作成する。

**実装の要点**:
- `needs: determine-templates`
- ```yaml
  strategy:
    fail-fast: false
    matrix:
      template: ${{ fromJson(needs.determine-templates.outputs.templates) }}
  ```
- 既存の「Determine template name」ステップは削除し、以降のステップは `${{ matrix.template }}` を参照する
- clone / rsync / commit&push / 配布先リリース作成の各ステップのロジックは現行を維持する(変数の出所が `steps.template.outputs.name` → `matrix.template` に変わるだけ)
- **配布先リリース作成の冪等性**: matrixの複数ジョブがそれぞれ別リポジトリ(`platform-harness-for-<name>`)に作るため衝突しない。ただし同一タグでの再実行時に `gh release create` が失敗しうるため、既存タグがある場合はスキップする(`gh release view` で存在確認)。現行にはこの保護がないが、matrix化により再実行時の部分的やり直しが現実的になるため追加する

### 3. `workflow_dispatch` の入力変更

**実装の要点**:
- `template` の `description` を「配布するテンプレート名(kiro / codex)。`all` で全テンプレート」に更新
- `default` を `kiro` → `all` に変更する(手動発火でも配布漏れが起きない既定にする)

## データフロー

### リリース公開時
```
1. release published イベント発火
2. determine-templates: *-template/ を走査 → ["kiro","codex"] を出力
3. publish (matrix 2ジョブ並列):
   kiro  → platform-harness-for-kiro  を clone → kiro-template/ を rsync → push → リリース作成
   codex → platform-harness-for-codex を clone → codex-template/ を rsync → push → リリース作成
```

### 手動発火時(単一テンプレート再配布)
```
1. workflow_dispatch (template=codex)
2. determine-templates: ["codex"] を出力
3. publish (matrix 1ジョブ): codex のみ配布(リリース作成ステップは release イベントでないためスキップ)
```

## エラーハンドリング戦略

- `fail-fast: false` により、1テンプレートの配布失敗(配布先リポジトリ不在・権限エラー等)が他テンプレートの配布を巻き込まない
- テンプレートディレクトリが0件の場合は `determine-templates` を失敗させる(設定ミスをサイレントに握り潰さない)
- 配布先リリースが既存の場合はスキップして成功扱いにする(再実行時の安全性)

## テスト戦略

### 段1: 静的検証
- YAMLとしてパース可能であることを確認する(`python3 -c "import yaml; yaml.safe_load(...)"`。PyYAMLは検証用に一時的に使う)
- matrix導出ロジック(`for` + `jq`)をローカルシェルで実行し、`["kiro","codex"]` が得られることを確認する
- 既存のpytest/ruff/basedpyrightが壊れていないことを確認する

### 段2: 実挙動検証
- 本PRのブランチ上で `gh workflow run publish-template.yml --ref feature/publish-all-templates -f template=codex` を実行し、単一テンプレート配布が動作することを確認する
  - **注意**: 実際に配布先リポジトリへpushが走る。現在の配布先はmainの内容と同一(v0.6.0同期済み)であり、このブランチはワークフローのみの変更でテンプレート内容に差分がないため、**「No changes to publish.」で終了する**ことが期待される挙動(=配布先を汚さずに経路を検証できる)
- リリーストリガーでの全件配布(matrix 2ジョブ)は、次回リリース時に確認する(requirements.mdのスコープ外に記載)

### 段3: コードレビュー
### 段4: スペック準拠検証(implementation-validator)

## ディレクトリ構造

```
.github/workflows/
└── publish-template.yml   [変更: 2ジョブ構成・matrix化]

docs/
└── architecture.md        [確認: 配布フローの記述があれば更新]
```

## 実装の順序

1. `publish-template.yml` の書き換え(determine-templates ジョブ追加 + publish の matrix 化 + dispatch 既定値変更)
2. docs の記述確認・必要なら更新
3. 検証(段1〜4)
4. 振り返り・コミット・PR

## セキュリティ考慮事項

- `PUBLISH_PAT` の使い方は現行のまま(matrixジョブごとに同じsecretを参照する)。ログへの露出を避けるため、URLへの埋め込み方も現行を踏襲する
- `matrix.template` はワークフロー内で導出した値(`*-template/` のディレクトリ名)または `workflow_dispatch` の入力値。後者は任意文字列を取りうるため、`platform-harness-for-<入力>` のcloneが失敗するだけでコマンドインジェクションには至らない構造を維持する(変数はクォートして使用する)

## 将来の拡張性

- 新テンプレート(例: `cursor-template/`)を追加した場合、配布先リポジトリ `platform-harness-for-cursor` を作るだけで自動的に配布対象になる
