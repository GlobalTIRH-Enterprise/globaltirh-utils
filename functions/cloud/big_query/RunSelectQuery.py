from google.cloud import bigquery
from utils.CreateLogger import log
from typing import List, Dict, Union
from pandas import DataFrame


def run_select_query(
    client: bigquery.Client,
    query: str,
    output_format: str = "list"
) -> Union[List[Dict], DataFrame]:
    """Executa uma consulta SELECT e retorna os resultados como lista ou DataFrame.

    Args:
        client: Cliente autenticado do BigQuery.
        query: Consulta SQL contendo SELECT.
        output_format: 'list' (padrão) para lista de dicionários ou 'dataframe' para pandas DataFrame.

    Returns:
        Resultados no formato solicitado. Lista vazia ou DataFrame vazio em caso de erro.

    Raises:
        ValueError: Se a query não contiver SELECT ou o formato for inválido.
    """
    if "select" not in query.lower():
        raise ValueError("A query deve conter um 'select'.")

    allowed = ["list", "dataframe"]
    if output_format.lower() not in allowed:
        raise ValueError(f"Formato inválido. Use um de: {allowed}")

    try:
        query_job = client.query(query)
        results = query_job.result()
        if output_format.lower() == "dataframe":
            df = results.to_dataframe()
            log.debug(f"Consulta executada. Retornadas {len(df)} linhas como DataFrame.")
            return df
        rows = [dict(row.items()) for row in results]
        log.debug(f"Consulta executada. Retornadas {len(rows)} linhas como lista.")
        return rows
    except Exception as e:
        log.error(f"Erro ao executar a consulta: {e}")
        return DataFrame() if output_format.lower() == "dataframe" else []