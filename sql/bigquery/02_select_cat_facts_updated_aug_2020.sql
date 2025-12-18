-- Consulta para extrair fatos de gatos atualizados em agosto de 2020
SELECT
  _id,
  text,
  type,
  source,
  deleted,
  created_at,
  updated_at,
  status_verified,
  status_sent_count
FROM `project_id.dataset.cat_facts`
WHERE updated_at >= TIMESTAMP('2020-08-01')
  AND updated_at <  TIMESTAMP('2020-09-01')
ORDER BY updated_at;
