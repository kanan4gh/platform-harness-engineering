# 要求仕様

## 関連 Issue

https://github.com/kanan4gh/platform-harness-for-kiro/issues/11

## 概要

Claude Code の `.claude/agents/` に相当する Kiro カスタムエージェントを `kiro-template/.kiro/agents/` に実装する。

## 背景

Claude Code ↔ Kiro の対応表:

| Claude Code | Kiro | 呼び出し方 |
|---|---|---|
| `.claude/agents/*.md` | `.kiro/agents/*.md` | `@agent-name` |

Phase 1（hooks）・Phase 2（manual steering）に続くフェーズ3として、エージェント層を移植することでハーネスの三層構造が揃う。

## 移植対象

| エージェント名 | 役割 |
|---|---|
| `implementation-validator` | 実装コードの品質検証・スペック整合性確認 |
| `doc-reviewer` | ドキュメント品質レビュー・改善提案 |

## 受け入れ条件

- [ ] `kiro-template/.kiro/agents/implementation-validator.md` が作成されており、`@implementation-validator` で呼び出せる
- [ ] `kiro-template/.kiro/agents/doc-reviewer.md` が作成されており、`@doc-reviewer` で呼び出せる
- [ ] 各エージェントが Kiro のフォーマット（frontmatter: `name`, `description`）に準拠している
- [ ] Kiro での受け入れテストで `@implementation-validator` および `@doc-reviewer` が正常動作する
- [ ] Phase 2 の `#skill-sdd-guide` 動作確認も受け入れテストに含める

## スコープ外

- Claude Code の詳細なコード品質チェック（npm lint/typecheck 等の実行）は Kiro では省略し、概念的な検証プロセスに絞る
- model 指定は Kiro の frontmatter 仕様に依存するため、不明なら省略する
