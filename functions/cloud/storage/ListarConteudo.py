from google.cloud import storage
from utils import log
from typing import List, Optional
from .GetBucket import get_bucket


def listar_conteudo(
    client: storage.Client,
    bucket_name: str,
    prefixo: Optional[str] = None
) -> List[dict]:
    """
    Lista arquivos de um bucket do GCS, opcionalmente filtrando por prefixo.

    Args:
        client: Cliente autenticado do Google Cloud Storage.
        bucket_name: Nome do bucket.
        prefixo: Prefixo para filtrar os objetos (ex.: pasta/).

    Returns:
        Lista de dicionários com informações de cada arquivo (nome, tamanho, tipo, última modificação).
    """
    try:
        bucket = get_bucket(client, bucket_name)
        blobs = bucket.list_blobs(prefix=prefixo)
        arquivos = []
        for blob in blobs:
            if blob.size is not None:
                arquivos.append({
                    "nome": blob.name,
                    "tamanho_bytes": blob.size,
                    "mime_type": blob.content_type,
                    "ultima_modificacao": blob.updated.isoformat() if blob.updated else None,
                })
        log.info(f"{len(arquivos)} arquivos encontrados (prefixo={prefixo})")
        return arquivos
    except Exception as e:
        log.error(f"Erro ao listar conteúdo do bucket: {e}")
        return []