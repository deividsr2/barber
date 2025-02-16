import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from conexao import engine  # Importa sua conexão do arquivo onde está definida

# Criar sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Carregar os dados do JSON
with open("barbeiros.json", "r", encoding="utf-8") as f:
    barbeiros_data = json.load(f)

# Atualizar os nomes dos barbeiros
for idx, nome in enumerate(barbeiros_data["nomes"], start=1):
    session.execute(
        text("UPDATE barber_teste_barbeiros SET barbeiro = :nome WHERE id = :id"),
        {"nome": nome, "id": idx}
    )

# Atualizar apenas os apelidos
for idx, apelido in enumerate(barbeiros_data["apelidos"], start=1):
    session.execute(
        text("UPDATE barber_teste_barbeiros SET apelido = :apelido WHERE id = :id"),
        {"apelido": apelido, "id": idx}
    )

# Commit e fechar sessão
session.commit()
session.close()

print("Dados atualizados com sucesso!")
