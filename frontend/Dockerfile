FROM node:20-alpine

WORKDIR /app

# 依存関係のインストール
COPY package*.json ./
RUN npm install

# アプリケーションコードをコピー
COPY . .

# ポート3000を公開
EXPOSE 3000

# デフォルトコマンド
CMD ["npm", "run", "dev"]
