# UOL Cat Lovers - Engenharia de Dados Teste

Projeto desenvolvido para o case técnico da UOL, simulando a evolução de uma startup que consome dados da API pública Cat Facts.

O objetivo do projeto é demonstrar:

* extração de dados via Python
* persistência local em CSV
* modelagem analítica no BigQuery
* consultas SQL
* proposta de arquitetura escalável em Google Cloud

---

# Estrutura do Projeto

```text
.
├── data/
│   └── uolcatlovers_cat_facts.csv
├── sql/
│   └── bigquery/
│       ├── 01_create_table_cat_facts.sql
│       ├── 02_select_cat_facts_updated_aug_2020.sql
│       └── 03_sample_cat_facts_for_qa.sql
├── src/
│   └── extract_cat_facts.py
├── .env.example
├── requirements.txt
└── README.md
```

---

# Configuração

Copie o arquivo `.env.example` para `.env` antes de executar o projeto.

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python src/extract_cat_facts.py
```

---

# Questão 1 - Extração de Cat Facts

Foi desenvolvido um script Python para consumir a API pública Cat Facts e exportar os dados para um arquivo CSV local.

Durante os testes, a API apresentou indisponibilidade recorrente (HTTP 503). O script foi mantido resiliente para lidar com falhas transitórias sem interromper o pipeline.

Principais pontos implementados:

* tratamento de erros de integração
* timeout configurável
* deduplicação por `_id`
* normalização dos dados
* exportação para CSV
* configuração via variáveis de ambiente
* logging básico de execução

O arquivo CSV é gerado mesmo em cenários sem retorno da API, preservando o contrato de saída do processo.

Arquivo principal:

```text
src/extract_cat_facts.py
```

---

# Questão 2 - Arquitetura Google Cloud

A arquitetura proposta desacopla ingestão, processamento e consumo analítico dos dados.

Fluxo proposto:

```text
Cat Facts API
    ↓
Cloud Run (Extract)
    ↓
Pub/Sub
    ↓
Cloud Run / Dataflow (Process)
    ↓
Cloud Storage (RAW)
    ↓
BigQuery
    ↓
Analytics / BI
```

Componentes utilizados:

* Cloud Run
* Pub/Sub
* Cloud Storage
* BigQuery
* Cloud Scheduler

Objetivos da arquitetura:

* escalabilidade
* tolerância a falhas
* reprocessamento
* desacoplamento entre etapas
* consumo analítico simplificado

---

# Questão 3 - Schema BigQuery

O schema analítico da tabela de fatos foi especificado em SQL considerando:

* tipagem adequada
* rastreabilidade
* auditoria
* possibilidade de evolução futura

Arquivo:

```text
sql/bigquery/01_create_table_cat_facts.sql
```

---

# Questão 4 - Consulta de fatos atualizados em agosto de 2020

Foi criada uma consulta SQL para retornar os fatos atualizados durante agosto de 2020 utilizando o campo `updated_at`.

Arquivo:

```text
sql/bigquery/02_select_cat_facts_updated_aug_2020.sql
```

---

# Questão 5 - Amostra aleatória para QA

Foi criada uma consulta SQL para extrair 100 registros aleatórios contendo:

* texto
* data de criação
* data de atualização

O resultado pode ser exportado diretamente para CSV via BigQuery.

Arquivo:

```text
sql/bigquery/03_sample_cat_facts_for_qa.sql
```

---

# Possíveis Evoluções

* carga incremental baseada em `updated_at`
* monitoramento e alertas
* testes automatizados
* controle de versionamento de schema
* orquestração completa do pipeline
