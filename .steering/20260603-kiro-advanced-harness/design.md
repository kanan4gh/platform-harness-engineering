# 設計書

## 実装アプローチ

`userTriggered` タイプの hook を 2 本作成する。各 hook のプロンプトに SDD フローの詳細手順を埋め込み、引数渡しの代わりに「機能名を教えてください」とエージェントが問い返す形で対応する。

## 変更対象ファイル

| ファイル | 変更種別 | 内容 |
|---------|---------|------|
| `kiro-template/.kiro/hooks/add-feature.json` | 新規作成 | SDD フルサイクル起動 hook |
| `kiro-template/.kiro/hooks/setup-project.json` | 新規作成 | docs/ 初期セットアップ起動 hook |

## 技術的判断と根拠

| 判断 | 根拠 |
|------|------|
| プロンプト内で機能名を問い返す | `userTriggered` hook は引数渡しの仕組みを持たない |
| `add-feature` のプロンプトに承認ゲートを明記 | `process.md` に追加した承認ゲート指示を hook でも強制する |
| `setup-project` は「1ファイルずつ・承認を得てから次へ」を強調 | テストで Kiro が一気に 6 ファイル作成した問題への対処 |
| `skill-sdd-guide` へ `#` 参照を促す文言をプロンプトに含める | フェーズ2で作成予定のスキルファイルへの橋渡し（今は参照先未作成でも問題ない） |

## add-feature.json のプロンプト設計

```
新機能の実装を SDD フローで開始します。

まず実装したい機能の名前を教えてください。

機能名が確認できたら、以下の順で進めます：
1. GitHub Issue を作成する（`gh issue create` または Web UI）
2. `.steering/_template/` をコピーして `.steering/YYYYMMDD-[機能名]/` を作成する
3. `requirements.md` を記入する → ユーザーの確認を得てから次へ
4. `design.md` を記入する → ユーザーの確認を得てから次へ
5. `tasklist.md` を記入する → ユーザーの確認を得てから実装へ
6. フィーチャーブランチを作成し、tasklist.md のタスクを順番に実装する
7. PR を作成してマージする

各ステップで必ずユーザーの確認を得てから次に進んでください。
```

## setup-project.json のプロンプト設計

```
新規プロジェクトのセットアップを開始します。

docs/ 配下に以下の 6 ドキュメントを順番に作成します。
各ファイルを作成するたびにユーザーの確認を得てから次へ進んでください。

1. product-requirements.md — まずプロダクトの概要・目的・ターゲットユーザーを聞いてから作成
2. functional-design.md
3. architecture.md
4. repository-structure.md
5. development-guidelines.md
6. glossary.md

作成後、.kiro/steering/ の product.md / tech.md / structure.md を実際のプロジェクト内容で更新してください。
```

## 実装の順序

1. `add-feature.json` を作成
2. `setup-project.json` を作成

<!-- この順序を tasklist.md のフェーズ1タスクに展開してください -->
