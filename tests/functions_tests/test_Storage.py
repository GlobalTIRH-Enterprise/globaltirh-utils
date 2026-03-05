import unittest
from unittest.mock import MagicMock, patch

from functions_global.cloud.storage import (
    upload_file_to_gcs,
    listar_conteudo,
    deletar_arquivo,
    download_arquivo,
    obter_metadados,
    valida_existencia_do_arquivo,
    get_bucket,
)


class TestStorageFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock()
        self.bucket_name = "default-bucket"
        self.mock_bucket = MagicMock()
        self.mock_client.bucket.return_value = self.mock_bucket

    def test_get_bucket(self):
        bucket = get_bucket(self.mock_client, self.bucket_name)
        self.mock_client.bucket.assert_called_with(self.bucket_name)
        self.assertEqual(bucket, self.mock_bucket)

    def test_get_bucket_raises_if_empty(self):
        with self.assertRaises(ValueError):
            get_bucket(self.mock_client, "")

    @patch("functions.storage.storage_functions.path.join")
    def test_upload_file_to_gcs_success(self, mock_path_join):
        mock_path_join.return_value = "/tmp/file.txt"
        mock_blob = MagicMock()
        self.mock_bucket.blob.return_value = mock_blob
        self.mock_bucket.name = self.bucket_name

        uri = upload_file_to_gcs(
            client=self.mock_client,
            bucket_name=self.bucket_name,
            filename="file.txt",
            destination_blob_name="folder/file.txt",
        )

        mock_blob.upload_from_filename.assert_called_with("/tmp/file.txt")
        self.assertEqual(uri, f"gs://{self.bucket_name}/folder/file.txt")

    def test_upload_file_to_gcs_error(self):
        self.mock_client.bucket.side_effect = Exception("Access Denied")

        uri = upload_file_to_gcs(
            client=self.mock_client,
            bucket_name=self.bucket_name,
            filename="file.txt",
            destination_blob_name="dest",
        )
        self.assertEqual(uri, "")

    def test_listar_conteudo(self):
        mock_blob = MagicMock()
        mock_blob.name = "file1.txt"
        mock_blob.size = 1024
        mock_blob.content_type = "text/plain"
        mock_blob.updated.isoformat.return_value = "2023-01-01"
        self.mock_bucket.list_blobs.return_value = [mock_blob]

        lista = listar_conteudo(
            client=self.mock_client,
            bucket_name=self.bucket_name,
        )

        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["nome"], "file1.txt")

    def test_deletar_arquivo_success(self):
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        self.mock_bucket.blob.return_value = mock_blob

        result = deletar_arquivo(
            client=self.mock_client,
            bucket_name=self.bucket_name,
            nome_arquivo="file.txt",
        )
        self.assertTrue(result)
        mock_blob.delete.assert_called_once()

    def test_deletar_arquivo_not_found(self):
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False
        self.mock_bucket.blob.return_value = mock_blob

        with self.assertRaises(FileNotFoundError):
            deletar_arquivo(
                client=self.mock_client,
                bucket_name=self.bucket_name,
                nome_arquivo="file.txt",
            )

    @patch("functions.storage.storage_functions.tempfile.NamedTemporaryFile")
    def test_download_arquivo(self, mock_tempfile):
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        self.mock_bucket.blob.return_value = mock_blob

        mock_temp_obj = MagicMock()
        mock_temp_obj.name = "/tmp/tempfile"
        mock_tempfile.return_value = mock_temp_obj

        path = download_arquivo(
            client=self.mock_client,
            bucket_name=self.bucket_name,
            nome_arquivo="file.txt",
        )

        self.assertEqual(path, "/tmp/tempfile")
        mock_blob.download_to_filename.assert_called_with("/tmp/tempfile")

if __name__ == "__main__":
    unittest.main()