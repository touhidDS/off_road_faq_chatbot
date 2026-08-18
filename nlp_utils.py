import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [
        lemmatizer.lemmatize(t)
        for t in tokens
        if t not in stop_words and t not in string.punctuation
    ]
    return " ".join(tokens)


class FAQMatcher:
    def __init__(self, faq_path, similarity_threshold=0.25):
        self.similarity_threshold = similarity_threshold

        with open(faq_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

        self.questions = [item["question"] for item in self.faqs]
        self.answers = [item["answer"] for item in self.faqs]

        cleaned_questions = [clean_text(q) for q in self.questions]

        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = self.vectorizer.fit_transform(cleaned_questions)

    def get_answer(self, user_question):
        cleaned = clean_text(user_question)

        if not cleaned:
            return {
                "answer": "Can you rephrase that? I didn't quite get it.",
                "matched_question": None,
                "confidence": 0.0,
            }

        user_vector = self.vectorizer.transform([cleaned])
        scores = cosine_similarity(user_vector, self.faq_vectors)[0]

        best_idx = scores.argmax()
        best_score = float(scores[best_idx])

        if best_score < self.similarity_threshold:
            return {
                "answer": "I don't have an answer for that. Try asking about tires, "
                "4WD/AWD, winching, ground clearance, or recovery.",
                "matched_question": None,
                "confidence": round(best_score, 3),
            }

        return {
            "answer": self.answers[best_idx],
            "matched_question": self.questions[best_idx],
            "confidence": round(best_score, 3),
        }
