import streamlit as st
from PIL import Image
import base64
import os
import glob
import json
from banco import atualizar_apelido_barbeiro, listar_barbeiros



# Função para substituir arquivos
def replace_file(directory, uploaded_file, prefix):
    file_extension = os.path.splitext(uploaded_file.name)[1]

    # Remover arquivos antigos
    old_files = glob.glob(os.path.join(directory, f"{prefix}.*"))
    for old_file in old_files:
        os.remove(old_file)

    file_path = os.path.join(directory, f"{prefix}{file_extension}")

    # Salvar novo arquivo
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


# Criar diretórios caso não existam
os.makedirs("logo", exist_ok=True)
os.makedirs("bc", exist_ok=True)
os.makedirs(".streamlit", exist_ok=True)

# Caminhos para os arquivos salvos
logo_dir = "logo/"
bg_dir = "bc/"
config_file = "config.txt"
theme_file = ".streamlit/config.toml"
opacity_file = "opacity.txt"
font_color_file = "font_color.txt"

# Função para salvar e carregar o nome da barbearia, tema, opacidade e cor da fonte
def save_company_name(name):
    with open(config_file, "w") as f:
        f.write(name)

def load_company_name():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return f.read().strip()
    return "Nome da sua empresa"

def save_theme(theme):
    with open(theme_file, "w") as f:
        f.write(f"[theme]\nbase=\"{theme}\"\n")

def load_theme():
    if os.path.exists(theme_file):
        with open(theme_file, "r") as f:
            for line in f:
                if line.startswith("base="):
                    return line.split("=")[1].strip().replace('"', '')
    return "light"

def save_opacity(opacity):
    with open(opacity_file, "w") as f:
        f.write(str(opacity))

def load_opacity():
    if os.path.exists(opacity_file):
        with open(opacity_file, "r") as f:
            return float(f.read().strip())
    return 0.8

def save_font_color(color):
    with open(font_color_file, "w") as f:
        f.write(color)

def load_font_color():
    if os.path.exists(font_color_file):
        with open(font_color_file, "r") as f:
            return f.read().strip()
    return "black"

# Recuperar configurações salvas
if "company_name" not in st.session_state:
    st.session_state.company_name = load_company_name()

if "theme" not in st.session_state:
    st.session_state.theme = load_theme()

if "bg_opacity" not in st.session_state:
    st.session_state.bg_opacity = load_opacity()

if "font_color" not in st.session_state:
    st.session_state.font_color = load_font_color()

# Garantir que 'page' esteja inicializada
if "page" not in st.session_state:
    st.session_state.page = "home"  # Página inicial

# Garantir que 'show_config' esteja inicializada
if "show_config" not in st.session_state:
    st.session_state.show_config = False  # Inicialmente esconder configurações

# Função para aplicar a logo e configurações de fundo
def set_page_configurations():
    logo_path = next(iter(glob.glob(f"{logo_dir}/logo.*")), "logo/logo.png")
    bg_path = next(iter(glob.glob(f"{bg_dir}/bc.*")), None)

    # Configuração da página
    st.set_page_config(page_title=st.session_state.company_name, page_icon=logo_path, layout="centered")

    # Função para definir o background com opacidade ajustável
    set_background(bg_path)
    set_font_color()

    # Exibir a logo no topo, mas apenas nas páginas de configuração
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)

# Funções para definir o background e cor da fonte
def set_background(bg_path):
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

def set_font_color():
    font_style = f"""
    <style>
    h1, h2, h3, h4, h5, h6, p, label, span {{
        color: {st.session_state.font_color} !important;
    }}
    </style>
    """
    st.markdown(font_style, unsafe_allow_html=True)

# Chamar configurações na página inicial e nas páginas de configuração
set_page_configurations()

# --- Configurações da Barbearia (No topo da página inicial) ---
if st.session_state.page == "home":  # Garantir que isso só aconteça na página inicial
    st.title(st.session_state.company_name)
    #st.subheader("Configurações da Barbearia")

    # Botão para exibir/esconder configurações
    if st.button("ESTILO DO SITE"):
        st.session_state.show_config = not st.session_state.show_config

    if st.session_state.show_config:
        # Inputs para upload, escolha de tema, cor da fonte, etc.
        uploaded_logo = st.file_uploader("Envie uma nova logo:", type=["png", "jpg", "jpeg"])
        uploaded_bg = st.file_uploader("Envie uma nova imagem de fundo:", type=["png", "jpg", "jpeg"])
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

            st.rerun()

# --- Configuração dos Barbeiros ---
barbeiros_file = "barbeiros.json"

def save_barbeiros(barbeiros):
    with open(barbeiros_file, "w") as f:
        json.dump(barbeiros, f)

def load_barbeiros():
    if os.path.exists(barbeiros_file):
        with open(barbeiros_file, "r") as f:
            return json.load(f)
    return {"quantidade": 2, "nomes": ["Barbeiro 1", "Barbeiro 2"]}

barbeiros_data = load_barbeiros()

# Inicializar estado para exibição/ocultação das configurações dos barbeiros
# Inicializar estado para exibição/ocultação das configurações dos barbeiros
if "show_barber_config" not in st.session_state:
    st.session_state.show_barber_config = False

# Botão para exibir/esconder configurações dos barbeiros
if st.sidebar.button("Configurar Barbeiros"):
    st.session_state.show_barber_config = not st.session_state.show_barber_config

# Mostrar configurações apenas se o botão estiver ativado
if st.session_state.show_barber_config:
    st.sidebar.subheader("Configurações dos Barbeiros")

    nomes_barbeiros = []
    for barbeiro in barbeiros_data:
        novo_apelido = st.sidebar.text_input(
            f"Apelido para {barbeiro['barbeiro']}:",
            value=barbeiro["apelido"] if barbeiro["apelido"] else ""
        )
        nomes_barbeiros.append({"id": barbeiro["id"], "apelido": novo_apelido})

    if st.sidebar.button("Salvar Alterações"):
        for barbeiro in nomes_barbeiros:
            atualizar_apelido_barbeiro(barbeiro["id"], barbeiro["apelido"])
        st.success("Apelidos atualizados com sucesso!")
        st.rerun()  # Atualiza a interface

# --- Navegação das Páginas ---
Home = st.Page("views/home.py", title="Home", icon=":material/account_circle:", default=True)

barbeiro_pages = [
    st.Page(f"views/barbeiro{i+1}.py", title=barbeiros_data["nomes"][i], icon=":material/bar_chart:")
    for i in range(barbeiros_data["quantidade"])
]

financeiro = st.Page("views/financeiro.py", title="Financeiro", icon=":material/attach_money:")
cadastro = st.Page("views/cadastro.py", title="Cadastro Serviços", icon=":material/settings:")
cadastro_prod = st.Page("views/cad_produtos.py", title="Cadastro Produtos", icon=":material/settings:")
config = st.Page("views/config_iniciais.py", title="Ajustes", icon=":material/settings:")

# Navegação sem configurações (apenas conteúdo das páginas)
pg = st.navigation(
    {
        "Home": [Home],
        "Barbeiros": barbeiro_pages,
        "Financeiro": [financeiro],
        "Cadastro": [cadastro,cadastro_prod],
        "Ajustes": [config],
    }
)

pg.run()  # Rodar navegação para carregar as páginas sem configurações visíveis
