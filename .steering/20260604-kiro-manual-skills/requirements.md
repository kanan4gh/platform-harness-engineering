# 要求内容

## 概要

Claude Code の `skills/` に相当する詳細ガイドを、Kiro の `inclusion: manual` steering ファイルとして実装する。必要な時だけ `#ファイル名` でロードする形で、常時注入（always）との使い分けを実現する。

## 関連 Issue

https://github.com/kanan4gh/platform-harness-for-kiro/issues/8

## ユースケースの軸

Kiro ユーザーが、tasklist.md の進捗管理ルールやドキュメント記入の詳細手順を必要な時だけ参照できる。

## 実装対象

| 成果物 | 内容 | 対応する Claude Code スキル |
|---|---|---|
| `kiro-template/.kiro/steering/skill-sdd-guide.md` | tasklist 進捗管理の詳細手順・タスク完全完了の原則 | `skills/steering/` |
| `kiro-template/.kiro/steering/skill-doc-writing.md` | 各永続ドキュメントの記入ガイド（PRD・設計書等） | `skills/prd-writing/` 等 |

## 受け入れ条件

- [ ] 両ファイルに `inclusion: manual` frontmatter が設定されている
- [ ] `skill-sdd-guide.md` に tasklist.md 管理ルール（タスク完全完了の原則・スキップ禁止・技術的スキップの条件）が記述されている
- [ ] `skill-doc-writing.md` に各ドキュメント（product-requirements・functional-design・architecture・repository-structure・development-guidelines・glossary）の記入ガイドが記述されている
- [ ] `add-feature.json` のプロンプトに `#skill-sdd-guide` を参照する文言を追加する

## スコープ外

- フェーズ3（カスタムエージェント）
- Kiro 実環境での動作確認（別途手動テスト）
