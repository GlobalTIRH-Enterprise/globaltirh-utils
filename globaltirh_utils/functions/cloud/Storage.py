from google.cloud import storage
import tempfile
from globaltirh_utils.CreateLogger import log

from typing import List
from os import getenv, path


class StorageManager:
    def __init__(self, bucket_name: str | None = None):
        try:
            self.client = storage.Client()

        except Exception as e:
            log.error(f"Erro ao inicializar StorageManager: {e}")
            raise
        self.bucket_name = bucket_name

    def get_bucket(self, bucket_name: str):
        target_bucket = bucket_name or self.bucket_name
        if not target_bucket:
            raise ValueError("Bucket name não fornecido.")
        return self.client.bucket(target_bucket)

    def upload_file_to_gcs(
        self,
        filename: str,
        destination_blob_name: str,
        bucket_name: str | None = None,
        temporary_folder: str | None = None,
    ) -> str:
        """
        Função para fazer upload de um arquivo para o Google Cloud Storage (GCS).

        Args:
            filename (str): O nome do arquivo a ser enviado.
            destination_blob_name (str): O nome que o arquivo terá no GCS (caminho dentro do bucket).
            bucket_name (str): O nome do bucket do GCS onde o arquivo será armazenado.
            temporary_folder (str): O caminho da pasta temporária onde o arquivo está localizado localmente. Se None, usa o temp do sistema.

        Returns:
            str: O URI do arquivo no GCS (gs://bucket/caminho) se o upload for bem-sucedido, caso contrário, retorna "".
        """
        if temporary_folder is None:
            temporary_folder = tempfile.gettempdir()

        source_file_path = path.join(temporary_folder, filename)
        destination_blob_name = destination_blob_name.replace("\\", "/")

        try:
            if bucket_name is None:
                if self.bucket_name is None:
                    raise Exception("No bucket name")
                bucket_name = self.bucket_name
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_path)
            gcs_uri = f"gs://{bucket.name}/{destination_blob_name}"

            log.info(f"File '{filename}' uploaded to {gcs_uri}")
            return gcs_uri

        except Exception as e:
            log.error(f"Error uploading '{filename}' to GCS: {type(e).__name__} - {e}")
            return ""

    def listar_conteudo(
        self, bucket_name: str | None = None, prefixo: str | None = None
    ) -> List[dict]:
        """
        Lista arquivos do bucket (opcionalmente por prefixo).
        """
        try:
            if bucket_name is None:
                if self.bucket_name is None:
                    raise Exception("No bucket name")
                bucket_name = self.bucket_name

            bucket = self.get_bucket(bucket_name)

            blobs = bucket.list_blobs(prefix=prefixo)

            arquivos = [
                {
                    "nome": blob.name,
                    "tamanho_bytes": blob.size,
                    "mime_type": blob.content_type,
                    "ultima_modificacao": blob.updated.isoformat() if blob.updated else None,
                }
                for blob in blobs
                if blob.size
            ]

            log.info(f"{len(arquivos)} arquivos encontrados (prefixo={prefixo})")
            return arquivos

        except Exception as e:
            log.error(f"Erro ao listar conteúdo do bucket: {e}")
            return []

    def deletar_arquivo(self, nome_arquivo: str, bucket_name: str | None = None):
        if bucket_name is None:
            if self.bucket_name is None:
                raise Exception("No bucket name")
            bucket_name = self.bucket_name
        bucket = self.get_bucket(bucket_name)

        blob = bucket.blob(nome_arquivo)

        if not blob.exists():
            raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado")

        blob.delete()

        return True

    def download_arquivo(self, nome_arquivo: str, bucket_name: str | None = None) -> str:
        """
        Faz download de um arquivo do bucket para um temp local e retorna o path local.
        """

        if bucket_name is None:
            if self.bucket_name is None:
                raise Exception("No bucket name")
            bucket_name = self.bucket_name

        bucket = self.get_bucket(bucket_name)

        blob = bucket.blob(nome_arquivo)

        if not blob.exists():
            raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado")

        temp_file = tempfile.NamedTemporaryFile(delete=False)

        blob.download_to_filename(temp_file.name)
        temp_file.close()

        return temp_file.name

    def obter_metadados(self, nome_arquivo: str, bucket_name: str | None = None) -> dict:
        """
        Retorna metadados simples de um arquivo no bucket.
        """

        if bucket_name is None:
            if self.bucket_name is None:
                raise Exception("No bucket name")
            bucket_name = self.bucket_name

        bucket = self.get_bucket(bucket_name)

        blob = bucket.blob(nome_arquivo)

        if not blob.exists():
            raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado")

        return {
            "nome": blob.name,
            "tamanho": blob.size,
            "content_type": blob.content_type,
            "atualizado_em": blob.updated.isoformat() if blob.updated else None,
            "bucket": bucket.name,
        }

    def valida_existencia_do_arquivo(
        self, nome_arquivo: str, bucket_name: str | None = None
    ) -> storage.Blob:

        if bucket_name is None:
            if self.bucket_name is None:
                raise Exception("No bucket name")
            bucket_name = self.bucket_name

        bucket = self.get_bucket(bucket_name)

        blob = bucket.blob(nome_arquivo)

        if not blob.exists():
            raise LookupError("Referência do arquivo não encontrada!")

        return blob
