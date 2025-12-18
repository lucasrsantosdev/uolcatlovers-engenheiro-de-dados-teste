-- Questão 5
-- Amostra aleatória de 100 fatos sobre gatos para ambiente de QA
-- Resultado pode ser exportado como CSV separado por vírgulas no BigQuery

SELECT
  text,
  created_at,
  updated_at
FROM `project_id.dataset.cat_facts`
ORDER BY RAND()
LIMIT 100;
