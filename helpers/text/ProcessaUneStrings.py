from typing import List
from helpers.validation.VerificaTipo import deco_verifica_tipo


@deco_verifica_tipo
def processa_une_strings(string_list: List[str]) -> str:
    """
    Remove duplicatas de uma lista de strings com base em uma versão normalizada
    (letras minúsculas e sem espaços em branco) e retorna os itens originais
    únicos unidos em uma única string.

    A normalização ignora espaços (' '), quebras de linha ('\n'), tabulações ('\t')
    e diferenças entre maiúsculas e minúsculas para fins de comparação.

    Args:
        string_list (List[str]): Uma lista de strings a ser processada.

    Returns:
        str: Uma string contendo as strings originais que foram consideradas
        únicas, unidas por espaço e mantendo a ordem da primeira aparição.
    """
    seen_normalized = set()
    original_unique_strings = []

    for s in string_list:
        # "".join(s.split()) remove todos os tipos de espaços em branco de uma vez
        normalized_s = "".join(s.split()).lower()

        if normalized_s not in seen_normalized:
            seen_normalized.add(normalized_s)
            original_unique_strings.append(s)

    return " ".join(original_unique_strings)
