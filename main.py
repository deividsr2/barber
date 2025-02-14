import streamlit as st
from PIL import Image
import base64
import os
import glob
import json

# Criar diretórios caso não existam
os.makedirs("logo", exist_ok=True)
os.makedirs("bc", exist_ok=True)
os.makedirs(".streamlit", exist_ok=True)  # Diretório para o config.toml

# Caminhos para os arquivos salvos
logo_dir = "logo/"
bg_dir = "bc/"
config_file = "config.txt"
theme_file = ".streamlit/config.toml"
opacity_file = "opacity.txt"
font_color_file = "font_color.txt"
barbeiros_file = "barbeiros.json"

# Função para salvar o nome da barbearia
def save_company_name(name):
    with open(config_file, "w") as f:
        f.write(name)

# Função para carregar o nome salvo
def load_company_name():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return f.read().strip()
    return "R10 Barber Shop"

# Função para salvar o tema escolhido
def save_theme(theme):
    with open(theme_file, "w") as f:
        f.write(f"[theme]\nbase=\"{theme}\"\n")

# Função para carregar o tema salvo
def load_theme():
    if os.path.exists(theme_file):
        with open(theme_file, "r") as f:
            for line in f:
                if line.startswith("base="):
                    return line.split("=")[1].strip().replace('"', '')
    return "light"  # Padrão: claro

# Função para salvar opacidade do background
def save_opacity(opacity):
    with open(opacity_file, "w") as f:
        f.write(str(opacity))

# Função para carregar opacidade salva
def load_opacity():
    if os.path.exists(opacity_file):
        with open(opacity_file, "r") as f:
            return float(f.read().strip())
    return 0.8  # Padrão: 80% de opacidade

# Função para salvar a cor da fonte
def save_font_color(color):
    with open(font_color_file, "w") as f:
        f.write(color)

# Função para carregar a cor da fonte salva
def load_font_color():
    if os.path.exists(font_color_file):
        with open(font_color_file, "r") as f:
            return f.read().strip()
    return "black"  # Padrão: Preto

# Recuperar configurações salvas
if "company_name" not in st.session_state:
    st.session_state.company_name = load_company_name()

if "theme" not in st.session_state:
    st.session_state.theme = load_theme()

if "bg_opacity" not in st.session_state:
    st.session_state.bg_opacity = load_opacity()

if "font_color" not in st.session_state:
    st.session_state.font_color = load_font_color()

# Função para remover arquivos antigos antes de salvar o novo
def replace_file(directory, new_file, prefix):
    for file in glob.glob(f"{directory}/{prefix}.*"):
        os.remove(file)
    
    ext = new_file.name.split(".")[-1]
    new_path = f"{directory}/{prefix}.{ext}"
    with open(new_path, "wb") as f:
        f.write(new_file.getbuffer())

    return new_path

# Buscar arquivos existentes
logo_path = next(iter(glob.glob(f"{logo_dir}/logo.*")), "logo/logo.png")
bg_path = next(iter(glob.glob(f"{bg_dir}/bc.*")), None)

# Configuração da página
st.set_page_config(page_title=st.session_state.company_name, page_icon=logo_path, layout="centered")

