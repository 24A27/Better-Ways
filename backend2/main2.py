import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import google.generativeai as genai

# 追加: .envを明示的に読み込む
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allow all origins for easy testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM clients
openai_client = None
gemini_model = None

try:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key:
        openai_client = openai.OpenAI(api_key=openai_api_key)
except Exception as e:
    print(f"OpenAI init error: {e}")

try:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if google_api_key:
        genai.configure(api_key=google_api_key)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Gemini init error: {e}")

@app.get("/")
def root():
    return {"message": "main2.py LLM API is running!"}

@app.get("/ai/{llm}/{role}/{prompt:path}")
def ai_endpoint(llm: str, role: str, prompt: str):
    """
    Example: /ai/gemini/teacher/javaについておしえて
    """
    if llm == "openai":
        if not openai_client:
            raise HTTPException(status_code=500, detail="OpenAI API not available.")
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a {role}."},
                    {"role": "user", "content": prompt}
                ]
            )
            return {"llm": "openai", "role": role, "prompt": prompt, "response": completion.choices[0].message.content}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    elif llm == "gemini":
        if not gemini_model:
            raise HTTPException(status_code=500, detail="Google Gemini API not available.")
        try:
            sys_prompt = f"You are a {role}." if role else ""
            response = gemini_model.generate_content([sys_prompt, prompt])
            return {"llm": "gemini", "role": role, "prompt": prompt, "response": response.text}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Supported llm: openai, gemini")
