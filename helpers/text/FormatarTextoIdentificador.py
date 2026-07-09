import re
import unicodedata
from helpers.validation.VerificaTipo import deco_verifica_tipo


@deco_verifica_tipo
def formatar_texto_para_identificador(text: str) -> str:
    """
    Formata uma string para ser usada como um identificador seguro,
    realizando as seguintes operações:
    - Remove acentos (ex: 'ç' -> 'c', 'á' -> 'a').
    - Substitui um ou mais espaços em branco por um único underscore.
    - Remove as seguintes pontuações: ',', ';', '.', '\', '/'.
    - Garante que não haja múltiplos underscores em sequência.

    Args:
        text (str): O texto a ser formatado.

    Returns:
        str: O texto formatado como um identificador.
    """
    # Remove acentos
    text = "".join(
        c for c in unicodedata.normalize("NFKD", text) if unicodedata.category(c) != "Mn"
    )

    # Substitui espaços por underscores
    text = re.sub(r"\s+", "_", text).strip()

    # Garante que não haja underscores duplicados
    text = re.sub(r"_+", "_", text)

    # Remove pontuações específicas
    pontuacao_remover = r"[,;.\\/]"
    text = re.sub(pontuacao_remover, "", text)

    return text.lower()
