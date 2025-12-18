CREATE TABLE dataset.cat_facts (
  id STRING,
  text STRING,
  type STRING,
  source STRING,
  deleted BOOL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  status_verified BOOL,
  status_sent_count INT64,
  ingested_at TIMESTAMP
);
