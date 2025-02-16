import streamlit as st
from PIL import Image
from banco import buscar_barbeiros, buscar_servicos, inserir_atividade, buscar_atividades
from datetime import datetime
import pandas as pd
import plotly.express as px

# Configuração da página
st.markdown("---")
st.title("Cadastro de Atividades")

# Definindo o ID fixo para o barbeiro
barbeiro_id_fixo = 4  # Você pode mudar esse ID conforme necessário

# Buscar dados da tabela barber_teste_barbeiros com base no ID fixo
barbeiro = next(
    (b for b in buscar_barbeiros() if b["id"] == barbeiro_id_fixo), 
    None
)

# Verificar se o barbeiro foi encontrado
if barbeiro:
    barbeiro_selecionado = barbeiro["apelido"]  # Apelido do barbeiro
    senha_correta = barbeiro["sa"]  # Senha armazenada no banco
else:
    barbeiro_selecionado = "Barbeiro não encontrado"
    senha_correta = None

# Buscar dados dos serviços
servicos = buscar_servicos()

# Montar lista de serviços para o selectbox
lista_servicos = [(servico["id"], servico["servico"], servico["valor"]) for servico in servicos]

# Formulário para cadastro de atividades
st.subheader("Preencha os detalhes da atividade:")
with st.form("form_atividade"):
    st.write(f"Barbeiro Selecionado: {barbeiro_selecionado}")

    servico_selecionado = st.selectbox(
        "Serviço:",
        options=lista_servicos,
        format_func=lambda x: f"{x[1]} - R$ {x[2]:.2f}"
    )

    observacao = st.text_area("Observação (opcional):")

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    submitted = st.form_submit_button("Cadastrar Atividade")

    if submitted:
        try:
            inserir_atividade(
                id_barbeiro=barbeiro_id_fixo,
                barbeiro=barbeiro_selecionado,
                data_hora=data_hora,
                servico=servico_selecionado[1],
                valor=float(servico_selecionado[2]),
                observacao=observacao
            )
            st.success("Atividade cadastrada com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao cadastrar atividade: {e}")

# Exibir atividades do barbeiro selecionado
st.markdown("---")
st.title(f"Atividades de {barbeiro_selecionado} 💈")

atividades = buscar_atividades()
if atividades:
    df = pd.DataFrame(atividades)
    df = df[df["id_barbeiro"] == barbeiro_id_fixo]
    df["data_hora"] = pd.to_datetime(df["data_hora"], format="%Y-%m-%d %H:%M:%S")

    if not df["data_hora"].isna().all():
        data_min = df["data_hora"].min().date()
        data_max = df["data_hora"].max().date()
    else:
        data_min = datetime.today().date()
        data_max = datetime.today().date()

    st.subheader("📅 Filtro de Data")
    col1, col2 = st.columns(2)
    data_inicio = col1.date_input("Data inicial:", data_min)
    data_fim = col2.date_input("Data final:", data_max)
    df_filtrado = df[(df["data_hora"].dt.date >= data_inicio) & (df["data_hora"].dt.date <= data_fim)]

    st.markdown("---")
    st.title(f"💰 Acesso Financeiro - {barbeiro_selecionado.capitalize()}")

    senha_digitada = st.text_input("Digite sua senha para ver os valores:", type="password")

    if senha_digitada == senha_correta:
        st.success("✅ Acesso liberado!")
        col1, col2 = st.columns(2)
        total_valor = df_filtrado["valor"].sum()
        col1.metric(label="💰 Receita Total no Período", value=f"R$ {total_valor:.2f}")

        lucro_percentual = col2.slider("Selecione o percentual de lucro:", min_value=10, max_value=100, value=50, step=5)
        lucro_calculado = (total_valor * lucro_percentual) / 100
        col2.metric(label=f"📈 Lucro Estimado ({lucro_percentual}%)", value=f"R$ {lucro_calculado:.2f}")

        st.subheader("📊 Receita por Data")
        df_filtrado["Data"] = df_filtrado["data_hora"].dt.date
        fig = px.bar(df_filtrado, x="Data", y="valor", title="Receita por Data", labels={"Data": "Data", "valor": "Valor R$"}, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Atividades Registradas")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.error("❌ Senha incorreta! Tente novamente.")

st.markdown("---")
