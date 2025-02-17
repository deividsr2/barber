import pymysql
from sqlalchemy import create_engine, text
import os
import streamlit as st

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "145.223.31.244")
DB_PORT = int(os.getenv("DB_PORT", 10))
DB_USER = os.getenv("DB_USER", "mysql")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Tricolor633#")
DB_NAME = os.getenv("DB_NAME", "banco")

# Conexão SQLAlchemy com pooling
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True, pool_size=10, max_overflow=20, pool_recycle=3600
)

# Função de conexão direta com PyMySQL
def create_connection():
    try:
        return pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Exception as e:
        st.error(f"Erro ao conectar ao banco: {e}")
        return None


# --------------------------------------------------
# Funções para a tabela barber_teste_servicos
# --------------------------------------------------

def inserir_servico(servico, valor, categoria):
    """
    Insere um novo serviço na tabela `barber_teste_servicos` com categoria.
    """
    query = text("INSERT INTO barber_teste_servicos (servico, valor, categoria) VALUES (:servico, :valor, :categoria)")
    with engine.connect() as connection:
        connection.execute(query, {"servico": servico, "valor": valor, "categoria": categoria})
        connection.commit()

def buscar_servicos():
    """
    Retorna todos os serviços cadastrados na tabela `barber_teste_servicos`.
    """
    query = text("SELECT * FROM barber_teste_servicos ORDER BY id DESC")
    with engine.connect() as connection:
        result = connection.execute(query)
        return [dict(row) for row in result]

def atualizar_servico(id, servico, valor, categoria):
    """
    Atualiza um serviço específico na tabela `barber_teste_servicos`, incluindo a categoria.
    """
    query = text("UPDATE barber_teste_servicos SET servico = :servico, valor = :valor, categoria = :categoria WHERE id = :id")
    with engine.connect() as connection:
        connection.execute(query, {"id": id, "servico": servico, "valor": valor, "categoria": categoria})
        connection.commit()



# --------------------------------------------------
# Funções para a tabela barber_teste_atividades
# --------------------------------------------------

def inserir_atividade(id_barbeiro, barbeiro, data_hora, servico, valor, observacao):
    """
    Insere uma nova atividade na tabela `barber_teste_atividades`.
    """
    query = text("""
    INSERT INTO barber_teste_atividades (id_barbeiro, barbeiro, data_hora, servico, valor, observacao) 
    VALUES (:id_barbeiro, :barbeiro, :data_hora, :servico, :valor, :observacao)
    """)
    with engine.connect() as connection:
        connection.execute(query, {
            "id_barbeiro": id_barbeiro,
            "barbeiro": barbeiro,
            "data_hora": data_hora,
            "servico": servico,
            "valor": valor,
            "observacao": observacao
        })
        connection.commit()

def buscar_atividades():
    """Busca todas as atividades registradas no banco."""
    conn = create_connection()
    if conn:
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # Usa DictCursor para retornar dicionários
                cursor.execute("SELECT * FROM barber_teste_atividades ORDER BY data_hora DESC")
                result = cursor.fetchall()
                return result  # Retorna a lista de dicionários diretamente
        except Exception as e:
            st.error(f"Erro ao buscar atividades: {e}")
            return []
        finally:
            conn.close()
    return []


def atualizar_atividade(id, dados):
    """
    Atualiza uma atividade específica na tabela `barber_teste_atividades`.
    """
    updates = ", ".join([f"{key} = :{key}" for key in dados.keys()])
    query = text(f"UPDATE barber_teste_atividades SET {updates} WHERE id = :id")
    dados["id"] = id
    with engine.connect() as connection:
        connection.execute(query, dados)
        connection.commit()


# --------------------------------------------------
# Funções para a tabela barber_teste_barbeiros
# --------------------------------------------------

def inserir_barbeiro(barbeiro):
    """
    Insere um novo barbeiro na tabela `barber_teste_barbeiros`.
    """
    query = text("INSERT INTO barber_teste_barbeiros (barbeiro) VALUES (:barbeiro)")
    with engine.connect() as connection:
        connection.execute(query, {"barbeiro": barbeiro})
        connection.commit()


def buscar_barbeiros():
    conn = create_connection()
    if conn:
        try:
            # Consulta para buscar barbeiros
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM barber_teste_barbeiros")
                result = cursor.fetchall()  # Isso retornará uma lista de dicionários
                return result  # Retorna a lista de barbeiros
        except Exception as e:
            st.error(f"Erro ao buscar barbeiros: {e}")
            return []
        finally:
            conn.close()
    return []

def buscar_servicos():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM barber_teste_servicos")
                result = cursor.fetchall()
                return result
        except Exception as e:
            st.error(f"Erro ao buscar serviços: {e}")
            return []
        finally:
            conn.close()
    return []


def atualizar_barbeiro(id, barbeiro):
    """
    Atualiza o nome de um barbeiro na tabela `barber_teste_barbeiros`.
    """
    query = text("UPDATE barber_teste_barbeiros SET barbeiro = :barbeiro WHERE id = :id")
    with engine.connect() as connection:
        connection.execute(query, {"id": id, "barbeiro": barbeiro})
        connection.commit()

