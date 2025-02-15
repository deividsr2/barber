import streamlit as st
import pandas as pd
from banco import inserir_produto, buscar_produtos, atualizar_produto

# Título da página
st.title("Cadastro de Produtos")

# Opções predefinidas
tipos = ["produto"]

# **1️⃣ Cadastro de Novo Produto**
st.subheader("Cadastrar Novo Produto")

# Formulário para inserir novos produtos
with st.form(key="produto_form"):
    produto = st.text_input("Nome do Produto")
    categoria = st.text_input("Categoria")
    estoque = st.number_input("Estoque", min_value=0, step=1)
    estoque_seguranca = st.number_input("Estoque de Segurança", min_value=0, step=1)
    valor = st.number_input("Valor", min_value=0.0, step=0.01)
    submit_button = st.form_submit_button(label="Cadastrar Produto")

# Quando o formulário para cadastrar for enviado
if submit_button:
    if produto and categoria and estoque >= 0 and valor >= 0:
        # Inserir no banco de dados
        inserir_produto(produto, categoria, estoque, estoque_seguranca, valor)
        st.success(f"Produto '{produto}' cadastrado com sucesso!")
    else:
        st.error("Por favor, preencha todos os campos corretamente.")

# **2️⃣ Editar Produto**
st.subheader("Editar Produto")

# Buscar produtos cadastrados para exibição e seleção
produtos = buscar_produtos()

if produtos:
    produto_selecionado = st.selectbox("Selecione um produto para editar", 
                                       options=[p["produto"] for p in produtos])

    # Encontrar os dados do produto selecionado
    produto_dados = next(p for p in produtos if p["produto"] == produto_selecionado)

    # Formulário de edição
    with st.form(key="editar_produto_form"):
        novo_produto = st.text_input("Nome do Produto", value=produto_dados["produto"])
        nova_categoria = st.text_input("Categoria", value=produto_dados["categoria"])
        novo_estoque = st.number_input("Estoque", min_value=0, step=1, value=produto_dados["estoque"])
        novo_estoque_seguranca = st.number_input("Estoque de Segurança", min_value=0, step=1, value=produto_dados["estoque_seguranca"])
        novo_valor = st.number_input("Valor", min_value=0.0, step=0.01, value=float(produto_dados["valor"]))

        atualizar_button = st.form_submit_button("Atualizar Produto")

    # Se o botão de atualizar for pressionado
    if atualizar_button:
        atualizar_produto(produto_dados["id"], novo_produto, nova_categoria, novo_estoque, novo_estoque_seguranca, novo_valor)
        st.success(f"Produto '{novo_produto}' atualizado com sucesso!")
        st.rerun()
else:
    st.warning("Nenhum produto cadastrado ainda.")

# **3️⃣ Exibir Produtos**
# **3️⃣ Exibir Produtos**
st.subheader("Produtos Cadastrados")

# Permitir ao usuário definir a porcentagem de alerta
percentual_alerta = st.number_input("Porcentagem de Alerta", min_value=0, max_value=100, value=10, step=1)

# Exibir a tabela de produtos cadastrados
if produtos:
    # Convertendo os dados dos produtos para um DataFrame do Pandas para exibição
    df_produtos = pd.DataFrame(produtos)

    # Calcular a diferença entre o estoque e o estoque de segurança
    df_produtos['diferenca'] = df_produtos['estoque'] - df_produtos['estoque_seguranca']

    # Adicionar a nova coluna com o alerta
    def gerar_alerta(row):
        limite_alerta = row['estoque_seguranca'] * (percentual_alerta / 100)
        if row['diferenca'] <= limite_alerta:
            return "⚠️"  # Ícone de alerta vermelho
        return ""  # Sem alerta

    # Aplicar a função de alerta
    df_produtos['alerta'] = df_produtos.apply(gerar_alerta, axis=1)

    # Exibir a tabela com a nova coluna de alerta
    st.dataframe(df_produtos[['produto', 'categoria', 'estoque', 'estoque_seguranca', 'valor', 'alerta']])  # Exibe os produtos e alerta