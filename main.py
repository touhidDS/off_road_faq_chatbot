from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from nlp_utils import FAQMatcher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(title="Off-Road FAQ Chatbot")

matcher = FAQMatcher(os.path.join(BASE_DIR, "faq_data.json"))


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(payload: Question):
    return matcher.get_answer(payload.question)


@app.get("/faqs")
def get_faqs():
    return matcher.faqs


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
