# Off-Road FAQ Chatbot

Small FAQ chatbot for off-road vehicle questions (4WD/AWD, tires, winching, recovery, etc).
Matches whatever the user types against a set of FAQ questions using TF-IDF + cosine similarity,
and returns the closest answer. If nothing matches well enough, it says so instead of guessing.

## How it works

- `faq_data.json` — question/answer pairs
- `nlp_utils.py` — text cleanup (NLTK: tokenize, remove stopwords, lemmatize) + TF-IDF matching (scikit-learn)
- `main.py` — FastAPI app, exposes `POST /ask` and `GET /faqs`
- `static/` — simple chat widget (HTML/CSS/JS) served at `/`

Similarity threshold is 0.25 — below that the bot just says it doesn't know.

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## Docker

```bash
docker build -t offroad-faq-bot .
docker run -p 7860:7860 offroad-faq-bot
```

## Possible improvements

TF-IDF only catches lexical overlap, so paraphrased questions can miss. Swapping in
sentence-transformers embeddings would help with that but adds a heavier dependency —
kept it simple for now.
