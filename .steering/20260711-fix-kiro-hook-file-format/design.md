# 設計書

## アーキテクチャ概要

ファイル形式の修正のみ。フックの内容(トリガー種別・プロンプト)はPR #44の設計を維持する。

## コンポーネント設計

### 1. フックファイルのリネームと形式修正

- `git mv` で `tasklist-check.json` / `add-feature.json` / `setup-project.json` → `*.kiro.hook`
- スキーマを実例準拠のキー順に整形: `version: "1.0.0"` → `enabled: true` → `name` → `description` → `when` → `then`
- `when`/`then` の中身は変更しない

### 2. ドキュメント整合

- ONBOARDING.md: チートシートの起動方法(パネル起動を追記)・注意書き(拡張子の説明に置換)・FAQ(「パネルに表示されない場合」のトラブルシュートに置換)
- functional-design.md マッピング表・skill-doc-writing.md: ファイル名参照を `.kiro.hook` に更新

## テスト戦略

- 全 `.kiro.hook` のJSONパース検証
- `uv run pytest` / `ruff check`(既存テストの非破壊確認)
- `.json` 前提記述の残存グラップ検索
- Kiro実機でのパネル表示確認はマージ後にユーザーが実施(本環境にKiro IDEなし)

## 実装の順序

1. リネーム → 2. スキーマ修正 → 3. ドキュメント更新 → 4. 検証 → 5. PR
