# 設計書

## 実装アプローチ

`inclusion: manual` の steering ファイルを 2 本作成する。Claude Code の対応スキルから内容を移植しつつ、Kiro の文脈に合わせた記述にする。

## 変更対象ファイル

| ファイル | 変更種別 | 内容 |
|---------|---------|------|
| `kiro-template/.kiro/steering/skill-sdd-guide.md` | 新規作成 | tasklist 進捗管理の詳細手順 |
| `kiro-template/.kiro/steering/skill-doc-writing.md` | 新規作成 | 永続ドキュメント記入ガイド |
| `kiro-template/.kiro/hooks/add-feature.json` | 変更 | プロンプトに `#skill-sdd-guide` 参照を追加 |

## 技術的判断と根拠

| 判断 | 根拠 |
|------|------|
| スキルを 2 ファイルに絞る | Claude Code のスキルは 7 本あるが、Kiro は汎用的なドキュメント作成能力を持つため、プロセス固有のガイド（SDD・ドキュメント品質）に絞れば十分 |
| ドキュメント記入ガイドを 1 ファイルにまとめる | Kiro の `#` 参照はファイル単位のため、6 ドキュメント分を 1 ファイルにセクションで整理する方が使いやすい |
| `add-feature.json` に `#skill-sdd-guide` 参照を追加 | hook 起動時にスキルを明示参照させることで、ユーザーが手動で `#` を入力する手間を省く |

## skill-sdd-guide.md の構成

```
# SDD ガイド（スペック駆動開発の詳細手順）

## tasklist.md 管理ルール
- タスク開始時に [ ] → [x] に更新する
- 全タスクが [x] になるまで継続する
- 「時間の都合により後回し」は禁止

## タスク完全完了の原則
- スキップが許可される条件（技術的理由のみ）
- スキップ時の記述形式

## フェーズ完了時の確認手順
- 未完了タスクの確認方法
- 振り返りの記入内容
```

## skill-doc-writing.md の構成

```
# ドキュメント記入ガイド

## product-requirements.md
## functional-design.md
## architecture.md
## repository-structure.md
## development-guidelines.md
## glossary.md
```

## 実装の順序

1. `skill-sdd-guide.md` を作成
2. `skill-doc-writing.md` を作成
3. `add-feature.json` のプロンプトを更新

<!-- この順序を tasklist.md のフェーズ1タスクに展開してください -->
