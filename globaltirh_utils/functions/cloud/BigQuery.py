from os import getenv
from google.cloud import bigquery
from globaltirh_utils.CreateLogger import log
from typing import List, Dict, Optional, Union, Any
from pandas import DataFrame



class BigQueryHelper:
    """
    Classe auxiliar para interagir com o Google BigQuery.
    """

    def __init__(self, project_id: str):
        """
        Inicializa o BigQueryHelper com o ID do projeto.

        Args:
            project_id (str): O ID do seu projeto Google Cloud.
        """
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id

    def create_dataset(
        self, dataset_id: str, location: str = "US", description: Optional[str] = None
    ) -> bool:
        """
        Cria um novo dataset no BigQuery.

        Args:
            dataset_id (str): O ID do dataset a ser criado.
            location (str, optional): A localização do dataset. O padrão é "US".
            description (str, optional): Uma descrição para o dataset. O padrão é None.

        Returns:
            bool: True se o dataset foi criado com sucesso, False caso contrário. Retorna True se o dataset já existir.
        """
        dataset_ref = self.client.dataset(dataset_id)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location

        if description:
            dataset.description = description

        try:
            self.client.create_dataset(dataset)  # Faz uma requisição à API.
            log.debug(f"Dataset criado {self.project_id}.{dataset_id}")
            return True
        except Exception as e:
            if "Already Exists" in str(e):
                log.debug(f"Dataset {self.project_id}.{dataset_id} já existe.")
                return True
            else:
                log.error(f"Erro ao criar o dataset {self.project_id}.{dataset_id}: {e}")
                return False

    def create_table(
        self, dataset_id: str, table_id: str, schema: List[bigquery.SchemaField]
    ) -> bool:
        """
        Cria uma nova tabela no BigQuery.

        Args:
            dataset_id (str): O ID do dataset onde a tabela será criada.
            table_id (str): O ID da tabela a ser criada.
            schema (list): Uma lista de objetos bigquery.SchemaField definindo o esquema da tabela.

        Returns:
            bool: True se a tabela foi criada com sucesso, False caso contrário. Retorna True se a tabela já existir.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = bigquery.Table(table_ref, schema=schema)

        try:
            self.client.create_table(table)  # Faz uma requisição à API.
            log.debug(f"Tabela criada {self.project_id}.{dataset_id}.{table_id}")
            return True
        except Exception as e:
            if "Already Exists" in str(e):
                log.debug(f"Tabela {self.project_id}.{dataset_id}.{table_id} já existe.")
                return True
            else:
                log.error(f"Erro ao criar a tabela {self.project_id}.{dataset_id}.{table_id}: {e}")
                return False

    def insert_data(
        self,
        dataset_id: str,
        table_id: str,
        rows_to_insert: List[Dict],
        schema: List[bigquery.SchemaField],
    ) -> List[Dict[str, Any]]:
        """
        Insere dados em uma tabela do BigQuery.

        Args:
            dataset_id (str): O ID do dataset que contém a tabela.
            table_id (str): O ID da tabela para inserir os dados.
            rows_to_insert (list): Uma lista de dicionários, onde cada dicionário representa uma linha a ser inserida.
                                    As chaves no dicionário devem corresponder aos nomes das colunas na tabela.
            schema (list): Uma lista de objetos bigquery.SchemaField definindo o esquema da tabela.

        Returns:
            list: Uma lista de erros (se houver) encontrados durante a inserção. Uma lista vazia significa sucesso.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        errors = self.client.insert_rows(
            table_ref, rows_to_insert, selected_fields=schema
        )  # Faz uma requisição à API.
        if errors:
            log.error(f"Encontrados erros ao inserir as linhas: {errors}")
        else:
            log.debug(
                f"Inseridas {len(rows_to_insert)} linhas em {self.project_id}.{dataset_id}.{table_id}"
            )
        return list(errors)

    def delete_table(self, dataset_id: str, table_id: str, must_exist: bool = False) -> bool:
        """
        Exclui uma tabela do BigQuery.

        Args:
            dataset_id (str): O ID do dataset que contém a tabela.
            table_id (str): O ID da tabela a ser excluída.
            must_exist (bool, optional): Se um erro deve ser gerado se a tabela não existir. O padrão é False.

        Returns:
            bool: True se a tabela foi excluída com sucesso, False caso contrário.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)

        try:
            self.client.delete_table(
                table_ref, not_found_ok=not must_exist
            )  # Faz uma requisição à API.
            log.error(f"Tabela excluída {self.project_id}.{dataset_id}.{table_id}")
            return True
        except Exception as e:
            log.debug(f"Erro ao excluir a tabela {self.project_id}.{dataset_id}.{table_id}: {e}")
            return False

    def get_data(
        self,
        dataset_id: str,
        table_id: str,
        where_clauses: Optional[Dict[str, Union[str, int, float, bool]]] = None,
        limit: int = 0,
    ) -> List[Dict]:
        """
        Recupera dados de uma tabela do BigQuery com base em condições especificadas.

        Args:
            dataset_id (str): O ID do dataset que contém a tabela.
            table_id (str): O ID da tabela para recuperar os dados.
            where_clauses (dict, optional): Um dicionário onde as chaves são nomes de colunas e os valores são os valores desejados para filtragem.
                                            O padrão é None (sem filtragem). Exemplo: `{'column1': 'value1', 'column2': 123}`
            limit (int, optional): O número máximo de linhas a serem retornadas. O padrão é 0 (sem limite).

        Returns:
            list: Uma lista de linhas, onde cada linha é um dicionário representando os dados. Retorna uma lista vazia se nenhum dado corresponder aos critérios.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = self.client.get_table(
            table_ref
        )  # Faz uma requisição à API para obter os metadados da tabela

        query = f"SELECT * FROM `{self.project_id}.{dataset_id}.{table_id}`"

        if where_clauses:
            where_conditions = []
            for column, value in where_clauses.items():
                # Lida com diferentes tipos de dados para valores na cláusula WHERE
                if isinstance(value, str):
                    where_conditions.append(
                        f"`{column}` = '{value}'"
                    )  # Coloca valores de string entre aspas
                else:
                    where_conditions.append(
                        f"`{column}` = {value}"
                    )  # Sem aspas para números, booleanos, etc.

            query += " WHERE " + " AND ".join(where_conditions)

        if limit:
            query += f" LIMIT {limit}"

        try:
            query_job = self.client.query(query)  # Faz uma requisição à API.
            results = list(query_job.result())  # Aguarda a conclusão do trabalho.

            # Converte objetos Row em dicionários para facilitar o uso
            rows = [dict(row.items()) for row in results]
            log.debug(
                f"Recuperadas {len(rows)} linhas de {self.project_id}.{dataset_id}.{table_id}"
            )
            return rows
        except Exception as e:
            log.error(f"Erro ao recuperar dados de {self.project_id}.{dataset_id}.{table_id}: {e}")
            return []

    def run_select_query(
        self, query: str, output_format: str = "list"
    ) -> Union[List[Dict], DataFrame]:
        """
        Executa uma consulta SELECT no BigQuery e retorna os resultados como uma lista de dicionários
        ou um DataFrame do pandas.

        Args:
            query (str): A consulta SQL a ser executada.
            output_format (str, optional): O formato de saída desejado.
                                            Pode ser 'list' (padrão) ou 'dataframe'.

        Returns:
            Union[List[Dict], pd.DataFrame]: Os resultados da consulta no formato especificado.
                                            Retorna uma lista vazia ou DataFrame vazio em caso de erro.

        Raises:
            ValueError: Se a query não for do tipo SELECT ou se o formato de saída for inválido.
        """
        if "select" not in query.lower():
            raise ValueError("A query deve conter um 'select'.")

        # Validação do formato de saída
        allowed_formats = ["list", "dataframe"]
        if output_format.lower() not in allowed_formats:
            raise ValueError(f"Formato de saída inválido. Use um dos seguintes: {allowed_formats}")

        try:
            query_job = self.client.query(query)
            results = query_job.result()  # Isso retorna um RowIterator

            if output_format.lower() == "dataframe":
                # O método .to_dataframe() é a forma mais eficiente de converter para pandas DataFrame
                df = results.to_dataframe()
                log.debug(f"Consulta executada. Retornadas {len(df)} linhas como DataFrame.")
                return df
            else:  # O padrão é 'list'
                # Converte o RowIterator em uma lista de dicionários
                rows = [dict(row.items()) for row in results]
                log.debug(
                    f"Consulta executada. Retornadas {len(rows)} linhas como lista de dicionários."
                )
                return rows

        except Exception as e:
            log.error(f"Erro ao executar a consulta: {e}")

            if isinstance(output_format, str) and output_format.lower() == "dataframe":
                return DataFrame()
            return []
