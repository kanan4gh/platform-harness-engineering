# 要求内容

## 概要

`docs/harness-guide.md` の内容を、Kiro 固有の記述からハーネス自体の説明に書き直す。

## 背景

PR #34 で `docs/harness-guide.md` を新規作成した際、旧 README.md（Kiro ハーネス開発用の作業場リポジトリの説明）をそのままコピーしてしまった。
`harness-guide.md` はテンプレート複製後のユーザーが参照するドキュメントであり、Kiro 固有の内容ではなく、platform-harness 自体の概念・使い方を説明すべき。

関連 Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/35

## ユースケースの軸

> **テンプレート複製後のユーザーが、このハーネスが何であるか・どう使うかを理解できる。**

## 実装対象の機能

### 1. harness-guide.md の内容を書き直す

- Kiro 固有の記述を削除
- platform-harness の概念（ハーネスとは何か、2層構造、SDD）を説明
- 日常的な使い方・開発フローを記載
- 参照先（CLAUDE.md）へのリンクを含める

## 受け入れ条件

- [ ] Kiro・kiro-template 固有の記述が含まれていない
- [ ] ハーネスの概念（目的・構成要素・2層構造）が説明されている
- [ ] 日常的な使い方が記載されている
- [ ] テンプレート複製後のユーザーが読んで意味をなす内容になっている

## スコープ外

- README.md の変更
- CLAUDE.md の変更
- harness-engineering.md の変更
