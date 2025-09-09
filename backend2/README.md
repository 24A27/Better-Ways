# Better-Ways Backend2 API

このディレクトリは、音声ファイルの文字起こし・分析・LLM連携APIの再利用用バックエンド（FastAPI）です。

## 機能
- 音声ファイルのアップロード＆自動文字起こし（OpenAI Whisper利用）
- 文字起こし内容の自動分析・フィードバック（OpenAI GPT-4o または Google Gemini）
- LLMチャットAPI

## セットアップ手順

### 1. Python環境の準備
Python 3.10 以上を推奨します。

### 2. 依存パッケージのインストール
```powershell
pip install -r requirements.txt
```

### 3. .envファイルの用意
ルート直下に `.env` ファイルを作成し、以下のようにAPIキーを設定してください。

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxx
```

- OpenAI APIキーは https://platform.openai.com/ で取得
- Google Gemini APIキーは https://aistudio.google.com/ で取得

### 4. サーバーの起動
```powershell
uvicorn main:app --reload
```

- デフォルトで http://127.0.0.1:8000 でAPIが起動します

## APIエンドポイント

### 1. 音声分析
- `POST /api/analyze-speech`
- フォームデータ: `file` (音声ファイル), `provider` ("openai" または "google")
- レスポンス: 文字起こし・分析・フィードバック

### 2. チャット
- `POST /api/chat`
- JSON: `{ "content": "質問内容" }`, `provider` ("openai" または "google")
- レスポンス: LLMからの返答

## 注意事項
- APIキーは絶対に公開しないでください。
- CORSは全許可になっています。必要に応じて制限してください。

## ライセンス
MIT License
