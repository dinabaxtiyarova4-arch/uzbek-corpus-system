import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import json
from collections import Counter

st.set_page_config(
    page_title="O'zbek Tili Korpusi",
    page_icon="📚",
    layout="wide"
)

# ==========================
# FUNKSIYALAR
# ==========================

STOP_WORDS = {
    "va","ham","bilan","uchun","bu","shu",
    "bir","ikki","uch","to'rt","besh",
    "lekin","ammo","esa","yoki","kabi"
}

SUFFIXES = [
    "ning","dan","ga","da","ni",
    "imiz","ingiz","lari",
    "im","ing","si",
    "lar",
    "moqda","yapti",
    "gan","kan",
    "adi","ydi",
    "ib","ab"
]


def preprocess_text(text):

    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)

    text = text.replace("ʻ", "'")
    text = text.replace("ʼ", "'")
    text = text.replace("‘", "'")
    text = text.replace("’", "'")

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def tokenize(text):

    return re.findall(
        r"[a-zA-Z'’-]+",
        text.lower()
    )


def lemmatize_word(word):

    lemma = word

    changed = True

    while changed:

        changed = False

        for suffix in sorted(
            SUFFIXES,
            key=len,
            reverse=True
        ):

            if lemma.endswith(suffix):

                if len(lemma) > len(suffix) + 2:

                    lemma = lemma[:-len(suffix)]

                    changed = True

                    break

    return lemma


def lemmatize_tokens(tokens):

    lemmas = []

    for token in tokens:

        if token in STOP_WORDS:
            continue

        lemma = lemmatize_word(token)

        if len(lemma) > 1:
            lemmas.append(lemma)

    return lemmas


# ==========================
# UI
# ==========================

st.title("📚 O'zbek Tili Matnlar Korpusi")

st.markdown(
"""
Ushbu tizim:

✅ Preprocessing

✅ Tokenizatsiya

✅ Lemmatizatsiya

✅ Top-20 lemma

✅ Grafik

✅ JSON eksport
"""
)

uploaded_file = st.file_uploader(
    "TXT fayl yuklang",
    type=["txt"]
)

if uploaded_file is not None:

    text = uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    )

    cleaned = preprocess_text(text)

    tokens = tokenize(cleaned)

    lemmas = lemmatize_tokens(tokens)

    lemma_freq = Counter(lemmas)

    top20 = lemma_freq.most_common(20)

    # ==================
    # STATISTIKA
    # ==================

    st.success("Fayl muvaffaqiyatli yuklandi")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Tokenlar",
        len(tokens)
    )

    col2.metric(
        "Lemmalar",
        len(lemmas)
    )

    col3.metric(
        "Noyob lemmalar",
        len(set(lemmas))
    )

    # ==================
    # TOP 20
    # ==================

    st.subheader("📊 Top-20 lemma")

    df = pd.DataFrame(
        top20,
        columns=[
            "Lemma",
            "Chastota"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # ==================
    # GRAFIK
    # ==================

    st.subheader("📈 Chastota grafigi")

    fig, ax = plt.subplots(
        figsize=(10,5)
    )

    ax.bar(
        df["Lemma"],
        df["Chastota"]
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

    # ==================
    # JSON
    # ==================

    result = {

        "token_count": len(tokens),

        "lemma_count": len(lemmas),

        "unique_lemmas": len(set(lemmas)),

        "top20": top20
    }

    json_data = json.dumps(
        result,
        ensure_ascii=False,
        indent=4
    )

    st.download_button(
        "⬇ JSON yuklab olish",
        json_data,
        file_name="corpus_result.json",
        mime="application/json"
    )
