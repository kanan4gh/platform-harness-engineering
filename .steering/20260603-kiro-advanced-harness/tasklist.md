# タスクリスト

## 🚨 タスク完全完了の原則

**全タスクが `[x]` になるまで作業を継続すること**

---

## フェーズ1: userTriggered hooks の実装

- [x] `kiro-template/.kiro/hooks/add-feature.json` を作成する
  - [x] `when.type: "userTriggered"` で定義する
  - [x] プロンプトに「機能名を問い返す」「承認ゲート付き SDD フロー」を含める
  - [x] `version: "1.0.0"` を含める
- [x] `kiro-template/.kiro/hooks/setup-project.json` を作成する
  - [x] `when.type: "userTriggered"` で定義する
  - [x] プロンプトに「1ファイルずつ・承認を得てから次へ」を含める
  - [x] `version: "1.0.0"` を含める

## フェーズ2: 品質チェック

- [x] `docs/architecture.md` の「テンプレートに含めるフック」テーブルを更新する（`add-feature.json` と `setup-project.json` を追加）
- [x] `docs/repository-structure.md` の `kiro-template/.kiro/hooks/` セクションを更新する

## フェーズ3: 振り返り

- [x] 振り返りをこのファイルの下部に記録する

---

## 将来計画（本スペックのスコープ外・漏れ防止のため記録）

### フェーズ2 スペック: inclusion: manual steering（スキル相当）
- `kiro-template/.kiro/steering/skill-sdd-guide.md` — tasklist 進捗管理の詳細手順
- `kiro-template/.kiro/steering/skill-doc-writing.md` — ドキュメント記入ガイド

### フェーズ3 スペック: カスタムエージェント（サブエージェント相当）
- `kiro-template/.kiro/agents/implementation-validator.md`
- `kiro-template/.kiro/agents/doc-reviewer.md`

---

## 実装後の振り返り

### 実装完了日
2026-06-03

### 計画と実績の差分
- 計画通り。差分なし。

### 学んだこと
- `userTriggered` hook のプロンプトに承認ゲートを明示することで、Kiro が一気に処理を進めすぎる問題に対処できる
- `setup-project` は Kiro との会話でも代替できることが判明していたが、hook として定義することで再現性と一貫性が高まる

### 次回への改善提案
- フェーズ2（`inclusion: manual` スキル群）を実装後、`add-feature.json` のプロンプトから `#skill-sdd-guide` を参照する文言を追加する
- Kiro 実環境で `userTriggered` hook の起動方法（Hook UI / コマンドパレット）を動作確認する

### リリース判断

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes |
| 未解決の重大バグはないか | なし（Kiro 実環境での動作確認は次フェーズ） |
| 適切なバージョン種別 | リリース不要（ハーネス全体でまとめてリリース） |

**提案**: フェーズ2（manual steering）の実装に進む前に、Kiro で `userTriggered` hook の動作確認を行う。
