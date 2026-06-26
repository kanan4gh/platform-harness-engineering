# 要求内容

## 概要

テンプレートとして複製したときに、README.md がこのハーネス固有の内容になってしまう問題を解消する。

## 背景

`platform-harness-engineering` を "Use this template" で複製すると、README.md がこのリポジトリ（ハーネスの作業場）向けの説明のままになる。新しいプロジェクトでは、自分のプロジェクト用の README として育てていきたい。

関連 Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/31

## ユースケースの軸

> **テンプレート利用者が、自分のプロジェクトの README をゼロから育てられるようになる。**

## 実装対象の機能

### 1. README.md のプレースホルダー化

- 現在の内容をプレースホルダー（最小構成）に差し替える
- プロジェクト名・説明を埋めるだけの最小構成
- `docs/harness-guide.md` へのリンクを記載

### 2. harness-guide.md の作成

- 現在の README.md の内容を `docs/harness-guide.md` として保存
- このハーネスの概要・開発フロー・関連リポジトリを記録

## 受け入れ条件

### README.md のプレースホルダー化
- [ ] README.md がプロジェクト名とプレースホルダーの説明のみになっている
- [ ] `docs/harness-guide.md` へのリンクが含まれている
- [ ] テンプレート利用者がそのまま書き換えて使える構成になっている

### harness-guide.md の作成
- [ ] `docs/harness-guide.md` に現在の README.md の内容が保存されている
- [ ] ハーネスの説明として完結した内容になっている

## スコープ外

- kiro-template/ 内の README の変更
- CLAUDE.md の変更
