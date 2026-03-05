from google.cloud import storage
import tempfile
from utils.CreateLogger import log
from typing import Optional
from os import path
from GetBucket import get_bucket


def upload_file_to_gcs(
    client: storage.Client,
    bucket_name: str,
    filename: str,
    destination_blob_name: str,
    temporary_folder: Optional[str] = None
) -> str:
    """
    Faz upload de um arquivo para o Google Cloud Storage (GCS).

    Args:
        client: Cliente autenticado do Google Cloud Storage.
        bucket_name: Nome do bucket de destino.
        filename: Nome do arquivo local a ser enviado.
        destination_blob_name: Caminho/nome do blob no bucket.
        temporary_folder: Pasta onde o arquivo local está localizado. Se None, usa diretório temporário do sistema.

    Returns:
        URI do arquivo no GCS (gs://bucket/caminho) em caso de sucesso, ou string vazia em caso de erro.
    """
    if temporary_folder is None:
        temporary_folder = tempfile.gettempdir()
    source_file_path = path.join(temporary_folder, filename)
    dest_blob = destination_blob_name.replace("\\", "/")

    try:
        bucket = get_bucket(client, bucket_name)
        blob = bucket.blob(dest_blob)
        blob.upload_from_filename(source_file_path)
        gcs_uri = f"gs://{bucket.name}/{dest_blob}"
        log.info(f"Arquivo '{filename}' enviado para {gcs_uri}")
        return gcs_uri
    except Exception as e:
        log.error(f"Erro ao enviar '{filename}' para GCS: {type(e).__name__} - {e}")
        return ""