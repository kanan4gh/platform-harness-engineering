# 要求内容

## 概要

`setup-project` フックへの導線を強化し、新規プロジェクト開始時に `add-feature` より先に実行されるよう README.md と ONBOARDING.md を改善する。

## 背景

Kiro ユーザーから「プロジェクト開始時に `setup-project` をスキップして、steering ファイルを手動で書いた後すぐに `add-feature` に進んでしまう」というフィードバックが複数あった（プロジェクトオーナーも同様の経験あり）。

現状の README.md クイックスタートは以下のフローになっており、`setup-project` への導線がない:

1. テンプレート複製
2. Kiro で開く
3. **steering ファイルを手動で編集**（product.md, tech.md, structure.md）
4. 最初の機能スペックを作成 → `add-feature`

`setup-project` フックは「docs/ の 6 ファイル作成 + steering ファイル更新」を両方担うため、手順 3 を置き換えられるはずだが活用されていない。

関連 Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/18

## ユースケースの軸

> Kiro ユーザーが新規プロジェクトを開始するとき、`setup-project` フックを最初のステップとして実行し、docs/ と steering ファイルを正しく揃えてから機能開発に入れる。

## 実装対象の機能

### 1. README.md クイックスタートの修正

- Step 3 を「steering ファイルを手動で編集」から「`setup-project` を実行」に変更
- `setup-project` が docs/ 作成 + steering 更新を両方担うことを明示
- 手動編集の説明を削除（または補足扱いに格下げ）

### 2. ONBOARDING.md セットアップセクションの修正

- Section 2「ステップ 2: steering ファイルをカスタマイズする」を `setup-project` 実行フローに変更
- 手動編集サンプル（tech.md の記入例等）を削除または後段の補足へ移動
- `setup-project` 実行後の動作確認への自然な流れを作る

## 受け入れ条件

### README.md

- [ ] クイックスタートの Step 3 が `setup-project` 実行の指示になっている
- [ ] `setup-project` が docs/ 6 ファイルと steering ファイルを両方作成することが読み取れる
- [ ] 手動で steering ファイルを編集する手順が主フローから消えている

### ONBOARDING.md

- [ ] Section 2 が `setup-project` 実行フローになっている
- [ ] 手動編集の記入例サンプルが主フローから消えている（または補足として明確に格下げされている）
- [ ] `setup-project` 実行 → 動作確認（Section 3）への流れが自然につながっている

## スコープ外

- `setup-project` フック自体のプロンプト修正
- `add-feature` フックへのガード追加（docs/ の存在チェック等）
- docs/ テンプレートファイルの内容変更

## 参照ドキュメント

- `kiro-template/README.md` — 修正対象
- `kiro-template/ONBOARDING.md` — 修正対象
- `kiro-template/.kiro/hooks/setup-project.json` — 参照（フックの振る舞い確認）
