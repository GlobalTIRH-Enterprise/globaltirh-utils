from google.cloud import bigquery
from helpers import log
from typing import Optional


def create_dataset(
    client: bigquery.Client,
    dataset_id: str,
    location: str = "US",
    description: Optional[str] = None
) -> bool:
    """Cria um novo dataset no BigQuery.

    Args:
        client: Cliente autenticado do BigQuery.
        dataset_id: ID do dataset a ser criado.
        location: Localização do dataset (padrão "US").
        description: Descrição opcional do dataset.

    Returns:
        True se o dataset foi criado ou já existia, False em caso de erro.
    """
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = location
    if description:
        dataset.description = description

    try:
        client.create_dataset(dataset)
        log.debug(f"Dataset criado {client.project}.{dataset_id}")
        return True
    except Exception as e:
        if "Already Exists" in str(e):
            log.debug(f"Dataset {client.project}.{dataset_id} já existe.")
            return True
        log.error(f"Erro ao criar o dataset {client.project}.{dataset_id}: {e}")
        return False