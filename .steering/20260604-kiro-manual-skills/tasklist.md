# タスクリスト

## 🚨 タスク完全完了の原則

**全タスクが `[x]` になるまで作業を継続すること**

---

## フェーズ1: inclusion: manual steering ファイルの実装

- [x] `kiro-template/.kiro/steering/skill-sdd-guide.md` を作成する
  - [x] `inclusion: manual` frontmatter を設定する
  - [x] tasklist.md 管理ルール（開始時・完了時の更新手順）を記述する
  - [x] タスク完全完了の原則（スキップ禁止・技術的スキップの条件と記述形式）を記述する
  - [x] フェーズ完了時の確認手順・振り返りの記入内容を記述する
- [x] `kiro-template/.kiro/steering/skill-doc-writing.md` を作成する
  - [x] `inclusion: manual` frontmatter を設定する
  - [x] 各ドキュメント（product-requirements・functional-design・architecture・repository-structure・development-guidelines・glossary）の記入ガイドをセクションごとに記述する
- [x] `kiro-template/.kiro/hooks/add-feature.json` のプロンプトを更新する
  - [x] `#skill-sdd-guide` を参照する文言をプロンプトに追加する

## フェーズ2: 品質チェック

- [x] 両ファイルに `inclusion: manual` が設定されていることを確認する
- [x] `skill-sdd-guide.md` の内容が Claude Code `skills/steering/` の主要ルールを網羅していることを確認する

## フェーズ3: 振り返り

- [x] 振り返りをこのファイルの下部に記録する

---

## 実装後の振り返り

### 実装完了日
2026-06-04

### 計画と実績の差分
- 計画通り3ファイルの変更で完了。差分なし。
- `skill-sdd-guide.md` の内容は Claude Code steering スキルの主要ルールをすべて網羅できた。

### 学んだこと
- Kiro の `inclusion: manual` は Claude Code の `skills/` に相当し、`#ファイル名` で明示参照する仕組みが有効に機能する。
- steering ファイルを manual にすることでコンテキスト汚染を防ぎつつ、必要時のみ詳細ルールをロードできる設計が確認できた。
- `add-feature.json` のプロンプトに `#skill-sdd-guide` を埋め込むことで、フック起動時に自動参照させられる。

### 次回への改善提案
- Phase 3（カスタムエージェント）実装後に Kiro での受け入れテストを実施し、`#skill-sdd-guide` 参照が実際に動作するか確認する。
- `skill-doc-writing.md` も `add-feature.json` または `setup-project.json` から自動参照させることを検討する。

### リリース判断

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes |
| 未解決の重大バグはないか | なし |
| 適切なバージョン種別 | MINOR |

**提案**: `inclusion: manual` スキルのポートが完了した単体でリリース価値あり。Phase 3（エージェント）と合わせて MINOR リリースを推奨。
