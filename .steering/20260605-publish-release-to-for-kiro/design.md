# 設計書

## 変更方針

`.github/workflows/publish-template.yml` の "Commit and push" ステップの後に、
"Create release on output repo" ステップを追加する。

変更は1ファイル・1ステップの追加のみ。

---

## 追加ステップの設計

```yaml
- name: Create release on output repo
  if: github.event_name == 'release'
  env:
    PUBLISH_PAT: ${{ secrets.PUBLISH_PAT }}
  run: |
    cd /tmp/output-repo

    # コンテンツ差分なしでスキップされた場合はリリースも作成しない
    if git log --oneline -1 | grep -q "chore: publish ${{ github.ref_name }}"; then
      echo "Content was published. Creating release..."
    else
      echo "No content changes were published. Skipping release creation."
      exit 0
    fi

    GH_TOKEN="${PUBLISH_PAT}" gh release create "${{ github.ref_name }}" \
      --repo "kanan4gh/platform-harness-for-kiro" \
      --title "${{ github.ref_name }}: ${{ github.event.release.name }}" \
      --notes "platform-harness-engineering ${{ github.ref_name }} に対応したテンプレートです。

詳細なリリースノートは https://github.com/kanan4gh/platform-harness-engineering/releases/tag/${{ github.ref_name }} を参照してください。"
```

## 設計の要点

### 条件制御

- `if: github.event_name == 'release'` で release イベント時のみ実行
- workflow_dispatch 時はステップ自体がスキップされる

### 差分なしスキップの検出

"Commit and push" ステップは差分がない場合 `exit 0` で終了し、コミットを作成しない。
直前のコミットメッセージが `chore: publish <ref_name>` でなければ差分なしと判断してスキップする。

### 認証

`GH_TOKEN` に `PUBLISH_PAT` を使用。すでに push に使っているトークンなので追加権限は不要。

### リリースノート

本リポジトリ側に詳細なノートがあるため、Kiro 側は定型文＋本リポジトリへのリンクのみ。

## 実装の順序

1. `.github/workflows/publish-template.yml` に "Create release on output repo" ステップを追加
