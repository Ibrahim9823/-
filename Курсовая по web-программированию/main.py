from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

import requests

app = FastAPI()

# =========================
# STATIC
# =========================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =========================
# OPENROUTER
# =========================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================
# ГЛАВНАЯ СТРАНИЦА
# =========================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# =========================
# МОДЕЛЬ ЗАПРОСА
# =========================

class ChatRequest(BaseModel):
    message: str

# =========================
# ЧАТ-БОТ
# =========================

@app.post("/api/chat")
async def chat(data: ChatRequest):

    try:

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Student Clinic"
        }

        payload = {
            "model": "deepseek/deepseek-chat-v3-0324",
            "messages": [

                {
                    "role": "system",
                    "content": """
Ты виртуальный консультант студенческой поликлиники.

Твои обязанности:

- отвечать вежливо;
- помогать пользователям ориентироваться по сайту;
- рассказывать о врачах;
- рассказывать об услугах;
- объяснять порядок записи.

Нельзя:
- ставить диагнозы;
- назначать лечение;
- рекомендовать препараты.

Если человек описывает симптомы,
советуй обратиться к врачу.
"""
                },

                {
                    "role": "user",
                    "content": data.message
                }

            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()

        print("STATUS:", response.status_code)
        print("RESPONSE:", result)

        if "choices" not in result:

            return {
                "answer": f"Ошибка API: {result}"
            }

        answer = result["choices"][0]["message"]["content"]

        return {
            "answer": answer
        }

    except Exception as e:

        print("ERROR:", repr(e))

        return {
            "answer": f"Ошибка сервера: {str(e)}"
        }
    