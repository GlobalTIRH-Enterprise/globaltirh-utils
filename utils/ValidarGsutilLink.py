from typing import Set, Optional
from os.path import splitext


def validar_gsutil_link(
    link: str, quant_parts: int = 4, tipos_verificar: Optional[Set[str]] = None
) -> Optional[str]:
    """
    Valida um link no formato gsutil, verificando se ele segue o padrão esperado.

    Args:
        link: O link gsutil a ser validado (ex: "gs://bucket/path/to/file.txt").
        quant_parts: 
            O número esperado de partes no caminho do link após o prefixo "gs://".
            Por padrão, espera-se 3 partes (bucket, categoria, uuid, filename).
        tipos_verificar: 
        Um conjunto de extensões de arquivo aceitáveis (ex: {".pdf", ".png"}).
            Se fornecido, o link será validado para ter uma dessas extensões.
            Se None ou vazio, a extensão do arquivo não será verificada.

    Returns:
        None se o link for válido.
        Uma string contendo uma mensagem de erro se o link for inválido.
    """

    if not link.startswith("gs://"):
        return f"Link '{link}' não está no formato gsutil!"

    partes = link[5:].split("/")
    if len(partes) != quant_parts:
        return f"Link '{link}' está faltando informações! Esperado {quant_parts} partes após 'gs://', encontrado {len(partes)}."

    # Verifica se tipos_verificar foi fornecido e não está vazio
    if tipos_verificar and len(tipos_verificar) > 0:
        extensao = splitext(link)[1]
        if extensao not in tipos_verificar:
            return f"Link '{link}' tem a extensão '{extensao}', e só são aceitas as: '{tipos_verificar}'"

    return None
