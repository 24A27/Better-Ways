import os
import re
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import librosa
import numpy as np

# --- LLM Client Imports ---
import openai
import google.generativeai as genai

# --- FastAPI App Setup ---
app = FastAPI()

# CORS settings to allow access from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Initialize LLM Clients ---
openai_client = None
gemini_model = None

# OpenAI初期化
try:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key and openai_api_key != "sk-xxxxxxxxxxxxxxxxxxxxxxxxxx":
        openai_client = openai.OpenAI(api_key=openai_api_key)
        print("OpenAI client initialized successfully.")
    else:
        print("Warning: Valid OPENAI_API_KEY not found.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")

# Google Gemini初期化
try:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if google_api_key and google_api_key != "your_google_api_key_here":
        genai.configure(api_key=google_api_key)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        print("Google Gemini client initialized successfully.")
    else:
        print("Warning: Valid GOOGLE_API_KEY not found.")
except Exception as e:
    print(f"Error initializing Google Gemini client: {e}")

# Root endpoint to verify the server is running
@app.get("/")
async def root():
    return {"message": "Backend is running successfully!", "status": "OK"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Pydantic model for the request body
class Message(BaseModel):
    content: str

# Pydantic model for analysis results
class SpeechAnalysisResult(BaseModel):
    transcript: str
    content_feedback: str
    total_words: int
    duration_seconds: float
    average_wpm: float
    filler_count: int
    filler_words: list[str]
    used_provider: str

def validate_audio_file(file: UploadFile) -> bool:
    """音声ファイルの形式を検証"""
    # Content-Typeチェック
    allowed_content_types = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/m4a", "audio/x-m4a"]
    
    # ファイル拡張子チェック
    if file.filename:
        file_extension = file.filename.split('.')[-1].lower()
        allowed_extensions = ["mp3", "wav", "m4a"]
        
        # いずれかの条件を満たしていればOK
        return (file.content_type in allowed_content_types or 
                file_extension in allowed_extensions)
    
    return file.content_type in allowed_content_types

def analyze_speech_patterns(transcript: str, duration_seconds: float):
    """音声パターンを分析する関数"""
    # 単語数をカウント（日本語と英語に対応）
    words = re.findall(r'\b\w+\b', transcript)
    total_words = len(words)
    
    # WPM計算（分あたりの単語数）
    duration_minutes = duration_seconds / 60
    average_wpm = total_words / duration_minutes if duration_minutes > 0 else 0
    
    # フィラー語のリスト
    filler_patterns = [
        r'えー+と?',
        r'あー+',
        r'うー+ん?',
        r'その+',
        r'なんか',
        r'ちょっと',
        r'um+',
        r'uh+',
        r'like',
        r'you know',
    ]
    
    filler_words = []
    filler_count = 0
    
    for pattern in filler_patterns:
        matches = re.findall(pattern, transcript, re.IGNORECASE)
        filler_words.extend(matches)
        filler_count += len(matches)
    
    return {
        "total_words": total_words,
        "duration_seconds": duration_seconds,
        "average_wpm": round(average_wpm, 2),
        "filler_count": filler_count,
        "filler_words": filler_words
    }

async def transcribe_audio(file_path: str, provider: str):
    """音声を文字起こしする統一関数"""
    if provider == "openai":
        if not openai_client:
            raise HTTPException(status_code=500, detail="OpenAI APIが利用できません。APIキーを確認してください。")
        
        with open(file_path, "rb") as audio_file:
            transcript_response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ja"
            )
            return transcript_response.text
    
    elif provider == "google":
        # Google Speech-to-Text APIの実装予定地
        # 現在は暫定的にOpenAI Whisperを使用
        if not openai_client:
            raise HTTPException(
                status_code=500, 
                detail="Google Speech-to-Text APIは未実装です。OpenAI Whisper APIを使用するため、OpenAI APIキーが必要です。"
            )
        
        print("注意: Googleプロバイダーですが、音声認識にはOpenAI Whisperを使用します。")
        with open(file_path, "rb") as audio_file:
            transcript_response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ja"
            )
            return transcript_response.text
    
    else:
        raise HTTPException(status_code=400, detail="サポートされていないプロバイダーです。")

