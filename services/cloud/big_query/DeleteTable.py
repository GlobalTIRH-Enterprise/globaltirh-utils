from google.cloud import bigquery
from helpers import log


def delete_table(
    client: bigquery.Client,
    dataset_id: str,
    table_id: str,
    must_exist: bool = False
) -> bool:
    """Exclui uma tabela do BigQuery.

    Args:
        client: Cliente autenticado do BigQuery.
        dataset_id: ID do dataset que contém a tabela.
        table_id: ID da tabela a ser excluída.
        must_exist: Se True, gera erro se a tabela não existir.

    Returns:
        True se a tabela foi excluída ou não existia (com must_exist=False), False em caso de erro.
    """
    table_ref = client.dataset(dataset_id).table(table_id)
    try:
        client.delete_table(table_ref, not_found_ok=not must_exist)
        log.debug(f"Tabela excluída {client.project}.{dataset_id}.{table_id}")
        return True
    except Exception as e:
        log.error(f"Erro ao excluir a tabela {client.project}.{dataset_id}.{table_id}: {e}")
        return False