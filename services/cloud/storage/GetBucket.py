from google.cloud import storage

def get_bucket(client: storage.Client, bucket_name: str) -> storage.Bucket:
    """Obtém um bucket do Google Cloud Storage.

    Args:
        client: Cliente autenticado do Google Cloud Storage.
        bucket_name: Nome do bucket.

    Returns:
        Objeto Bucket referente ao nome fornecido.

    Raises:
        ValueError: Se o bucket_name for None ou vazio.
    """
    if not bucket_name:
        raise ValueError("Bucket name não fornecido.")
    return client.bucket(bucket_name)