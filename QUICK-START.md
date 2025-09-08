# ⚡ クイックスタートガイド

## 最短3ステップで起動！

### 1️⃣ APIキーを設定
```bash
cp .env.example .env
# .envファイルを開いて、APIキーを設定
```

### 2️⃣ Dockerで起動
# 初回起動・コード変更時
```bash
docker-compose up --build
```
# 日常的な起動 2回目以降
```bash
docker-compose up
```
# トラブル時・完全リセット
```bash
docker-compose up --build --force-recreate
```


### 3️⃣ ブラウザでアクセス
http://localhost:5173

---

## 🔑 APIキーの取得
- **OpenAI**: https://platform.openai.com/
- **Google**: https://aistudio.google.com/

## 📖 詳細な説明
詳しいセットアップ方法は `README-start.md` を参照してください。

## 🆘 困ったら
```bash
docker-compose down
docker-compose up --build --force-recreate
```
