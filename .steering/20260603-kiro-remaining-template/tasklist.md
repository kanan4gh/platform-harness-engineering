# タスクリスト

## 🚨 タスク完全完了の原則

**このファイルの全タスクが完了するまで作業を継続すること**

### 必須ルール
- **全てのタスクを`[x]`にすること**
- 「時間の都合により別タスクとして実施予定」は禁止
- 未完了タスク（`[ ]`）を残したまま作業を終了しない

---

## フェーズ1: hooks の実装

- [x] `kiro-template/.kiro/hooks/` ディレクトリを作成する
- [x] `tasklist-check.json` を作成する
  - [x] Kiro hooks JSON 形式で記述する
  - [x] `tasklist.md` 保存をトリガーに設定する
  - [x] エージェントへの指示（prompt）を含める
  - [x] kiro-cli を必要とするコマンドを含めないことを確認する

## フェーズ2: mcp.json の実装

- [x] `kiro-template/.kiro/settings/` ディレクトリを作成する
- [x] `mcp.json` を作成する
  - [x] 有効な JSON 形式で `mcpServers` オブジェクトを含める
  - [x] 空のひな型として実装する

## フェーズ3: README.md の実装

- [x] `kiro-template/README.md` を作成する
  - [x] テンプレートの概要・目的を記述する
  - [x] "Use this template" でのリポジトリ複製手順を記述する
  - [x] Kiro でフォルダを開く手順を記述する
  - [x] 必須カスタマイズ項目（product.md・tech.md・structure.md）の手順を GUI 操作で記述する
  - [x] ブートストラップ・リリース・自走フェーズの説明を記述する
  - [x] kiro-cli コマンドが含まれていないことを確認する

## フェーズ4: 品質チェック

- [x] `docs/development-guidelines.md` のフックファイル品質基準を確認する
  - [x] kiro-cli を必要とするコマンドを含まないこと
  - [x] フックの目的と動作が明確であること
- [x] `docs/architecture.md` のドキュメント品質チェックリストを確認する
  - [x] README.md のセットアップ手順が GUI 操作のみで完結している
  - [x] ブートストラップ・リリース・自走フェーズの説明が README.md に記載されている

## フェーズ5: 振り返り

- [x] 振り返りをこのファイルの下部に記録する

---

## 実装後の振り返り

### 実装完了日
2026-06-03

### 計画と実績の差分

**計画と異なった点**:
- `tasklist-check.json` の `filePattern` に glob パターンのバグがあった（`**/.steering/**/tasklist.md` ではルート直下の `.steering/` にマッチしない）。バリデーターが検出し `.steering/**/tasklist.md` に修正した
- README に Claude CLI 移行ガイドと Spec mode 対処手順の追加が必要と判明（PRD 受け入れ条件の見落とし）

**新たに必要になったタスク**:
- なし（バリデーターのフィードバックで同一スプリント内に対処済み）

### 学んだこと

- glob パターンの `**/` プレフィックスは「ルート直下」を含まない実装が多い。`.steering/` のようにルート直下に固定されているディレクトリへのパターンは `**/.steering/` ではなく `.steering/` から書き始める
- README の品質基準は `docs/architecture.md` のチェックリストだけでなく `docs/product-requirements.md` の受け入れ条件も確認する必要がある

### 次回への改善提案
- hooks の filePattern は受け入れテスト（Kiro 実環境）で必ず動作確認する。Kiro の glob 実装は標準と異なる可能性がある
- `kiro-template/` が完成したので、次は `docs/repository-structure.md` を `kiro-template/` 構造に合わせて更新し、Bootstrap フェーズの成果物として記録する

### リリース判断

**前提条件の確認**:
- [x] 全ファイルが作成されている
- [x] 品質基準チェックが完了している
- [ ] `kiro-template/` 全体として受け入れテスト（シナリオ1〜4）を実施できる状態である（Kiro 実環境での確認は未実施）

**評価**:

| 観点 | 評価 |
|---|---|
| 今回の変更はユーザーにとって価値のあるまとまりか | Yes |
| 未解決の重大バグはないか | なし（filePattern バグは修正済み） |
| 適切なバージョン種別 | リリース不要（ハーネス全体の初回リリースにまとめる） |

**提案**:
`kiro-template/` の全コンポーネントが揃った。次は `docs/repository-structure.md` の更新と受け入れテスト実施により、初回リリースの準備を進める。
