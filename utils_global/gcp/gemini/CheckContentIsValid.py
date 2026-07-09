from utils_global.validation.VerificaTipo import deco_verifica_tipo


@deco_verifica_tipo
def check_content_is_valid(content: list) -> None:
    """
    Valida a estrutura de uma lista de conteúdos (geralmente usada para histórico de chat).

    Itera sobre os elementos da lista fornecida para garantir que cada um seja
    um dicionário devidamente formatado, contendo as chaves obrigatórias 'role'
    (com valores específicos) e 'parts' (sendo uma lista de objetos).

    Args:
        content (list): A lista de conteúdos anteriores a ser validada.

    Returns:
        None: Se a validação for bem-sucedida, a função não retorna nada.

    Raises:
        ValueError: Se a lista contiver elementos inválidos, estruturas ausentes
                    ou dados fora do padrão esperado.
    """
    for elem in content:
        if not isinstance(elem, dict):
            raise ValueError("Os elementos do conteúdo anterior não são objetos (dicionários)")

        if "role" not in elem or "parts" not in elem:
            raise ValueError(
                "A lista de conteúdos anteriores não contém as chaves necessárias 'role' e 'parts'"
            )

        if elem["role"] not in {"user", "model"}:
            raise ValueError("O valor de 'role' deve ser 'model' ou 'user'")

        parts = elem["parts"]
        if not isinstance(parts, list):
            raise ValueError("O campo 'parts' deve ser uma lista")

        for part in parts:
            if not isinstance(part, dict):
                raise ValueError("Cada elemento de 'parts' deve ser um objeto (dicionário)")

    return None