def buscar_senha_barbeiro(nome_barbeiro):
    """
    Busca a senha do barbeiro no banco de dados.
    """
    query = text("SELECT sa FROM barber_teste_barbeiros WHERE barbeiro = :barbeiro")
    with engine.connect() as connection:
        result = connection.execute(query, {"barbeiro": nome_barbeiro}).fetchone()
        return result[0] if result else None  # Retorna a senha ou None


def atualizar_senha_barbeiro(nome_barbeiro, nova_senha):
    """
    Atualiza a senha do barbeiro no banco de dados.
    """
    query = text("UPDATE barber_teste_barbeiros SET sa = :nova_senha WHERE barbeiro = :barbeiro")
    with engine.connect() as connection:
        connection.execute(query, {"nova_senha": nova_senha, "barbeiro": nome_barbeiro})
        connection.commit()

def atualizar_apelido_barbeiro(id, apelido):
    """
    Atualiza o apelido de um barbeiro na tabela `barber_teste_barbeiros`.
    """
    query = text("UPDATE barber_teste_barbeiros SET apelido = :apelido WHERE id = :id")
    with engine.connect() as connection:
        connection.execute(query, {"id": id, "apelido": apelido})
        connection.commit()

def listar_barbeiros():
    """
    Retorna os IDs e nomes atuais dos barbeiros cadastrados no banco.
    """
    query = text("SELECT id, barbeiro, apelido FROM barber_teste_barbeiros")
    with engine.connect() as connection:
        result = connection.execute(query).fetchall()
        return [{"id": row[0], "barbeiro": row[1], "apelido": row[2]} for row in result]

# ==============================
# 📌 Funções para a tabela barber_teste_produtos
# ==============================

def inserir_produto(produto, categoria, estoque, estoque_seguranca, valor):
    """
    Insere um novo produto na tabela `barber_teste_produtos`.
    """
    # Garantir que estoque e estoque_seguranca sejam inteiros
    estoque = int(estoque)
    estoque_seguranca = int(estoque_seguranca)
    
    query = text("""
        INSERT INTO barber_teste_produtos (produto, categoria, estoque, estoque_seguranca, valor)
        VALUES (:produto, :categoria, :estoque, :estoque_seguranca, :valor)
    """)
    with engine.connect() as connection:
        connection.execute(query, {
            "produto": produto, 
            "categoria": categoria, 
            "estoque": estoque,
            "estoque_seguranca": estoque_seguranca,
            "valor": valor
        })
        connection.commit()



def buscar_produtos():
    """
    Retorna todos os produtos cadastrados na tabela `barber_teste_produtos`.
    """
    query = text("SELECT id, produto, categoria, estoque, estoque_seguranca, valor FROM barber_teste_produtos")
    with engine.connect() as connection:
        result = connection.execute(query)
        produtos = [dict(row) for row in result.mappings()]  # Garante que retorna um dicionário
        return produtos



def atualizar_produto(id, produto, categoria, estoque, estoque_seguranca, valor):
    """
    Atualiza um produto na tabela `barber_teste_produtos`.
    """
    # Garantir que estoque e estoque_seguranca sejam inteiros
    estoque = int(estoque)
    estoque_seguranca = int(estoque_seguranca)
    
    query = text("""
        UPDATE barber_teste_produtos 
        SET produto = :produto, categoria = :categoria, estoque = :estoque, 
            estoque_seguranca = :estoque_seguranca, valor = :valor 
        WHERE id = :id
    """)
    with engine.connect() as connection:
        connection.execute(query, {
            "id": id,
            "produto": produto,
            "categoria": categoria,
            "estoque": estoque,
            "estoque_seguranca": estoque_seguranca,
            "valor": valor
        })
        connection.commit()


def inserir_agendamento(dt, ano, dia, mes, semana, dia_da_semana, ano_txt, servico, telefone_cliente, email_cliente, id_barbeiro, barbeiro, horario, telefone_remetente, email_remetente):
    """
    Insere um novo agendamento na tabela `barber_teste_agendamento`.
    """
    query = text("""
        INSERT INTO barber_teste_agendamento (
            dt, ano, dia, mes, semana, dia_da_semana, ano_txt, servico, telefone_cliente,
            email_cliente, id_barbeiro, barbeiro, horario, telefone_remetente, email_remetente
        ) VALUES (
            :dt, :ano, :dia, :mes, :semana, :dia_da_semana, :ano_txt, :servico, :telefone_cliente,
            :email_cliente, :id_barbeiro, :barbeiro, :horario, :telefone_remetente, :email_remetente
        )
    """)

    with engine.connect() as connection:
        connection.execute(query, {
            "dt": dt,
            "ano": ano,
            "dia": dia,
            "mes": mes,
            "semana": semana,
            "dia_da_semana": dia_da_semana,
            "ano_txt": ano_txt,
            "servico": servico,
            "telefone_cliente": telefone_cliente,
            "email_cliente": email_cliente,
            "id_barbeiro": id_barbeiro,
            "barbeiro": barbeiro,
            "horario": horario,
            "telefone_remetente": telefone_remetente,
            "email_remetente": email_remetente
        })
        connection.commit()