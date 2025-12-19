
## ℹ️ℹ️ℹ️“Copie example.env para .env antes de rodar.”ℹ️ℹ️ℹ️ ##

## 🧭 Visão Geral

📌 Projeto desenvolvido para o case da Uol, simulando a evolução de uma startup desde uma extração simples de dados até uma arquitetura analítica escalável em nuvem.

⚠️ Durante o desenvolvimento, a API pública utilizada apresentou indisponibilidade constante (HTTP 503). Em vez de contornar ou ignorar esse cenário, a solução foi pensada para lidar com falhas reais de integração, mantendo contratos de dados estáveis e permitindo a evolução futura da arquitetura.
A indisponibilidade da API não foi tratada como um bloqueio, mas como parte do problema a ser resolvido

🧠 Essa abordagem reflete um cenário comum em ambientes de produção, onde dependências externas nem sempre estão disponíveis.

ℹ️  Obs: As configurações de ambiente (URL da API, timeouts, paths e parâmetros de execução)
foram isoladas em variáveis de ambiente (`.env`), seguindo boas práticas de segurança
e permitindo fácil adaptação entre ambientes local, cloud e CI/CD.


## 🐍 Questão 1 – Extração de Cat Facts (Python)

🐍 Foi desenvolvido um script simples em Python para extrair fatos sobre gatos a partir da API pública Cat Facts, seguindo a documentação oficial do projeto.

🚨 Durante os testes, a API apresentou instabilidade contínua. Todos os endpoints testados (/facts e /facts/random) retornaram erro HTTP 503 (Service Unavailable), indicando que o backend da aplicação (Heroku free dyno) está fora do ar ou descontinuado.

🛠️ Mesmo com essa limitação externa, optei por manter o script como se estivesse lidando com um cenário real de produção:

🛡️ Lidar de forma resiliente com falhas de API

🔁 Realizar múltiplas tentativas de coleta

📄 Manter o contrato de saída dos dados

💾 Gerar o arquivo CSV local com cabeçalho, mesmo quando não há registros

✅ Com isso, o pipeline permanece estável e previsível, algo essencial em integrações com serviços externos que podem ficar indisponíveis temporariamente.

## ☁️ Questão 2 – Arquitetura em Nuvem (Google Cloud)

☁️ Abaixo está uma proposta simples de arquitetura em Google Cloud para substituir a solução local, permitindo extrair, armazenar e disponibilizar os dados de forma escalável para o usuário final.

🏗️ Essa arquitetura foi pensada para crescer junto com o volume de dados e, se necessário, pode ser implementada sem grandes mudanças estruturais.

┌──────────────────────────┐
│ Cat Facts API (External) │
└─────────────┬────────────┘
              │ HTTPS
              v
┌────────────────────────────────┐
│ Cloud Run – Extract Service     │
│ - Consume /facts/random         │
│ - Payload validation            │
│ - Logging & error handling      │
└─────────────┬──────────────────┘
              │ Events
              v
┌────────────────────────────────┐
│ Pub/Sub                        │
│ Topic: cat-facts-raw            │
│ - Decoupling                   │
│ - Automatic retries            │
└─────────────┬──────────────────┘
              │
              v
┌────────────────────────────────┐
│ Processing (Dataflow / Run)    │
│ - Normalization                │
│ - Deduplication (_id)          │
│ - Enrichment                   │
└─────────────┬─────────┬────────┘
              │ RAW     │ CURATED
              v         v
┌──────────────────┐   ┌────────────────────┐
│ Cloud Storage     │   │ BigQuery            │
│ bucket/raw        │   │ dataset.cat_facts  │
│ jsonl / csv       │   │ analytic table     │
└──────────┬────────┘   └──────────┬─────────┘
           │                        │
           v                        v
 Reprocessing / Audit        Looker / SQL / Apps

┌──────────────────────────┐
│ Cloud Scheduler           │
│ - Triggers ingestion      │
└──────────────────────────┘



## 🧠 Considerações de Arquitetura

⚙️ Cloud Run foi escolhido por ser serverless, simples de operar e escalar automaticamente conforme a demanda.

📬 Pub/Sub desacopla a ingestão do processamento, evitando perda de dados em cenários de falha ou picos de volume.

🧱 Cloud Storage (RAW) mantém os dados originais, permitindo auditoria e reprocessamento quando necessário.

📊 BigQuery funciona como a camada analítica final, facilitando o consumo pelo time de analytics.

🚀 Essa arquitetura permite evoluir facilmente para um modelo near real-time no futuro, sem mudanças estruturais grandes.

ℹ️ Obs: para um volume pequeno, Cloud Functions também seria viável. A escolha do Cloud Run foi feita pensando em evolução de carga, controle de dependências e facilidade de versionamento do serviço.

## 🧾 Questão 3 – Esquema da Tabela (BigQuery)

🧾 Esse esquema foi modelado para suportar consultas analíticas, auditoria e possíveis evoluções futuras do pipeline.

📂 sql no caminho abaixo

sql/bigquery/01_create_table_cat_facts.sql

## 📊 Questão 4 – Consulta de Fatos Atualizados (BigQuery)

📊 Para apoiar o time de analytics, foi criada uma consulta SQL que extrai todos os fatos sobre gatos que foram atualizados durante o mês de agosto de 2020.
⏱️ A consulta utiliza o campo updated_at como TIMESTAMP e trabalha com intervalo fechado/aberto para garantir precisão temporal.

📂 O SQL ta no caminho abaixo

sql/bigquery/02_select_cat_facts_updated_aug_2020.sql

## 🎲 Questão 5 – Amostra Aleatória para QA (BigQuery)

🎲 Para atender o time de desenvolvimento, foi criada uma consulta SQL que extrai uma amostra aleatória de 100 registros da base de fatos sobre gatos.

🧪 A consulta retorna apenas os campos necessários para o ambiente de QA:

📝Texto do fato

📅Data de criação

⏱️Data de atualização

📤O resultado pode ser exportado diretamente para um arquivo CSV separado por vírgulas utilizando as funcionalidades nativas do BigQuery.

📂sql no caminho abaixo

sql/bigquery/03_sample_cat_facts_for_qa.sql

## 🔮 Próximos Passos Possíveis

🧬 Implementar controle de versionamento de schema

🧪 Criar testes automatizados para o extrator

📡 Adicionar monitoramento e alertas (Cloud Monitoring)

🔁 Implementar carga incremental baseada em updated_at