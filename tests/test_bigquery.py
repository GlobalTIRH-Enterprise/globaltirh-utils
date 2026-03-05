import unittest
from unittest.mock import MagicMock, patch
from globaltirh_utils.functions.cloud.BigQuery import BigQueryHelper

class TestBigQueryHelper(unittest.TestCase):

    @patch("globaltirh_utils.functions.cloud.BigQuery.bigquery.Client")
    def setUp(self, mock_client):
        self.project_id = "test-project"
        self.bq_helper = BigQueryHelper(self.project_id)
        self.mock_client_instance = mock_client.return_value

    def test_create_dataset_success(self):
        self.mock_client_instance.create_dataset.return_value = MagicMock()
        result = self.bq_helper.create_dataset("dataset_test")
        self.assertTrue(result)
        self.mock_client_instance.create_dataset.assert_called_once()

    def test_create_dataset_already_exists(self):
        # Simula erro de "Already Exists"
        self.mock_client_instance.create_dataset.side_effect = Exception("Already Exists")
        result = self.bq_helper.create_dataset("dataset_test")
        self.assertTrue(result)  # Deve retornar True se já existe

    def test_create_dataset_error(self):
        self.mock_client_instance.create_dataset.side_effect = Exception("Generic Error")
        result = self.bq_helper.create_dataset("dataset_test")
        self.assertFalse(result)

    def test_create_table_success(self):
        self.mock_client_instance.create_table.return_value = MagicMock()
        result = self.bq_helper.create_table("dataset", "table", [])
        self.assertTrue(result)

    def test_insert_data_success(self):
        # insert_rows retorna uma lista de erros. Vazia = sucesso.
        self.mock_client_instance.insert_rows.return_value = []
        errors = self.bq_helper.insert_data("dataset", "table", [{"col": "val"}], [])
        self.assertEqual(errors, [])

    def test_insert_data_failure(self):
        expected_errors = [{"reason": "stopped"}]
        self.mock_client_instance.insert_rows.return_value = expected_errors
        errors = self.bq_helper.insert_data("dataset", "table", [{"col": "val"}], [])
        self.assertEqual(errors, expected_errors)

    def test_delete_table_success(self):
        self.mock_client_instance.delete_table.return_value = None
        result = self.bq_helper.delete_table("dataset", "table")
        self.assertTrue(result)

    def test_delete_table_error(self):
        self.mock_client_instance.delete_table.side_effect = Exception("Error")
        result = self.bq_helper.delete_table("dataset", "table")
        self.assertFalse(result)

    def test_get_data(self):
        # Mock do resultado da query
        mock_query_job = MagicMock()
        mock_row = MagicMock()
        mock_row.items.return_value = [("col1", "val1")]
        mock_query_job.result.return_value = [mock_row]
        
        self.mock_client_instance.query.return_value = mock_query_job

        # Teste com cláusula WHERE
        rows = self.bq_helper.get_data("dataset", "table", where_clauses={"id": 1})
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["col1"], "val1")
        
        # Verifica se a query foi construída corretamente
        args, _ = self.mock_client_instance.query.call_args
        self.assertIn("WHERE `id` = 1", args[0])

    def test_run_select_query_list(self):
        mock_query_job = MagicMock()
        mock_row = MagicMock()
        mock_row.items.return_value = [("colA", 100)]
        mock_query_job.result.return_value = [mock_row]
        self.mock_client_instance.query.return_value = mock_query_job

        result = self.bq_helper.run_select_query("SELECT * FROM table")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["colA"], 100)

    def test_run_select_query_dataframe(self):
        mock_query_job = MagicMock()
        mock_result = MagicMock()
        # Mock do método to_dataframe
        mock_result.to_dataframe.return_value = MagicMock(name="DataFrame") 
        mock_query_job.result.return_value = mock_result
        self.mock_client_instance.query.return_value = mock_query_job

        result = self.bq_helper.run_select_query("SELECT * FROM table", output_format="dataframe")
        # Verifica se chamou to_dataframe
        mock_result.to_dataframe.assert_called_once()

    def test_run_select_query_invalid(self):
        with self.assertRaises(ValueError):
            self.bq_helper.run_select_query("UPDATE table SET x=1")

if __name__ == "__main__":
    unittest.main()