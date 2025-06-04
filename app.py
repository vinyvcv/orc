import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="OCR com EasyOCR", layout="centered")
st.title("📄 OCR Online com EasyOCR")

uploaded_file = st.file_uploader("📷 Envie uma imagem (.jpg, .png, .jpeg)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Imagem enviada", use_container_width=True)

    st.info("⏳ Lendo o texto da imagem...")

    reader = easyocr.Reader(['pt'])  # OCR em português
    resultado = reader.readtext(np.array(image), detail=0, paragraph=True)
    texto = "\n".join(resultado)

    if texto.strip():
        st.success("✅ Texto extraído:")
        st.text_area("📝", texto.strip(), height=300)
    else:
        st.warning("⚠️ Nenhum texto detectado.")
