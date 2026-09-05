"""
train.py — Melatih TF-IDF vectorizer untuk sistem tanya-jawab FAQ.

Menghasilkan:
- vectorizer.joblib  : TF-IDF vectorizer terlatih
- vector.json        : vektor TF-IDF untuk setiap pertanyaan di data.json

Jalankan: python train.py
"""

import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()


def preprocess_text(text: str) -> str:
    """Lowercase, hapus tanda baca, lalu stem tiap kata (Bahasa Indonesia, via Sastrawi)."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    return " ".join(stemmed_words)


def main():
    with open("data.json", "r", encoding="utf-8") as file:
        corpus = json.load(file)["qa_corpus"]

    questions = [item["question"] for item in corpus]
    answers = [item["answer"] for item in corpus]

    preprocessed_questions = [preprocess_text(q) for q in questions]
    preprocessed_answers = [preprocess_text(a) for a in answers]

    combined_corpus = preprocessed_questions + preprocessed_answers

    vectorizer = TfidfVectorizer()
    vectorizer.fit(combined_corpus)
    joblib.dump(vectorizer, "vectorizer.joblib")

    question_vectors = vectorizer.transform(preprocessed_questions)

    vector_data = []
    for question, answer, vector in zip(questions, answers, question_vectors):
        vector_data.append(
            {
                "question": question,
                "answer": answer,
                "vector": vector.toarray().tolist()[0],
            }
        )

    with open("vector.json", "w", encoding="utf-8") as file:
        json.dump(vector_data, file, indent=4, ensure_ascii=False)

    print(f"Ukuran vocabulary: {len(vectorizer.get_feature_names_out())} kata")
    print(f"Jumlah pertanyaan divektorisasi: {len(vector_data)}")
    print("Training selesai. Tersimpan: vectorizer.joblib, vector.json")


if __name__ == "__main__":
    main()
