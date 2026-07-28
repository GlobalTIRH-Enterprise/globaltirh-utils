import unittest
from unittest.mock import MagicMock, patch

from services.cloud.big_query import (
    create_dataset,
    create_table,
    insert_data,
    delete_table,
    get_data,
    run_select_query,
)


class TestBigQueryFunctions(unittest.TestCase):

    def setUp(self):
        self.project_id = "test-project"
        self.mock_client = MagicMock()
        self.mock_client.project = self.project_id

    def test_create_dataset_success(self):
        self.mock_client.create_dataset.return_value = MagicMock()
        result = create_dataset(self.mock_client, "dataset_test")
        self.assertTrue(result)
        self.mock_client.create_dataset.assert_called_once()

    def test_create_dataset_already_exists(self):
        self.mock_client.create_dataset.side_effect = Exception("Already Exists")
        result = create_dataset(self.mock_client, "dataset_test")
        self.assertTrue(result)

    def test_create_dataset_error(self):
        self.mock_client.create_dataset.side_effect = Exception("Generic Error")
        result = create_dataset(self.mock_client, "dataset_test")
        self.assertFalse(result)

    def test_create_table_success(self):
        self.mock_client.create_table.return_value = MagicMock()
        result = create_table(self.mock_client, "dataset", "table", [])
        self.assertTrue(result)

    def test_insert_data_success(self):
        self.mock_client.insert_rows.return_value = []
        errors = insert_data(self.mock_client, "dataset", "table", [{"col": "val"}], [])
        self.assertEqual(errors, [])

    def test_insert_data_failure(self):
        expected_errors = [{"reason": "stopped"}]
        self.mock_client.insert_rows.return_value = expected_errors
        errors = insert_data(self.mock_client, "dataset", "table", [{"col": "val"}], [])
        self.assertEqual(errors, expected_errors)

    def test_delete_table_success(self):
        self.mock_client.delete_table.return_value = None
        result = delete_table(self.mock_client, "dataset", "table")
        self.assertTrue(result)

    def test_delete_table_error(self):
        self.mock_client.delete_table.side_effect = Exception("Error")
        result = delete_table(self.mock_client, "dataset", "table")
        self.assertFalse(result)

    def test_get_data(self):
        mock_query_job = MagicMock()
        mock_row = MagicMock()
        mock_row.items.return_value = [("col1", "val1")]
        mock_query_job.result.return_value = [mock_row]
        self.mock_client.query.return_value = mock_query_job

        rows = get_data(self.mock_client, "dataset", "table", where_clauses={"id": 1})

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["col1"], "val1")
        args, _ = self.mock_client.query.call_args
        self.assertIn("WHERE `id` = 1", args[0])

    def test_run_select_query_list(self):
        mock_query_job = MagicMock()
        mock_row = MagicMock()
        mock_row.items.return_value = [("colA", 100)]
        mock_query_job.result.return_value = [mock_row]
        self.mock_client.query.return_value = mock_query_job

        result = run_select_query(self.mock_client, "SELECT * FROM table")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["colA"], 100)

    def test_run_select_query_dataframe(self):
        mock_query_job = MagicMock()
        mock_result = MagicMock()
        mock_result.to_dataframe.return_value = MagicMock(name="DataFrame")
        mock_query_job.result.return_value = mock_result
        self.mock_client.query.return_value = mock_query_job

        result = run_select_query(
            self.mock_client, "SELECT * FROM table", output_format="dataframe"
        )
        mock_result.to_dataframe.assert_called_once()

    def test_run_select_query_invalid(self):
        with self.assertRaises(ValueError):
            run_select_query(self.mock_client, "UPDATE table SET x=1")


if __name__ == "__main__":
    unittest.main()