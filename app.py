import streamlit as st
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

st.title("📄 OCR com IA (100% online)")

imagem = st.file_uploader("📤 Envie uma imagem com texto", type=["jpg", "jpeg", "png"])

@st.cache_resource
def carregar_modelo():
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-stage1")
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-stage1")
    return processor, model

if imagem:
    img = Image.open(imagem).convert("RGB")
    st.image(img, caption="Imagem enviada", use_container_width=True)

    st.info("⏳ Realizando OCR com modelo TrOCR...")

    processor, model = carregar_modelo()
    pixel_values = processor(images=img, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    texto = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    if texto.strip():
        st.success("✅ Texto detectado:")
        st.text_area("📝", texto.strip(), height=300)
    else:
        st.warning("⚠️ Nenhum texto encontrado.")
