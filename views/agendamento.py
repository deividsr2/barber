import streamlit as st
from datetime import date
import pandas as pd
from banco import buscar_barbeiros, buscar_servicos, inserir_agendamento
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

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
telefone_cliente = st.text_input("Telefone do Cliente (com DDD, ex: +5511999999999):")
email_cliente = st.text_input("E-mail do Cliente:")

# Função para enviar mensagem via WhatsApp
def enviar_whatsapp(numero_cliente, servico, data, horario, barbeiro):
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

        client = Client(account_sid, auth_token)

        mensagem = (
            f"✅ Confirmação de Agendamento ✅\n\n"
            f"📅 Data: {data.strftime('%d/%m/%Y')}\n"
            f"⏰ Horário: {horario}\n"
            f"💈 Serviço: {servico}\n"
            f"✂️ Barbeiro: {barbeiro}\n\n"
            f"Obrigado por agendar conosco! Qualquer dúvida, estamos à disposição. 😉"
        )

        message = client.messages.create(
            from_=twilio_whatsapp_number,
            body=mensagem,
            to=f"whatsapp:{numero_cliente}"
        )

        return True
    except Exception as e:
        st.error(f"❌ Erro ao enviar mensagem no WhatsApp: {e}")
        return False

# Botão de agendar
if st.button("Agendar Serviço"):
    if not horario:
        st.warning("⏳ Por favor, informe o horário do agendamento.")
    elif not telefone_cliente.startswith("+"):
        st.warning("📱 Informe o telefone do cliente no formato internacional, ex: +5511999999999")
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

            # Enviar mensagem de confirmação via WhatsApp
            if enviar_whatsapp(telefone_cliente, servico_selecionado["servico"], data_agendamento, horario, barbeiro_selecionado["apelido"]):
                st.success("✅ Agendamento realizado com sucesso! Mensagem de confirmação enviada via WhatsApp.")
            else:
                st.warning("⚠️ Agendamento realizado, mas houve um erro ao enviar a mensagem no WhatsApp.")
            
        except Exception as e:
            st.error(f"❌ Erro ao realizar o agendamento: {e}")
            st.rerun()
