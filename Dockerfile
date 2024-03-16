FROM python:3.12.2-slim-bookworm

# Adiciona pacotes necessários para compilar dependências Python
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Define o diretório de trabalho dentro do contêiner
WORKDIR /crawler

# Copia apenas o arquivo de requisitos primeiro
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação para o diretório de trabalho
COPY . .

# Define o comando a ser executado quando o contêiner for iniciado
CMD ["python", "crawler/update_price.py"]