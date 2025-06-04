import streamlit as st
import subprocess
import os
import time
import json
import uuid

# Função para extrair o texto de um JSON do Docling
def extrair_texto(obj):
    textos = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "text" and isinstance(v, str):
                textos.append(v.strip())
            else:
                textos.extend(extrair_texto(v))
    elif isinstance(obj, list):
        for item in obj:
            textos.extend(extrair_texto(item))
    return textos

# Título do app
st.title("🧾 Leitor de Imagem com OCR (Docling)")

# Upload da imagem
uploaded_file = st.file_uploader("📷 Envie uma imagem (.jpg, .png, .pdf)", type=["jpg", "png", "jpeg", "pdf"])

if uploaded_file:
    # Nome temporário para salvar
    unique_id = uuid.uuid4().hex
    nome_entrada = f"temp_{unique_id}_{uploaded_file.name}"
    nome_json = os.path.splitext(nome_entrada)[0] + ".json"

    # Salvar a imagem enviada
    with open(nome_entrada, "wb") as f:
        f.write(uploaded_file.read())

    st.info("⏳ Lendo a imagem... Isso pode levar alguns segundos...")

    # Rodar o Docling
    subprocess.run(["docling", nome_entrada, "--ocr", "--to", "json"])

    # Esperar o JSON ser criado
    for _ in range(20):
        if os.path.exists(nome_json):
            break
        time.sleep(0.5)
    else:
        st.error("❌ Erro: JSON não foi gerado. Verifique o conteúdo da imagem.")
        st.stop()

    # Ler e extrair texto
    try:
        with open(nome_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            textos = extrair_texto(data)
    except Exception as e:
        st.error(f"❌ Erro ao processar o JSON: {e}")
        st.stop()

    if textos:
        st.success("✅ Texto extraído da imagem:")
        st.text_area("📝 Texto reconhecido:", "\n\n".join(textos), height=400)
    else:
        st.warning("⚠️ Nenhum texto encontrado na imagem.")

    # Limpar arquivos temporários
    os.remove(nome_entrada)
    os.remove(nome_json)
