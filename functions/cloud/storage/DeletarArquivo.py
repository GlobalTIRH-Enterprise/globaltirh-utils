from google.cloud import storage
from utils.CreateLogger import log
from GetBucket import get_bucket


def deletar_arquivo(
    client: storage.Client,
    bucket_name: str,
    nome_arquivo: str
) -> bool:
    """
    Exclui um arquivo do bucket.

    Args:
        client: Cliente autenticado do Google Cloud Storage.
        bucket_name: Nome do bucket.
        nome_arquivo: Nome do blob a ser excluído.

    Returns:
        True se a exclusão for bem-sucedida.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        Exception: Para outros erros da API.
    """
    bucket = get_bucket(client, bucket_name)
    blob = bucket.blob(nome_arquivo)
    if not blob.exists():
        raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado no bucket '{bucket_name}'")
    blob.delete()
    log.info(f"Arquivo '{nome_arquivo}' excluído de gs://{bucket_name}/{nome_arquivo}")
    return True