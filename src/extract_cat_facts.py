import os
from datetime import datetime
import csv
import logging
import time
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

# =========================
# 🔧 ENV / CONFIG
# =========================
load_dotenv()

BASE_URL = os.getenv("CAT_FACT_API_BASE_URL")
ANIMAL_TYPE = os.getenv("CAT_FACT_ANIMAL_TYPE", "cat")

CSV_PATH = os.getenv("CSV_OUTPUT_PATH", "data/cat_facts.csv")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
SLEEP_BETWEEN_REQUESTS = int(os.getenv("SLEEP_BETWEEN_REQUESTS", 2))
DEFAULT_TOTAL = int(os.getenv("DEFAULT_TOTAL", 100))
DEFAULT_BATCH = int(os.getenv("DEFAULT_BATCH", 1))

# ✅ validação explícita (local correto)
if not BASE_URL:
    raise ValueError(
        "CAT_FACT_API_BASE_URL não definido. "
        "Verifique o arquivo .env (use example.env como base)."
    )

# =========================
# 📌 LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

# =========================
# 🔌 CONSUMO DA API
# =========================

# A API pode retornar 503 (Heroku free dyno descontinuado)
# Esse comportamento é tratado como falha transitória

def fetch_cat_facts(amount: int) -> List[Dict[str, Any]]:
    """
    Busca fatos de gatos na API.
    Retorna lista de fatos (dict). Em erro, retorna lista vazia.
    """
    url = f"{BASE_URL}/facts/random"
    params = {
        "animal_type": ANIMAL_TYPE,
        "amount": amount,
    }

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            logging.warning(
                "Falha na API Cat Facts | status=%s | url=%s",
                response.status_code,
                url,
            )
            return []

        data = response.json()

        # amount=1 geralmente retorna objeto, não lista
        if isinstance(data, dict):
            return [data]

        if isinstance(data, list):
            return data

        logging.warning("Formato inesperado de resposta da API")
        return []

    except requests.RequestException as exc:
        logging.warning("Erro de request na API Cat Facts: %s", exc)
        return []

    except requests.RequestException as exc:
        logging.warning("Erro de request na API Cat Facts: %s", exc)
        return []

# =========================
# 🔄 NORMALIZAÇÃO
# =========================
def normalize_fact(fact: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza um fato da API para estrutura flat.
    """
    status = fact.get("status") or {}

    return {
        "_id": fact.get("_id"),
        "text": fact.get("text"),
        "type": fact.get("type"),
        "source": fact.get("source"),
        "deleted": fact.get("deleted"),
        "created_at": fact.get("createdAt"),
        "updated_at": fact.get("updatedAt"),
        "status_verified": status.get("verified"),
        "status_sent_count": status.get("sentCount"),
        "ingested_at": datetime.utcnow().isoformat(),
    }


# =========================
# 💾 EXPORTAÇÃO CSV
# =========================
def export_to_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Header padrão do projeto
    fieldnames = [
        "_id",
        "text",
        "type",
        "source",
        "deleted",
        "created_at",
        "updated_at",
        "status_verified",
        "status_sent_count",
        "ingested_at",
    ]

    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    logging.info(
        "Exportação finalizada: %s (%d registros)", path, len(rows)
    )


# =========================
# ▶️ EXECUÇÃO PRINCIPAL
# =========================
def main(
    total: int = DEFAULT_TOTAL,
    batch: int = DEFAULT_BATCH,
) -> None:
    logging.info("Iniciando extração de Cat Facts")
    logging.info("Total desejado: %d | Batch: %d", total, batch)

    resultados: Dict[str, Dict[str, Any]] = {}
    restantes = total

    failed_batches = 0  

    while restantes > 0:
        quantidade = min(batch, restantes)
        logging.info("Buscando %d fato(s) na API", quantidade)

        fatos = fetch_cat_facts(quantidade)

        if not fatos:
            failed_batches += 1  
            logging.warning("Nenhum dado retornado neste batch. Continuando...")
            restantes -= quantidade
            time.sleep(SLEEP_BETWEEN_REQUESTS)
            continue

        for fato in fatos:
            normalizado = normalize_fact(fato)
            fact_id = normalizado.get("_id")
            if fact_id:
                resultados[fact_id] = normalizado

        restantes -= quantidade
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    export_to_csv(CSV_PATH, list(resultados.values()))
    
    logging.info(
        "Processo finalizado | Registros únicos: %d | Batches com falha: %d",
        len(resultados),
        failed_batches,
    )



if __name__ == "__main__":
    main()
