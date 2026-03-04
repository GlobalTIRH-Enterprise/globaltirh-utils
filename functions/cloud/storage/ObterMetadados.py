from google.cloud import storage
from GetBucket import get_bucket

def obter_metadados(
    client: storage.Client,
    bucket_name: str,
    nome_arquivo: str
) -> dict:
    """
    Retorna metadados de um arquivo no bucket.

    Args:
        client: Cliente autenticado do Google Cloud Storage.
        bucket_name: Nome do bucket.
        nome_arquivo: Nome do blob.

    Returns:
        Dicionário com metadados: nome, tamanho, content_type, atualizado_em, bucket.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        Exception: Para outros erros da API.
    """
    bucket = get_bucket(client, bucket_name)
    blob = bucket.blob(nome_arquivo)
    if not blob.exists():
        raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado no bucket '{bucket_name}'")
    return {
        "nome": blob.name,
        "tamanho": blob.size,
        "content_type": blob.content_type,
        "atualizado_em": blob.updated.isoformat() if blob.updated else None,
        "bucket": bucket.name,
    }