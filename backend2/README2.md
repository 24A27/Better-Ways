# main2.py LLM API 使い方

このAPIは、URLで「LLMの種類」「ロール」「プロンプト内容」を指定して、AIの返答を取得できるシンプルなエンドポイントを提供します。

## サーバーの起動方法

1. 必要なパッケージをインストール

```powershell
pip install -r requirements.txt
```

2. .envファイルにAPIキーを設定

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxx
```

3. サーバーを起動

```powershell
uvicorn main2:app --reload
```

## エンドポイント仕様

### GET /ai/{llm}/{role}/{prompt}

- **llm**: 使用するAI（"openai" または "gemini"）
- **role**: AIのロール（例: "teacher", "engineer" など）
- **prompt**: 質問や指示内容（日本語・英語どちらも可）

#### 例

- OpenAIでteacherロール:
  - `http://localhost:8000/ai/openai/teacher/日本の歴史を教えて`
- Geminiでengineerロール:
  - `http://localhost:8000/ai/gemini/engineer/AIでできることを教えて`

#### レスポンス例
```json
{
  "llm": "gemini",
  "role": "teacher",
  "prompt": "javaについておしえて",
  "response": "...AIからの返答..."
}
```

## 注意事項
- URLの最後の部分（prompt）は日本語もOKですが、URLエンコードが必要な場合があります。
- APIキーは絶対に公開しないでください。
- CORSは全許可になっています。必要に応じて制限してください。

## ライセンス
MIT License

1. サーバーを再起動する
同じディレクトリ（backend2）で、再度下記コマンドを実行します。
uvicorn main2:app --reload

2. ブラウザで再度アクセス
http://localhost:8000/ai/gemini/teacher/javaについておしえて