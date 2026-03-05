from google.cloud import bigquery
from utils_global.CreateLogger import log
from typing import List, Dict, Optional, Union


def get_data(
    client: bigquery.Client,
    dataset_id: str,
    table_id: str,
    where_clauses: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    limit: int = 0
) -> List[Dict]:
    """Recupera dados de uma tabela do BigQuery com filtros opcionais.

    Args:
        client: Cliente autenticado do BigQuery.
        dataset_id: ID do dataset que contém a tabela.
        table_id: ID da tabela para consulta.
        where_clauses: Dicionário com colunas e valores para filtro (ex.: {'coluna': 'valor'}).
        limit: Número máximo de linhas a retornar (0 = sem limite).

    Returns:
        Lista de dicionários com os dados recuperados. Lista vazia se nenhum dado ou erro.
    """
    query = f"SELECT * FROM `{client.project}.{dataset_id}.{table_id}`"

    if where_clauses:
        conditions = []
        for col, val in where_clauses.items():
            if isinstance(val, str):
                conditions.append(f"`{col}` = '{val}'")
            else:
                conditions.append(f"`{col}` = {val}")
        query += " WHERE " + " AND ".join(conditions)

    if limit:
        query += f" LIMIT {limit}"

    try:
        query_job = client.query(query)
        results = query_job.result()
        rows = [dict(row.items()) for row in results]
        log.debug(f"Recuperadas {len(rows)} linhas de {client.project}.{dataset_id}.{table_id}")
        return rows
    except Exception as e:
        log.error(f"Erro ao recuperar dados de {client.project}.{dataset_id}.{table_id}: {e}")
        return []