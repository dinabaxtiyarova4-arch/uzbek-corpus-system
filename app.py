import streamlit as st

st.set_page_config(
    page_title="O'zbek Korpusi",
    page_icon="📚",
    layout="wide"
)

st.title("📚 O'zbek Tili Matnlar Korpusi")

st.write("TXT fayl yuklang va statistikani ko'ring")

uploaded_file = st.file_uploader(
    "TXT fayl yuklang",
    type=["txt"]
)

if uploaded_file is not None:

    text = uploaded_file.read().decode("utf-8")

    st.success("Fayl yuklandi")

    st.text_area(
        "Matn",
        text,
        height=250
    )

    words = text.split()

    col1, col2 = st.columns(2)

    col1.metric(
        "So'zlar soni",
        len(words)
    )

    col2.metric(
        "Belgilar soni",
        len(text)
    )
