# 🐱 Cat Facts Extractor

Este script realiza a extração de fatos sobre gatos a partir da API pública **Cat Facts**
e exporta os dados para um arquivo **CSV local**, já prontos para análise ou ingestão em
outras camadas do pipeline.
O foco aqui não é só “buscar dados”, mas lidar bem com **falhas reais de API**,
manter um **formato de saída previsível** e deixar o processo fácil de entender
e reproduzir.

## 🔍 O que o script faz

- 🔗 Consome o endpoint `/facts/random`
- ⚠️ Trata falhas da API (ex: `HTTP 503 – Service Unavailable`)
- 🧹 Normaliza os dados retornados para uma estrutura flat
- 🆔 Remove duplicidades com base no campo `_id`
- 📄 Gera um arquivo CSV com cabeçalho consistente
- 🕒 Registra logs claros para facilitar debug e acompanhamento

Mesmo quando a API está indisponível, o script **não quebra o fluxo**
e mantém o contrato de saída.

## ▶️ Como rodar ##

### 1️⃣ Crie e ative um ambiente virtual ###
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.\.venv\Scripts\activate    # Windows

### 2️⃣ Instale as dependências ###
pip install -r requirements.txt


### 3️⃣ Configure as variáveis de ambiente ###
cp example.env .env 

### 4️⃣ Execute o script ###
python extract_cat_facts.py

### ⚙️ Variáveis de Ambiente ###

As principais variáveis utilizadas pelo script são:
CAT_FACT_API_BASE_URL → URL base da API Cat Facts
CAT_FACT_ANIMAL_TYPE → Tipo de animal (padrão: cat)
CSV_OUTPUT_PATH → Caminho de saída do CSV
REQUEST_TIMEOUT → Timeout das requisições HTTP (em segundos)
SLEEP_BETWEEN_REQUESTS → Intervalo entre chamadas à API
DEFAULT_TOTAL → Total de fatos a serem buscados
DEFAULT_BATCH → Tamanho do batch por requisição

💡 antes de iniciar o script valida se existe as variaveis criticas

### 🧠 Observações ###

A API pública utilizada pode apresentar instabilidade (Heroku free dyno).
Esse cenário foi tratado de forma intencional, simulando integrações reais.
O código foi escrito priorizando clareza, previsibilidade e facilidade de manutenção..