import streamlit as st
import os
from pathlib import Path
from PIL import Image

# Definir o caminho da pasta de imagens
PASTA_IMAGENS = Path("img_barbeiros")

# Criar a pasta caso não exista
PASTA_IMAGENS.mkdir(parents=True, exist_ok=True)

# Listar os arquivos de imagem na pasta
imagens_existentes = [f for f in os.listdir(PASTA_IMAGENS) if f.endswith((".png", ".jpg", ".jpeg"))]

st.title("Gerenciar Imagens dos Barbeiros")

# Exibir imagens existentes com tamanho reduzido
if imagens_existentes:
    st.subheader("Imagens atuais")
    for img in imagens_existentes:
        caminho_img = PASTA_IMAGENS / img
        imagem = Image.open(caminho_img)

        # Redimensionar imagem para largura máxima de 300px
        imagem.thumbnail((300, 300))

        st.image(imagem, caption=img, use_container_width=True)
else:
    st.write("Nenhuma imagem encontrada na pasta.")

# Upload de nova imagem para substituir uma existente
st.subheader("Substituir uma imagem")

imagem_selecionada = st.selectbox("Escolha a imagem que deseja substituir", imagens_existentes)

imagem_upload = st.file_uploader("Faça upload da nova imagem", type=["png", "jpg", "jpeg"])

if imagem_upload and imagem_selecionada:
    caminho_substituir = PASTA_IMAGENS / imagem_selecionada

    # Abrir a imagem carregada pelo usuário
    imagem_nova = Image.open(imagem_upload)

    # Redimensionar a nova imagem antes de salvar
    imagem_nova.thumbnail((300, 300))
    imagem_nova.save(caminho_substituir)

    st.success(f"A imagem '{imagem_selecionada}' foi substituída com sucesso!")
    st.rerun()
