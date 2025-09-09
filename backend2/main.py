import os
import re
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import librosa
import numpy as np

# LLM Client Imports
import openai
import google.generativeai as genai

app = FastAPI()

# Allow all origins for easier reuse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_client = None
gemini_model = None

# Initialize OpenAI
try:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key:
        openai_client = openai.OpenAI(api_key=openai_api_key)
except Exception as e:
    print(f"OpenAI init error: {e}")

# Initialize Google Gemini
try:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if google_api_key:
        genai.configure(api_key=google_api_key)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Gemini init error: {e}")

@app.get("/")
async def root():
    return {"message": "Backend is running!", "status": "OK"}

class Message(BaseModel):
    content: str

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
    allowed_content_types = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/m4a", "audio/x-m4a"]
    if file.filename:
        file_extension = file.filename.split('.')[-1].lower()
        allowed_extensions = ["mp3", "wav", "m4a"]
        return (file.content_type in allowed_content_types or file_extension in allowed_extensions)
    return file.content_type in allowed_content_types

def analyze_speech_patterns(transcript: str, duration_seconds: float):
    words = re.findall(r'\b\w+\b', transcript)
    total_words = len(words)
    duration_minutes = duration_seconds / 60
    average_wpm = total_words / duration_minutes if duration_minutes > 0 else 0
    filler_patterns = [
        r'えー+と?', r'あー+', r'うー+ん?', r'その+', r'なんか', r'ちょっと',
        r'um+', r'uh+', r'like', r'you know',
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
    if provider == "openai":
        if not openai_client:
            raise HTTPException(status_code=500, detail="OpenAI API not available.")
        with open(file_path, "rb") as audio_file:
            transcript_response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ja"
            )
            return transcript_response.text
    elif provider == "google":
        # Not implemented, fallback to OpenAI Whisper
        if not openai_client:
            raise HTTPException(status_code=500, detail="Google Speech-to-Text not implemented. OpenAI API required.")
        with open(file_path, "rb") as audio_file:
            transcript_response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ja"
            )
            return transcript_response.text
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider.")

async def get_content_feedback(transcript: str, provider: str):
    prompt = f"""
Analyze the following speech transcript and provide detailed feedback on structure, logic, and persuasiveness. Give constructive and practical advice.

Transcript:
{transcript}
"""
    if provider == "openai":
        if not openai_client:
            return "OpenAI API not available."
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a presentation and speech expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"OpenAI feedback error: {str(e)}"
    elif provider == "google":
        if not gemini_model:
            return "Google Gemini API not available."
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Google Gemini feedback error: {str(e)}"
    return "Feedback not available."

@app.post("/api/analyze-speech", response_model=SpeechAnalysisResult)
async def analyze_speech(file: UploadFile = File(...), provider: str = Form("openai")):
    if provider not in ["openai", "google"]:
        raise HTTPException(status_code=400, detail="Provider must be 'openai' or 'google'.")
    if not validate_audio_file(file):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use MP3, WAV, or M4A.")
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        y, sr = librosa.load(temp_file_path)
        duration_seconds = librosa.get_duration(y=y, sr=sr)
        transcript = await transcribe_audio(temp_file_path, provider)
        speech_analysis = analyze_speech_patterns(transcript, duration_seconds)
        content_feedback = await get_content_feedback(transcript, provider)
        return SpeechAnalysisResult(
            transcript=transcript,
            content_feedback=content_feedback,
            used_provider=provider,
            **speech_analysis
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech analysis error: {str(e)}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass

@app.post("/api/chat")
async def chat_with_llm(message: Message, provider: str = "openai"):
    if provider == "openai":
        if not openai_client:
            return {"error": "OpenAI client not initialized."}
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
            return {"error": "Google Gemini client not initialized."}
        try:
            response = gemini_model.generate_content(message.content)
            return {"response": response.text, "used_provider": "google"}
        except Exception as e:
            return {"error": f"Google Gemini Error: {str(e)}"}
    else:
        return {"error": f"Invalid provider: {provider}. Use 'openai' or 'google'"}
