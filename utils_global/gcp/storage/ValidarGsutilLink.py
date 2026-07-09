from typing import Set, Optional
from os.path import splitext
from utils_global.validation.VerificaTipo import deco_verifica_tipo


@deco_verifica_tipo
def validar_gsutil_link(
    link: str, quant_parts: int = 4, tipos_verificar: Optional[Set[str]] = None
) -> None:
    """
    Valida um link no formato gsutil, verificando se ele segue o padrão esperado.

    Args:
        link: O link gsutil a ser validado (ex: "gs://bucket/path/to/file.txt").
        quant_parts:
            O número esperado de partes no caminho do link após o prefixo "gs://".
            Por padrão, espera-se 4 partes (bucket, categoria, uuid, filename).
        tipos_verificar:
            Um conjunto de extensões de arquivo aceitáveis (ex: {".pdf", ".png"}).
            Se fornecido, o link será validado para ter uma dessas extensões.
            Se None ou vazio, a extensão do arquivo não será verificada.

    Returns:
        None se o link for válido.

    Raises:
        ValueError: Se o link não possuir o prefixo 'gs://', tiver um número
            incorreto de partes ou uma extensão não permitida.
    """

    if not link.startswith("gs://"):
        raise ValueError(f"Link '{link}' não está no formato gsutil!")

    partes = link[5:].split("/")
    if len(partes) != quant_parts:
        raise ValueError(
            f"Link '{link}' está faltando informações! Esperado {quant_parts} "
            f"partes após 'gs://', encontrado {len(partes)}."
        )

    # Verifica se tipos_verificar foi fornecido e não está vazio
    if tipos_verificar:
        extensao = splitext(link)[1]
        if extensao not in tipos_verificar:
            raise ValueError(
                f"Link '{link}' tem a extensão '{extensao}', e só são aceitas as: '{tipos_verificar}'"
            )

    return None
