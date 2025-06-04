import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="OCR com EasyOCR", layout="centered")
st.title("📄 OCR Online com EasyOCR")

@st.cache_resource
def carregar_leitor():
    return easyocr.Reader(['pt'], gpu=False)

uploaded_file = st.file_uploader("📷 Envie uma imagem (.jpg, .png, .jpeg)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # Reduz o tamanho da imagem para evitar estouro de memória
    max_size = (1024, 1024)
    image.thumbnail(max_size)

    st.image(image, caption="Imagem enviada", use_container_width=True)
    st.info("⏳ Realizando OCR, por favor aguarde...")

    try:
        reader = carregar_leitor()
        resultado = reader.readtext(np.array(image), detail=0, paragraph=True)
        texto = "\n".join(resultado)

        if texto.strip():
            st.success("✅ Texto detectado:")
            st.text_area("📝", texto.strip(), height=400)
        else:
            st.warning("⚠️ Nenhum texto encontrado.")
    except Exception as e:
        st.error(f"❌ Erro durante o OCR: {e}")
