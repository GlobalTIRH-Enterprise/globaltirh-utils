import tempfile
from google.cloud import storage
from utils_global.CreateLogger import log
from GetBucket import get_bucket

def download_arquivo(
    client: storage.Client,
    bucket_name: str,
    nome_arquivo: str
) -> str:
    """
    Faz download de um arquivo do bucket para um arquivo temporário local.

    Args:
        client: Cliente autenticado do Google Cloud Storage.
        bucket_name: Nome do bucket.
        nome_arquivo: Nome do blob a ser baixado.

    Returns:
        Caminho absoluto do arquivo temporário local.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        Exception: Para outros erros da API.
    """
    bucket = get_bucket(client, bucket_name)
    blob = bucket.blob(nome_arquivo)
    if not blob.exists():
        raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado no bucket '{bucket_name}'")
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    blob.download_to_filename(temp_file.name)
    temp_file.close()
    log.info(f"Arquivo '{nome_arquivo}' baixado para {temp_file.name}")
    return temp_file.name