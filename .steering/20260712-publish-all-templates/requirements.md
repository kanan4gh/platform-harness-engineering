# 要求内容

## 概要

リリース公開時に全テンプレート(kiro・codex)が自動配布されるよう `publish-template.yml` をmatrix化する。

## 背景

- 関連Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/48
- 現行の `publish-template.yml` はリリーストリガー時の配布対象が `kiro` にハードコードされている(L26: `echo "name=kiro" >> $GITHUB_OUTPUT`)
- 実例: v0.6.0(codex-template展開)のリリースでは自動配布はkiroのみ実行され、codexは `gh workflow run -f template=codex` の手動発火で同期した
- テンプレートが2つに増えた現在、リリースのたびに片方の配布を忘れるリスクが常在する

## ユースケースの軸

> **メンテナがリリースを作成するだけで、全テンプレートが対応する配布先リポジトリへ同期される。**

## 実装対象の機能

### 1. 配布対象の動的導出
- `*-template/` ディレクトリ名からテンプレート名(kiro・codex)を導出し、JSON配列としてmatrixに渡す
- テンプレートを追加してもワークフローの修正が不要になる

### 2. matrix化による並列配布
- リリース公開時: 導出した全テンプレートを配布する
- `fail-fast: false` により、1テンプレートの失敗が他の配布を巻き込まない

### 3. workflow_dispatchの維持・改善
- 単一テンプレートの再配布は従来どおり可能にする
- 既定値は全テンプレート(`all`)とし、手動発火でも配布漏れが起きないようにする

### 4. 既存挙動の維持
- 差分がなければ何もしない(`git diff --cached --quiet`)
- リリーストリガー時は配布先リポジトリにもリリースを作成する(各テンプレートに対して実行)

## 受け入れ条件

- [ ] リリース公開時、kiro・codex の両方が配布先へ同期される(matrixで2ジョブ実行される)
- [ ] `*-template/` を追加すればワークフロー修正なしで配布対象に含まれる
- [ ] `workflow_dispatch` で単一テンプレート(`kiro` / `codex`)の再配布ができる
- [ ] `workflow_dispatch` の既定値(`all`)で全テンプレートが配布される
- [ ] 差分がない場合に何もしない挙動が維持されている
- [ ] リリーストリガー時に配布先リポジトリのリリースが作成される挙動が維持されている
- [ ] ワークフローYAMLが構文的に妥当である(パース検証)

## スコープ外

- 配布先リポジトリ(`platform-harness-for-*`)側の変更
- テンプレートの内容変更
- 配布先リポジトリが存在しない新テンプレートの自動作成(存在しない場合は当該matrixジョブが失敗する。`fail-fast: false` により他テンプレートの配布は継続される)
- 実際のリリース発火による本番検証(次回リリース時に確認する。本PRでは `workflow_dispatch` による動作確認まで)

## 参照ドキュメント

- Issue #48
- `.github/workflows/publish-template.yml`(変更対象)
- `docs/architecture.md` / `docs/repository-structure.md`
