#!/bin/bash
set -e

# ネットワークが遅い環境でも確実にリトライするためのラッパー関数
retry() {
  local n=1
  local max=3
  local delay=15
  while true; do
    "$@" && break || {
      if [[ $n -lt $max ]]; then
        echo "失敗 (試行 $n/$max)。${delay}秒後にリトライします..."
        ((n++))
        sleep $delay
      else
        echo "コマンドが $max 回失敗しました: $*"
        return 1
      fi
    }
  done
}

# uv
retry curl -LsSf --retry 3 --retry-delay 10 --connect-timeout 60 --max-time 300 https://astral.sh/uv/install.sh -o /tmp/uv-install.sh
sh /tmp/uv-install.sh

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

export PATH="$HOME/.local/bin:$PATH"

# Python開発ツール
retry uv tool install ruff
retry uv tool install basedpyright

# AWS CLI v2（aws-cli feature を使わず手動インストールすることで AWS Toolkit の自動注入を回避）
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
  AWS_CLI_URL="https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"
else
  AWS_CLI_URL="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
fi
retry curl -fsSL --connect-timeout 60 --max-time 300 "$AWS_CLI_URL" -o /tmp/awscliv2.zip
unzip -q /tmp/awscliv2.zip -d /tmp
sudo /tmp/aws/install
rm -rf /tmp/aws /tmp/awscliv2.zip

# AWS CDK
# retry npm install -g aws-cdk --fetch-retry-mintimeout 20000 --fetch-retry-maxtimeout 120000

# AWS SAM CLI
# retry pip install aws-sam-cli --timeout 300 --retries 5

# バージョン確認
claude --version || true
aws --version || true
#cdk --version || true
#sam --version || true
