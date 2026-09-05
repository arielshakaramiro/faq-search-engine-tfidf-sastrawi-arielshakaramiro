"""
app.py — CLI sistem tanya-jawab FAQ berbasis TF-IDF + Sastrawi.

Jalankan setelah train.py: python app.py

Catatan perbaikan dari versi materi bootcamp aslinya (lihat README, bagian
"Audit & Perbaikan"):

1. Pertanyaan user sekarang di-preprocess (lowercase + hapus tanda baca +
   stemming Sastrawi) dengan fungsi yang SAMA seperti dipakai untuk
   melatih vectorizer. Versi asli langsung men-transform pertanyaan user
   mentah tanpa preprocessing, padahal seluruh korpus FAQ sudah
   di-preprocess saat training -- ini menyebabkan overlap kata yang lebih
   rendah dari seharusnya.
2. Metrik pencarian defaultnya diganti ke **cosine similarity**, bukan
   Euclidean distance dengan threshold tetap. Hasil audit menunjukkan
   Euclidean distance + threshold tetap (THR=1.0) bisa memunculkan
   false positive untuk pertanyaan yang sama sekali di luar topik.
   Euclidean tetap disediakan sebagai opsi (metric="euclidean") untuk
   perbandingan/edukasi.
"""

import json
import re

import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

EUCLIDEAN_THRESHOLD = 1.0
COSINE_THRESHOLD = 0.15  # di bawah ini dianggap "tidak ada yang cocok"


def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    return " ".join(stemmed_words)


def load_resources():
    vectorizer = joblib.load("vectorizer.joblib")
    with open("vector.json", "r", encoding="utf-8") as file:
        question_vectors = json.load(file)
    return vectorizer, question_vectors


def find_best_match(user_question, vectorizer, question_vectors, metric="cosine"):
    processed = preprocess_text(user_question)
    user_vector = vectorizer.transform([processed]).toarray()

    best_score = float("inf") if metric == "euclidean" else -1
    best_item = None

    for item in question_vectors:
        qv = np.array(item["vector"]).reshape(1, -1)
        if metric == "euclidean":
            score = euclidean_distances(user_vector, qv)[0][0]
            is_better = score < best_score and score <= EUCLIDEAN_THRESHOLD
        else:
            score = cosine_similarity(user_vector, qv)[0][0]
            is_better = score > best_score and score >= COSINE_THRESHOLD
        if is_better:
            best_score = score
            best_item = item

    return best_item, best_score


def main():
    vectorizer, question_vectors = load_resources()

    print("Selamat datang di sistem tanya jawab Emerald Mabel. Ketik 'exit' untuk keluar.")
    while True:
        user_question = input("Anda: ")
        if user_question.lower() == "exit":
            print("Terima kasih telah menggunakan layanan kami. Sampai jumpa!")
            break

        item, score = find_best_match(user_question, vectorizer, question_vectors, metric="cosine")
        if item:
            print(f"Pertanyaan terkait: {item['question']}")
            print(f"Emerald Mabel: {item['answer']}")
        else:
            print("Maaf, kami tidak menemukan jawaban yang sesuai dengan pertanyaan Anda.")


if __name__ == "__main__":
    main()
