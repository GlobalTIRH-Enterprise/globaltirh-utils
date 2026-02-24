import mimetypes
from typing import Optional

from .VerificaTipo import deco_verifica_tipo

_TEXT_EXTENSIONS = (".txt", ".md", ".csv", ".log")


@deco_verifica_tipo
def guess_mimetype(path: str) -> Optional[str]:
    """
    Infere o tipo MIME (MIME type) de um arquivo com base no seu caminho ou nome.

    Utiliza a biblioteca padrão `mimetypes` como método primário. Caso o ambiente
    (ex: containers Docker muito enxutos ou OS com registros ausentes) não consiga
    identificar, aplica regras de fallback para extensões comuns (PDF e textos).

    Args:
        path (str): O caminho completo do arquivo ou apenas o seu nome.

    Returns:
        Optional[str]: Uma string representando o tipo MIME (ex: 'application/pdf',
            'text/plain') ou None se o tipo não puder ser inferido.
    """
    # 1. Tenta inferir o tipo usando a biblioteca nativa do Python
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type:
        return mime_type

    # Converte para minúsculas para garantir que .PDF ou .TXT sejam capturados
    path_lower = path.lower()

    # 2. Fallback para PDF
    if path_lower.endswith(".pdf"):
        return "application/pdf"

    # 3. Fallback para arquivos de texto variados
    if path_lower.endswith(_TEXT_EXTENSIONS):
        return "text/plain"

    # 4. Retorna None para deixar o SDK ou a camada superior decidir a ação
    return None
