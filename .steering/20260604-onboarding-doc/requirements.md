# 要求仕様

## 関連 Issue

https://github.com/kanan4gh/platform-harness-for-kiro/issues/14

## 概要

社内 Kiro ユーザー向けのオンボーディングドキュメントを作成する。ハーネスの全機能を説明しつつ、SDD でワンサイクルの開発（機能追加から PR マージまで）を体験させることを目的とする。

## ターゲットユーザー

- Kiro の基本操作（チャット・ファイル編集）はわかる
- SDD の概念は知っている。本ハーネスは初めて
- 社内の開発者（エンジニア）
- **環境**: Windows + Python（devcontainer なし）

## 出力先

`kiro-template/ONBOARDING.md`

テンプレートを受け取ったユーザーがそのまま参照できるよう、テンプレート内に同梱する。

## ドキュメントの構成（案）

1. **このハーネスとは** — 何のためにあるか・何が変わるか（1ページで把握できる量）
2. **セットアップ** — テンプレート複製 → steering カスタマイズ → 動作確認
3. **機能リファレンス** — hooks / manual steering / agents の使い方
4. **チュートリアル: SDD でワンサイクル回す** — 架空の小機能を例に requirements → design → tasklist → 実装 → PR まで完走

## 受け入れ条件

- [ ] ドキュメントを読んだだけで、Kiro ユーザーが `add-feature` フックを使って SDD ワンサイクルを自走できる
- [ ] 各ハーネス機能（hooks・`#skill-sdd-guide`・`@implementation-validator`・`@doc-reviewer`）の呼び出し方が明記されている
- [ ] Kiro built-in spec を断る手順など、ハーネス固有の注意事項が記載されている
- [ ] **環境確認ステップが含まれている**（Windows + Python 環境で Kiro が正しくコマンドを提案できるかを確認する）
- [ ] SDD ワンサイクルの例は Windows + Python を前提としたストーリーで記述されている

## スコープ外

- docs/ 配下の永続ドキュメントの書き方（`#skill-doc-writing` に委ねる）
- Python・uv などのインストール手順（OS レベルの環境構築は読者が事前に済ませている前提）
- Claude CLI からの移行手順（既存の README に記載あり）
