# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.13-slim

# Gitをインストール
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# 作業ディレクトリを/appに設定
WORKDIR /app

# requirements.txtをコンテナにコピー
COPY requirements.txt .
# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトをコンテナにコピー
COPY ./requirement_list ./requirement_list
COPY ./settings.yaml .
COPY ./pyproject.toml .

# IS_DOCKER環境変数を設定
ENV IS_DOCKER=true
# 標準出力がバッファリングされないよう設定（C#側でリアルタイムに進捗を拾うため）
ENV PYTHONUNBUFFERED=1

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "-m", "requirement_list"]

# メタデータの追加
LABEL org.opencontainers.image.source="https://github.com/bteam-toku/requirement_list_develop.git"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="要件リスト一覧出力（Dockerコンテナ）"