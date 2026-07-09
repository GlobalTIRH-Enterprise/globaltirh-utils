from google.cloud import storage
from .GetBucket import get_bucket


def valida_existencia_do_arquivo(
    client: storage.Client,
    bucket_name: str,
    nome_arquivo: str
) -> storage.Blob:
    """
    Verifica se um arquivo existe no bucket e retorna o objeto Blob.

    Args:
        client: Cliente autenticado do Google Cloud Storage.
        bucket_name: Nome do bucket.
        nome_arquivo: Nome do blob.

    Returns:
        O objeto Blob referente ao arquivo.

    Raises:
        LookupError: Se o arquivo não existir.
    """
    bucket = get_bucket(client, bucket_name)
    blob = bucket.blob(nome_arquivo)
    if not blob.exists():
        raise LookupError(f"Arquivo '{nome_arquivo}' não encontrado no bucket '{bucket_name}'")
    return blob