async def get_content_feedback(transcript: str, provider: str):
    """音声内容のフィードバックを取得"""
    prompt = f"""
以下の音声の文字起こし内容を分析し、話の構成、論理性、説得力について詳細なフィードバックを提供してください。

文字起こし:
{transcript}

以下の観点で分析してください：
1. 話の構成（導入、本論、結論）
2. 論理的な流れ
3. 具体例や根拠の使用
4. 聞き手への配慮
5. 改善点と具体的なアドバイス

フィードバックは建設的で実用的なものにしてください。
"""
    
    if provider == "openai":
        if not openai_client:
            return "OpenAI APIが利用できません。APIキーを確認してください。"
        
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたはプレゼンテーションとスピーチの専門家です。"},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"OpenAI フィードバック生成エラー: {str(e)}"
    
    elif provider == "google":
        if not gemini_model:
            return "Google Gemini APIが利用できません。APIキーを確認してください。"
        
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Google Gemini フィードバック生成エラー: {str(e)}"
    
    return "フィードバック生成機能が利用できません。"

# API endpoint for speech analysis
@app.post("/api/analyze-speech", response_model=SpeechAnalysisResult)
async def analyze_speech(file: UploadFile = File(...), provider: str = Form("openai")):
    """音声ファイルをアップロードして分析する（重複防止機能付き）"""
    
    # プロバイダーの検証
    if provider not in ["openai", "google"]:
        raise HTTPException(
            status_code=400, 
            detail="プロバイダーは 'openai' または 'google' を指定してください。"
        )
    
    print(f"使用プロバイダー: {provider}")
    
    # ファイル形式チェック
    if not validate_audio_file(file):
        raise HTTPException(
            status_code=400, 
            detail="サポートされていないファイル形式です。MP3, WAV, M4Aファイルをアップロードしてください。"
        )
    
    temp_file_path = None
    
    try:
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # 音声ファイルの長さを取得
        y, sr = librosa.load(temp_file_path)
        duration_seconds = librosa.get_duration(y=y, sr=sr)
        
        # 文字起こし処理
        transcript = await transcribe_audio(temp_file_path, provider)
        
        # 音声パターン分析
        speech_analysis = analyze_speech_patterns(transcript, duration_seconds)
        
        # 内容フィードバック取得
        content_feedback = await get_content_feedback(transcript, provider)
        
        return SpeechAnalysisResult(
            transcript=transcript,
            content_feedback=content_feedback,
            used_provider=provider,
            **speech_analysis
        )
        
    except HTTPException:
        # HTTPExceptionは再度raiseする
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"音声分析中にエラーが発生しました: {str(e)}"
        )
    
    finally:
        # 一時ファイルを確実に削除
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                print(f"一時ファイルを削除しました: {temp_file_path}")
            except Exception as e:
                print(f"一時ファイル削除エラー: {e}")

# API endpoint for chat
@app.post("/api/chat")
async def chat_with_llm(message: Message, provider: str = "openai"):
    """チャット機能（プロバイダー指定可能）"""
    
    if provider == "openai":
        if not openai_client:
            return {"error": "OpenAI client is not initialized. Check your API key."}
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message.content}
                ]
            )
            response_content = completion.choices[0].message.content
            return {"response": response_content, "used_provider": "openai"}
        except Exception as e:
            return {"error": f"OpenAI Error: {str(e)}"}

    elif provider == "google":
        if not gemini_model:
            return {"error": "Google Gemini client is not initialized. Check your API key."}
        try:
            response = gemini_model.generate_content(message.content)
            return {"response": response.text, "used_provider": "google"}
        except Exception as e:
            return {"error": f"Google Gemini Error: {str(e)}"}

    else:
        return {"error": f"Invalid provider: {provider}. Use 'openai' or 'google'"}
