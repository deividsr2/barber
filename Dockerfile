# Use uma imagem base do Python
FROM python:3.12-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta que o Streamlit utiliza (8501 por padrão)
EXPOSE 8501

# Comando para rodar o aplicativo
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
