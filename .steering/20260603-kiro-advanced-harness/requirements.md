# 要求内容

## 概要

受け入れテストで判明した Kiro の仕組みを活用し、Claude Code ハーネスの残り要素（commands / skills / agents）を Kiro ハーネスに移植する。

## 関連 Issue

https://github.com/kanan4gh/platform-harness-for-kiro/issues/8

## ユースケースの軸

Kiro ユーザーが、Claude Code の `/add-feature` 相当のワークフロー自動化を Kiro 上で利用できる。

## 実装対象

### フェーズ1（本スペックの実装範囲）: userTriggered hook

| 成果物 | 内容 |
|---|---|
| `kiro-template/.kiro/hooks/add-feature.json` | SDD フルサイクル（スペック作成→実装→PR）を起動する userTriggered hook |
| `kiro-template/.kiro/hooks/setup-project.json` | docs/ 初期セットアップを起動する userTriggered hook |

### フェーズ2（次スペックで実装）: inclusion: manual steering（スキル相当）

| 成果物 | 内容 |
|---|---|
| `kiro-template/.kiro/steering/skill-sdd-guide.md` | tasklist 進捗管理の詳細手順 |
| `kiro-template/.kiro/steering/skill-doc-writing.md` | 各ドキュメントの記入ガイド |

### フェーズ3（次スペックで実装）: カスタムエージェント（サブエージェント相当）

| 成果物 | 内容 |
|---|---|
| `kiro-template/.kiro/agents/implementation-validator.md` | 実装品質チェック |
| `kiro-template/.kiro/agents/doc-reviewer.md` | ドキュメント品質レビュー |

## 受け入れ条件（フェーズ1）

- [ ] `add-feature.json` が `userTriggered` タイプで定義されている
- [ ] `add-feature.json` のプロンプトが「機能名を問い返す → スペック作成 → 実装 → PR」の流れを指示している
- [ ] `setup-project.json` が `userTriggered` タイプで定義されている
- [ ] `setup-project.json` のプロンプトが「docs/ を1ファイルずつ・承認を得ながら作成」の流れを指示している
- [ ] Kiro の Hook UI またはコマンドパレットから起動できる形式になっている（`version` フィールドあり）

## スコープ外（本スペック）

- フェーズ2・3の実装（別スペックで対応）
- hook のプロンプトで参照するスキルファイル本体（フェーズ2で実装）
- Kiro 実環境での動作確認（別途手動テスト）
