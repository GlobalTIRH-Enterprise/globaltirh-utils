from google.cloud import bigquery
from helpers import log
from typing import List


def create_table(
    client: bigquery.Client,
    dataset_id: str,
    table_id: str,
    schema: List[bigquery.SchemaField]
) -> bool:
    """Cria uma nova tabela no BigQuery.

    Args:
        client: Cliente autenticado do BigQuery.
        dataset_id: ID do dataset onde a tabela será criada.
        table_id: ID da tabela a ser criada.
        schema: Lista de objetos SchemaField definindo o esquema.

    Returns:
        True se a tabela foi criada ou já existia, False em caso de erro.
    """
    table_ref = client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref, schema=schema)

    try:
        client.create_table(table)
        log.debug(f"Tabela criada {client.project}.{dataset_id}.{table_id}")
        return True
    except Exception as e:
        if "Already Exists" in str(e):
            log.debug(f"Tabela {client.project}.{dataset_id}.{table_id} já existe.")
            return True
        log.error(f"Erro ao criar a tabela {client.project}.{dataset_id}.{table_id}: {e}")
        return False