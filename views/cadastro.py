import streamlit as st
from banco import inserir_servico, buscar_servicos, atualizar_servico

st.title("Cadastro de Serviços")

# Opções predefinidas
tipos = ["serviço", "despesa", "produto", "vale"]

# ==============================
# 📌 CADASTRAR NOVO SERVIÇO
# ==============================
st.subheader("Cadastrar Novo Serviço")

with st.form(key="novo_servico_form"):
    novo_servico = st.text_input("Nome do Serviço")
    novo_tipo = st.selectbox("Tipo de Cadastro", tipos)
    novo_valor = st.number_input("Valor do Serviço", min_value=0.0, step=0.01)
    nova_categoria = st.text_input("Categoria", placeholder="Digite a categoria do serviço")

    cadastrar_button = st.form_submit_button(label="Cadastrar Serviço")

if cadastrar_button:
    if novo_servico and nova_categoria.strip():
        servico_com_tipo = f"{novo_servico} - {novo_tipo}"

        # Ajustar o valor se for 'despesa' ou 'vale'
        if novo_tipo in ["despesa", "vale"]:
            novo_valor = -novo_valor  

        inserir_servico(servico_com_tipo, novo_valor, nova_categoria)
        st.success(f"Serviço '{servico_com_tipo}' cadastrado com sucesso!")
        st.rerun()

# ==============================
# ✏️ EDITAR SERVIÇO EXISTENTE
# ==============================
st.subheader("Editar Serviço Existente")

# Buscar serviços já cadastrados
servicos = buscar_servicos()
servicos_dict = {s['servico']: s for s in servicos}  

# Dropdown para selecionar serviço a editar (pelo nome)
servico_selecionado = st.selectbox("Selecione um serviço para editar", options=["Nenhum"] + list(servicos_dict.keys()))

# Se um serviço for selecionado, exibe os campos para edição
if servico_selecionado != "Nenhum":
    servico_edicao = servicos_dict[servico_selecionado]
    id_selecionado = servico_edicao["id"]
    nome_servico = servico_edicao["servico"]
    valor_servico = float(servico_edicao["valor"])  # Converter Decimal para float
    categoria_servico = servico_edicao["categoria"]

    with st.form(key="editar_servico_form"):
        servico_editado = st.text_input("Nome do Serviço", value=nome_servico)
        valor_editado = st.number_input("Valor do Serviço", min_value=0.0, step=0.01, value=valor_servico)
        categoria_editada = st.text_input("Categoria", value=categoria_servico)

        editar_button = st.form_submit_button(label="Salvar Alterações")

    if editar_button:
        if servico_editado and categoria_editada.strip():
            atualizar_servico(id_selecionado, servico_editado, valor_editado, categoria_editada)
            st.success(f"Serviço '{servico_editado}' atualizado com sucesso!")
            st.rerun()

# ==============================
# 📋 LISTA DE SERVIÇOS
# ==============================
st.subheader("Serviços Cadastrados")
if servicos:
    for servico in servicos:
        st.write(f"**{servico['id']}** | {servico['servico']} - R${servico['valor']} | Categoria: {servico['categoria']}")
else:
    st.warning("Nenhum serviço cadastrado ainda.")


servico