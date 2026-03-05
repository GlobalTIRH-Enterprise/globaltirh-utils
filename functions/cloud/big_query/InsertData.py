from google.cloud import bigquery
from globaltirh_utils.CreateLogger import log
from typing import List, Dict, Any


def insert_data(
    client: bigquery.Client,
    dataset_id: str,
    table_id: str,
    rows_to_insert: List[Dict],
    schema: List[bigquery.SchemaField]
) -> List[Dict[str, Any]]:
    """Insere dados em uma tabela do BigQuery.

    Args:
        client: Cliente autenticado do BigQuery.
        dataset_id: ID do dataset que contém a tabela.
        table_id: ID da tabela para inserir os dados.
        rows_to_insert: Lista de dicionários representando as linhas.
        schema: Esquema da tabela (lista de SchemaField).

    Returns:
        Lista de erros encontrados durante a inserção; lista vazia indica sucesso.
    """
    table_ref = client.dataset(dataset_id).table(table_id)
    errors = client.insert_rows(table_ref, rows_to_insert, selected_fields=schema)
    if errors:
        log.error(f"Encontrados erros ao inserir as linhas: {errors}")
    else:
        log.debug(f"Inseridas {len(rows_to_insert)} linhas em {client.project}.{dataset_id}.{table_id}")
    return list(errors)