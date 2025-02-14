import streamlit as st
import base64
import os

# Recuperar nome da barbearia das configurações
if "company_name" not in st.session_state:
    st.session_state.company_name = "R10 Barber Shop"  # Nome padrão caso não esteja carregado

# Título da página com o nome da barbearia
st.title(f"Bem-vindo à {st.session_state.company_name}")
st.write("Use o menu à esquerda para navegar entre as páginas dos barbeiros.")

# Lista de imagens e links correspondentes
imagens_links = {
    "img_barbeiros/barbeiro_1.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_1",
    "img_barbeiros/barbeiro_2.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_2",
    "img_barbeiros/barbeiro_3.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_3",
    "img_barbeiros/barbeiro_4.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_4",
    "img_barbeiros/barbeiro_5.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_5",
    "img_barbeiros/barbeiro_6.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_6",
    "img_barbeiros/barbeiro_7.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_7",
    "img_barbeiros/barbeiro_8.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_8",
    "img_barbeiros/barbeiro_9.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_9",
    "img_barbeiros/barbeiro_10.jpg": "https://deividsr2-barber-r10-git-main-v4o0iy.streamlit.app/barbeiro_10",
}

# Função para converter imagens em Base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Gerar imagens com links em Base64 para embutir no HTML
image_tags = "".join(
    [
        f'<a href="{link}" target="_blank"><img src="data:image/jpg;base64,{get_image_base64(img)}"></a>'
        for img, link in imagens_links.items()
    ]
)

# Código HTML do carrossel corrigido
carousel_html = f"""
<style>
    .carousel-container {{
        position: relative;
        width: 100%;
        max-width: 700px;
        margin: auto;
        overflow: hidden;
        border-radius: 10px;
    }}
    .carousel {{
        display: flex;
        transition: transform 0.5s ease-in-out;
        width: {len(imagens_links) * 33.33}%;
    }}
    .carousel a {{
        flex: 1 0 33.33%;
        text-align: center;
    }}
    .carousel img {{
        width: 80%;  /* Reduz o tamanho das imagens */
        border-radius: 10px;
    }}
    .carousel-buttons {{
        position: absolute;
        top: 50%;
        width: 100%;
        display: flex;
        justify-content: space-between;
        transform: translateY(-50%);
    }}
    .carousel-buttons button {{
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
        border: none;
        padding: 15px;
        cursor: pointer;
        border-radius: 50%;
        font-size: 24px;
        transition: 0.3s;
    }}
    .carousel-buttons button:hover {{
        background-color: rgba(0, 0, 0, 1);
    }}
</style>

<div class="carousel-container">
    <div class="carousel">
        {image_tags}
    </div>
    <div class="carousel-buttons">
        <button onclick="prevSlide()">&#10094;</button>  <!-- Seta esquerda -->
        <button onclick="nextSlide()">&#10095;</button>  <!-- Seta direita -->
    </div>
</div>

<script>
    let currentIndex = 0;
    const totalSlides = {len(imagens_links)} - 2; // Exibe todas as imagens
    const carousel = document.querySelector(".carousel");

    function updateCarousel() {{
        if (carousel) {{
            carousel.style.transform = "translateX(-" + (currentIndex * 33.33) + "%)";
        }}
    }}

    function nextSlide() {{
        currentIndex = (currentIndex + 1) % {len(imagens_links)};
        updateCarousel();
    }}

    function prevSlide() {{
        currentIndex = (currentIndex - 1 + {len(imagens_links)}) % {len(imagens_links)};
        updateCarousel();
    }}

    document.addEventListener("DOMContentLoaded", function() {{
        updateCarousel();
        setInterval(nextSlide, 3000); // Auto-play a cada 3 segundos
    }});
</script>
"""

# Exibir carrossel no Streamlit
st.components.v1.html(carousel_html, height=400)
