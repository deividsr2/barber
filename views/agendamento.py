import streamlit as st
from datetime import date
import pandas as pd
import win32com.client as win32
from banco import buscar_barbeiros, buscar_servicos, inserir_agendamento

# Configuração da página
st.title("📅 Agendamento de Serviços")

# Data mínima permitida (hoje)
data_minima = date.today()

# Buscar serviços e barbeiros do banco
servicos = buscar_servicos()
barbeiros = buscar_barbeiros()

# Criar dicionários para buscar informações dos barbeiros
barbeiros_dict = {b["id"]: b for b in barbeiros}

# Seleção de serviço
servico_selecionado = st.selectbox(
    "Selecione o serviço:",
    options=servicos,
    format_func=lambda x: x["servico"]
)

# Seleção de barbeiro
barbeiro_selecionado = st.selectbox(
    "Selecione o barbeiro:",
    options=barbeiros,
    format_func=lambda x: x["apelido"]
)

# Obter detalhes do barbeiro selecionado
id_barbeiro = barbeiro_selecionado["id"]
telefone_remetente = barbeiros_dict[id_barbeiro]["telefone"]
email_remetente = barbeiros_dict[id_barbeiro]["email"]

# Seleção de data (somente datas futuras)
data_agendamento = st.date_input("Escolha a data:", min_value=data_minima)

# Entrada de horário
horario = st.text_input("Horário (ex: 14:30):")

# Dados do cliente
telefone_cliente = st.text_input("Telefone do Cliente:")
email_cliente = st.text_input("E-mail do Cliente:")

# Botão de agendar
if st.button("Agendar Serviço"):
    if not horario:
        st.warning("⏳ Por favor, informe o horário do agendamento.")
    else:
        try:
            # Inserir agendamento no banco
            inserir_agendamento(
                dt=data_agendamento,
                ano=data_agendamento.year,
                dia=data_agendamento.day,
                mes=data_agendamento.strftime("%B"),
                semana=data_agendamento.strftime("%U"),
                dia_da_semana=data_agendamento.strftime("%A"),
                ano_txt=str(data_agendamento.year),
                servico=servico_selecionado["servico"],
                telefone_cliente=telefone_cliente,
                email_cliente=email_cliente,
                id_barbeiro=id_barbeiro,
                barbeiro=barbeiro_selecionado["apelido"],
                horario=horario,
                telefone_remetente=telefone_remetente,
                email_remetente=email_remetente
            )

            # Enviar e-mail de confirmação
            outlook = win32.Dispatch("Outlook.Application")
            email = outlook.CreateItem(0)
            email.To = email_cliente
            email.Subject = "Confirmação de Agendamento - Barbearia"
            email.Body = f"""
            Olá,

            Seu agendamento foi confirmado com sucesso!

            ✅ Serviço: {servico_selecionado['servico']}
            ✂️ Barbeiro: {barbeiro_selecionado['apelido']}
            📅 Data: {data_agendamento.strftime("%d/%m/%Y")}
            ⏰ Horário: {horario}

            Se precisar reagendar ou cancelar, entre em contato.

            Atenciosamente,
            Barbearia
            """
            email.Send()

            st.success("✅ Agendamento realizado com sucesso! Um e-mail de confirmação foi enviado.")

        except Exception as e:
            st.error(f"❌ Erro ao realizar o agendamento: {e}")
            st.rerun()
