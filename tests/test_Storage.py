import unittest
from unittest.mock import MagicMock, patch
from utils_global.functions_global.cloud.Storage import StorageManager

class TestStorageManager(unittest.TestCase):

    @patch("utils_global.functions_global.cloud.Storage.storage.Client")
    def setUp(self, mock_client_cls):
        self.mock_client = mock_client_cls.return_value
        self.storage_manager = StorageManager(bucket_name="default-bucket")

    def test_get_bucket_default(self):
        self.storage_manager.get_bucket(None)
        self.mock_client.bucket.assert_called_with("default-bucket")

    def test_get_bucket_override(self):
        self.storage_manager.get_bucket("other-bucket")
        self.mock_client.bucket.assert_called_with("other-bucket")

    @patch("utils_global.functions_global.cloud.Storage.path.join")
    def test_upload_file_to_gcs_success(self, mock_path_join):
        mock_path_join.return_value = "/tmp/file.txt"
        
        mock_bucket = MagicMock()
        mock_bucket.name = "default-bucket"
        mock_blob = MagicMock()
        
        self.mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob

        uri = self.storage_manager.upload_file_to_gcs(
            filename="file.txt",
            destination_blob_name="folder/file.txt"
        )

        mock_blob.upload_from_filename.assert_called_with("/tmp/file.txt")
        self.assertEqual(uri, "gs://default-bucket/folder/file.txt")

    def test_upload_file_to_gcs_error(self):
        # Simula erro ao obter bucket
        self.mock_client.bucket.side_effect = Exception("Access Denied")
        
        uri = self.storage_manager.upload_file_to_gcs("file.txt", "dest")
        self.assertEqual(uri, "")

    def test_listar_conteudo(self):
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "file1.txt"
        mock_blob.size = 1024
        mock_blob.content_type = "text/plain"
        mock_blob.updated.isoformat.return_value = "2023-01-01"
        
        mock_bucket.list_blobs.return_value = [mock_blob]
        self.mock_client.bucket.return_value = mock_bucket

        lista = self.storage_manager.listar_conteudo()
        
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["nome"], "file1.txt")

    def test_deletar_arquivo_success(self):
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        
        mock_bucket.blob.return_value = mock_blob
        self.mock_client.bucket.return_value = mock_bucket

        result = self.storage_manager.deletar_arquivo("file.txt")
        self.assertTrue(result)
        mock_blob.delete.assert_called_once()

    def test_deletar_arquivo_not_found(self):
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False
        
        mock_bucket.blob.return_value = mock_blob
        self.mock_client.bucket.return_value = mock_bucket

        with self.assertRaises(FileNotFoundError):
            self.storage_manager.deletar_arquivo("file.txt")

    @patch("utils_global.functions_global.cloud.Storage.tempfile.NamedTemporaryFile")
    def test_download_arquivo(self, mock_tempfile):
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        
        mock_bucket.blob.return_value = mock_blob
        self.mock_client.bucket.return_value = mock_bucket

        # Configura o arquivo temporário mockado
        mock_temp_obj = MagicMock()
        mock_temp_obj.name = "/tmp/tempfile"
        mock_tempfile.return_value = mock_temp_obj

        path = self.storage_manager.download_arquivo("file.txt")
        
        self.assertEqual(path, "/tmp/tempfile")
        mock_blob.download_to_filename.assert_called_with("/tmp/tempfile")

if __name__ == "__main__":
    unittest.main()