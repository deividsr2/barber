import streamlit as st
import os
from pathlib import Path
from PIL import Image, UnidentifiedImageError

# Definir o caminho da pasta de imagens
PASTA_IMAGENS = Path("img_barbeiros")

# Criar a pasta caso não exista
PASTA_IMAGENS.mkdir(parents=True, exist_ok=True)

# Listar os arquivos de imagem na pasta e verificar se são válidos
imagens_existentes = []
for f in os.listdir(PASTA_IMAGENS):
    if f.endswith((".png", ".jpg", ".jpeg")):
        try:
            # Tentar abrir o arquivo para verificar se é uma imagem válida
            caminho_img = PASTA_IMAGENS / f
            Image.open(caminho_img)
            imagens_existentes.append(f)
        except UnidentifiedImageError:
            st.warning(f"O arquivo {f} não é uma imagem válida e será ignorado.")

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
    st.write("Nenhuma imagem válida encontrada na pasta.")

# Upload de nova imagem para substituir uma existente
st.subheader("Substituir uma imagem")

imagem_selecionada = st.selectbox("Escolha a imagem que deseja substituir", imagens_existentes)

imagem_upload = st.file_uploader("Faça upload da nova imagem", type=["png", "jpg", "jpeg"])

if imagem_upload and imagem_selecionada:
    try:
        # Tentar abrir a imagem carregada
        imagem_nova = Image.open(imagem_upload)

        # Redimensionar a nova imagem antes de salvar
        imagem_nova.thumbnail((300, 300))

        # Caminho para substituir a imagem
        caminho_substituir = PASTA_IMAGENS / imagem_selecionada

        # Salvar a nova imagem
        imagem_nova.save(caminho_substituir)

        st.success(f"A imagem '{imagem_selecionada}' foi substituída com sucesso!")
        st.rerun()

    except UnidentifiedImageError:
        st.error("O arquivo carregado não é uma imagem válida. Tente novamente com um arquivo de imagem.")
