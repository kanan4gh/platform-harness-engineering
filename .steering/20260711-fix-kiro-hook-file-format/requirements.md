# 要求内容

## 概要

kiro-templateのフックファイルをKiroが実際に読み込む形式(`.kiro.hook`拡張子+`enabled`フィールド)に修正する。

## 背景

- 関連Issue: https://github.com/kanan4gh/platform-harness-engineering/issues/45
- Kiro実機確認(Issue #42のフォローアップ)で、Agent Hooksパネルにフックが1つも表示されない事象が発生した
- 調査の結果、Kiroのフックファイルは`.kiro.hook`拡張子(例: `auto-format.kiro.hook`)で、スキーマに`enabled`フィールドを含む形式が標準であることを確認した(kiro.dev/docs/hooks/および実例リポジトリ)
- テンプレートは初期作成時から`.json`拡張子で配置しており、パネルに読み込まれていなかった(旧ONBOARDINGの「Hook UIから起動できない」FAQはこれが原因だった可能性が高い)

## ユースケースの軸

> **Kiroテンプレートの利用者が、Agent Hooksパネルでフックを確認・起動できるようになる。**

## 実装対象の機能

1. `.kiro/hooks/*.json` 3ファイルを `*.kiro.hook` にリネームする
2. 各フックに `"enabled": true` を追加し、versionを標準形式(`1.0.0`)に揃える(キー順も実例に合わせる)
3. ONBOARDING.mdのHook UI関連記述(チートシート注意書き・FAQ)を実態に合わせて更新する
4. `.json`拡張子への参照(functional-design.md・skill-doc-writing.md)を`.kiro.hook`に更新する

## 受け入れ条件

- [x] `.kiro/hooks/` 配下が `*.kiro.hook` のみになっている
- [x] 各フックJSONが `version` / `enabled` / `name` / `description` / `when` / `then` を含みパース可能である
- [x] ONBOARDING.md・functional-design.md・skill-doc-writing.mdに`.json`前提の記述が残っていない

## スコープ外

- フック内容(プロンプト・トリガー)の変更(PR #44で完了済み)
- Kiro実機での再確認(マージ後にユーザーが実施)

## 参照ドキュメント

- Issue #45 / PR #44 / `.steering/20260710-deploy-harness-core-v040-kiro/`
- https://kiro.dev/docs/hooks/
