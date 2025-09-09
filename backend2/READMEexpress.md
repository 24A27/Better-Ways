# Express LLM API サンプル 使い方

このファイルは Node.js (Express) で LLM API (OpenAI/Gemini) を叩くサンプルです。

## 必要なもの
- Node.js (v18以上推奨)
- npm
- APIキー（OpenAI, Google Gemini）

## セットアップ手順

1. backend2 ディレクトリに移動

```powershell
cd c:\Users\arsuser\Documents\24A27山上\Better-Ways\backend2
```

2. 必要なパッケージをインストール

```powershell
npm install express axios dotenv
```

3. .envファイルを用意し、APIキーを記載

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxx
```

4. サーバーを起動

```powershell
node express-llm-api.js
```

5. ブラウザやcurlでアクセス

例：
- Geminiでteacherロール
  - http://localhost:8000/ai/gemini/teacher/javaについておしえて
- OpenAIでengineerロール
  - http://localhost:8000/ai/openai/engineer/AIでできることを教えて

（日本語部分は自動でエンコードされますが、うまくいかない場合はURLエンコードしてください）

## エンドポイント仕様

- GET /ai/:llm/:role/:prompt
  - llm: openai または gemini
  - role: AIのロール（例: teacher, engineer など）
  - prompt: 質問内容

### レスポンス例
```json
{
  "llm": "gemini",
  "role": "teacher",
  "prompt": "javaについておしえて",
  "response": "...AIからの返答..."
}
```

## 注意事項
- APIキーは絶対に公開しないでください。
- このサンプルは学習・検証用です。

## ライセンス
MIT License
