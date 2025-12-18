## Questão 1 – Extração de Cat Facts (Python)

Desenvolvi um script simples em Python para extrair fatos sobre gatos a partir da API pública Cat Facts, seguindo a documentação oficial do projeto.

Durante os testes, a API apresentou instabilidade constante. Todos os endpoints testados (/facts e /facts/random) retornaram erro HTTP 503 (Service Unavailable), o que indica que o backend da aplicação (Heroku free dyno) está fora do ar ou descontinuado.

Mesmo com essa limitação externa, o script foi pensado para funcionar em um cenário real, então ele foi construído para:

Lidar bem com falhas de API

Tentar a coleta mais de uma vez

Manter o formato de saída esperado

Gerar o arquivo CSV local com cabeçalho, mesmo quando não há dados

Com isso, o pipeline continua estável e previsível, algo comum e necessário quando lidamos com integrações externas que podem ficar indisponíveis.

## Questão 2 – Arquitetura em Nuvem (Google Cloud)

Abaixo está uma proposta simples de arquitetura em Google Cloud para substituir a solução local, permitindo extrair, armazenar e disponibilizar os dados de forma escalável para o usuário final.
Se necessário, essa arquitetura poderia ser implementada sem grandes mudanças.

┌──────────────────────┐
│  Cat Facts API (Ext) │
└──────────┬───────────┘
           │ HTTPS
           v
┌───────────────────────────────┐
│ Cloud Run – Extract Service    │
│ - Consome /facts               │
│ - Valida payload               │
│ - Publica eventos              │
└──────────┬────────────────────┘
           │
           v
┌───────────────────────────────┐
│ Pub/Sub                       │
│ topic: cat-facts-raw           │
│ - desacoplamento               │
│ - retries automáticos          │
└──────────┬────────────────────┘
           │
           v
┌───────────────────────────────┐
│ Dataflow / Cloud Run (Process) │
│ - Normalização                 │
│ - Deduplicação por _id         │
│ - Enriquecimento               │
└──────────┬───────────┬────────┘
           │ RAW       │ Curated
           v           v
┌─────────────────┐   ┌──────────────────┐
│ Cloud Storage   │   │ BigQuery          │
│ bucket/raw      │   │ dataset.cat_facts │
│ - jsonl / csv   │   │ - tabela analítica│
└──────────┬──────┘   └─────────┬────────┘
           │                    │
           v                    v
   Reprocesso / Auditoria   Looker / App / SQL

┌──────────────────────────┐
│ Cloud Scheduler           │
│ - dispara ingestão        │
└──────────────────────────┘

Considerações de Arquitetura

Cloud Run foi escolhido por ser simples, serverless e escalar automaticamente conforme a demanda.

Pub/Sub desacopla a ingestão do processamento, evitando perda de dados em caso de falhas ou picos.

Cloud Storage (RAW) armazena os dados originais, permitindo auditoria e reprocessamento.

BigQuery funciona como a camada final analítica, facilitando o consumo pelo time de analytics.

Essa arquitetura permite evoluir facilmente para um modelo near real-time no futuro, sem mudanças estruturais grandes.

## Questao 3: Referenciar isso no README
O esquema da tabela em BigQuery está definido em: `sql/bigquery/01_create_table_cat_facts.sql`.

## Questão 4 – Consulta de Fatos Atualizados (BigQuery)

Para apoiar o time de analytics, foi criada uma consulta SQL que extrai todos os fatos sobre gatos que foram atualizados durante o mês de agosto de 2020.

A consulta considera o campo `updated_at` como `TIMESTAMP` e utiliza um intervalo fechado/aberto para garantir precisão temporal.

O SQL está disponível em:

sql/bigquery/02_select_cat_facts_updated_aug_2020.sql

## Questão 5 – Amostra Aleatória para QA (BigQuery)

Para atender o time de desenvolvimento, foi criada uma consulta SQL que extrai uma amostra aleatória de 100 registros da base de fatos sobre gatos.

A consulta retorna apenas os campos necessários para o ambiente de QA:
- texto do fato
- data de criação
- data de atualização

O resultado da query pode ser exportado diretamente para um arquivo CSV separado por vírgulas utilizando as funcionalidades nativas do BigQuery.

O SQL está disponível em:

sql/bigquery/03_sample_cat_facts_for_qa.sql