# Função para definir o background com opacidade ajustável
def set_background():
    if bg_path:
        with open(bg_path, "rb") as image:
            encoded_string = base64.b64encode(image.read()).decode()
        background_style = f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,{1 - st.session_state.bg_opacity}), rgba(0,0,0,{1 - st.session_state.bg_opacity})), 
                        url(data:image/jpg;base64,{encoded_string}) no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """
        st.markdown(background_style, unsafe_allow_html=True)

# Função para definir a cor da fonte
def set_font_color():
    font_style = f"""
    <style>
    h1, h2, h3, h4, h5, h6, p, label, span {{
        color: {st.session_state.font_color} !important;
    }}
    </style>
    """
    st.markdown(font_style, unsafe_allow_html=True)

# Aplicar estilos
set_background()
set_font_color()

# Exibir a logo no topo
if os.path.exists(logo_path):
    st.image(logo_path, width=150)

st.title(st.session_state.company_name)

st.subheader("Configurações da Barbearia")

# Botão para exibir ou ocultar as configurações
show_config = st.button("Exibir/Ocultar Configurações")

# Quando o botão for clicado, exibir as configurações
if show_config:
    with st.expander("Configurações", expanded=True):
        # Inputs para upload
        uploaded_logo = st.file_uploader("Envie uma nova logo:", type=["png", "jpg", "jpeg"])
        uploaded_bg = st.file_uploader("Envie uma nova imagem de fundo:", type=["png", "jpg", "jpeg"])

        # Input para alterar o nome da barbearia
        new_name = st.text_input("Nome da Barbearia:", st.session_state.company_name)

        # Opção para escolher o tema
        theme_options = {"Claro": "light", "Escuro": "dark"}
        theme_choice = st.selectbox("Escolha o tema:", list(theme_options.keys()), 
                                    index=list(theme_options.values()).index(st.session_state.theme))

        # Controle deslizante para ajustar opacidade do background
        new_opacity = st.slider("Opacidade do fundo", min_value=0.1, max_value=1.0, value=st.session_state.bg_opacity, step=0.05)

        # Opção para escolher a cor da fonte
        font_color_options = {
            "Preto": "black",
            "Branco": "white",
            "Vermelho": "red",
            "Azul": "blue",
            "Amarelo": "yellow"
        }
        font_choice = st.selectbox("Escolha a cor da fonte:", list(font_color_options.keys()),
                                   index=list(font_color_options.values()).index(st.session_state.font_color))

        # Botão para salvar as alterações
        if st.button("Salvar Alterações"):
            if uploaded_logo:
                logo_path = replace_file(logo_dir, uploaded_logo, "logo")
                st.success("Logo atualizada!")

            if uploaded_bg:
                bg_path = replace_file(bg_dir, uploaded_bg, "bc")
                st.success("Imagem de fundo atualizada!")

            if new_name and new_name != st.session_state.company_name:
                st.session_state.company_name = new_name
                save_company_name(new_name)
                st.success("Nome da empresa atualizado!")

            if theme_options[theme_choice] != st.session_state.theme:
                st.session_state.theme = theme_options[theme_choice]
                save_theme(st.session_state.theme)
                st.warning("Tema atualizado! Reinicie o app para aplicar.")

            if new_opacity != st.session_state.bg_opacity:
                st.session_state.bg_opacity = new_opacity
                save_opacity(new_opacity)
                st.success("Opacidade do fundo atualizada!")

            if font_color_options[font_choice] != st.session_state.font_color:
                st.session_state.font_color = font_color_options[font_choice]
                save_font_color(st.session_state.font_color)
                st.success("Cor da fonte atualizada!")

            st.rerun()  # Recarregar a página para aplicar mudanças


# Função para salvar os barbeiros
def save_barbeiros(barbeiros):
    with open(barbeiros_file, "w") as f:
        json.dump(barbeiros, f)

# Função para carregar os barbeiros salvos
def load_barbeiros():
    if os.path.exists(barbeiros_file):
        with open(barbeiros_file, "r") as f:
            return json.load(f)
    return {"quantidade": 2, "nomes": ["Barbeiro 1", "Barbeiro 2"]}

# Carregar configurações salvas
barbeiros_data = load_barbeiros()

# Agora que temos a lista de barbeiros, podemos defini-la
nomes_barbeiros = barbeiros_data["nomes"]

# Botão para exibir ou ocultar configurações de barbeiros
show_barbeiros_config = st.button("Exibir/Ocultar Configurações dos Barbeiros")

# Quando o botão for clicado, exibir as configurações dos barbeiros
if show_barbeiros_config:
    with st.expander("Configuração dos Barbeiros", expanded=True):
        # Selecionar número de barbeiros (mínimo 2, máximo 10)
        quantidade_barbeiros = st.slider("Número de Barbeiros", min_value=2, max_value=10, value=barbeiros_data["quantidade"])

        # Campos para nomear os barbeiros
        nomes_barbeiros = []
        for i in range(quantidade_barbeiros):
            nome = st.text_input(f"Nome do Barbeiro {i+1}:", value=barbeiros_data["nomes"][i] if i < len(barbeiros_data["nomes"]) else f"Barbeiro {i+1}")
            nomes_barbeiros.append(nome)

        # Botão para salvar configurações
        if st.button("Salvar Configurações dos Barbeiros"):
            barbeiros_data["quantidade"] = quantidade_barbeiros
            barbeiros_data["nomes"] = nomes_barbeiros
            save_barbeiros(barbeiros_data)
            st.success("Configurações dos barbeiros salvas! Recarregue o app para aplicar as mudanças.")

# --- CONFIGURAÇÃO DA NAVEGAÇÃO ---
# Página inicial
Home = st.Page("views/home.py", title="Home", icon=":material/account_circle:", default=True)

# Criar páginas de barbeiros dinamicamente
barbeiro_pages = [
    st.Page(f"views/barbeiro{i+1}.py", title=nomes_barbeiros[i], icon=":material/bar_chart:")
    for i in range(barbeiros_data["quantidade"])
]

# Outras páginas fixas
financeiro = st.Page("views/financeiro.py", title="Financeiro", icon=":material/attach_money:")
cadastro = st.Page("views/cadastro.py", title="Cadastro", icon=":material/settings:")

# Configurar navegação com os barbeiros selecionados
pg = st.navigation(
    {
        "Home": [Home],
        "Barbeiros": barbeiro_pages,
        "Financeiro": [financeiro],
        "Cadastro": [cadastro],
    }
)

# --- Exibir a Logo ---
st.logo("logo/logo.png")

# --- Rodar Navegação ---
pg.run()
