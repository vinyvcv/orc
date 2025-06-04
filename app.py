import streamlit as st
from PIL import Image
import pytesseract
import io

st.set_page_config(page_title="OCR Online", layout="centered")
st.title("📄 Leitor de Imagem com OCR (Tesseract)")
st.write("Envie uma imagem para extrair o texto.")

# Upload da imagem
imagem = st.file_uploader("📤 Envie uma imagem (.jpg, .png, .jpeg)", type=["jpg", "png", "jpeg"])

if imagem:
    # Exibir imagem carregada
    img = Image.open(imagem)
    st.image(img, caption="Imagem enviada", use_column_width=True)

    st.info("⏳ Realizando OCR, aguarde...")

    # OCR com Tesseract
    texto = pytesseract.image_to_string(img, lang="por")  # 'por' = português

    if texto.strip():
        st.success("✅ Texto extraído com sucesso:")
        st.text_area("📝 Texto detectado:", texto.strip(), height=400)
    else:
        st.warning("⚠️ Nenhum texto foi encontrado na imagem.")
