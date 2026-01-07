# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.13-slim

# 作業ディレクトリを/appに設定
WORKDIR /app

# requirements.txtをコンテナにコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトをコンテナにコピー
COPY ./requirement_list ./requirement_list
COPY ./requirement_list_setup ./requirement_list_setup

# 作業ディレクトリの/workフォルダを作成
RUN mkdir /work

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "-m"]

# メタデータの追加
LABEL org.opencontainers.image.source="https://github.com/bteam-toku/requirement_list_develop.git"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="要件リスト一覧出力（Dockerコンテナ）"