from utils.validation.VerificaTipo import deco_verifica_tipo

# Utilizar frozenset fora da função evita a recriação da estrutura a cada chamada, otimizando a performance.
_VALORES_VERDADEIROS = frozenset({"1", "true", "t", "verdadeiro", "v"})
_VALORES_FALSOS = frozenset({"0", "false", "f", "falso"})


@deco_verifica_tipo
def string_to_bool(s: str | bool) -> bool:
    """
    Converte uma string ou valor booleano para um tipo estritamente booleano (True/False).

    A string de entrada é convertida para letras minúsculas e tem seus
    espaços em branco nas extremidades removidos antes da avaliação.

    Args:
        s (str | bool): O valor a ser convertido.

    Returns:
        bool:
            - True se a string for "1", "true", "t", "verdadeiro" ou "v" (ignorando maiúsculas/minúsculas).
            - False se a string for "0", "false", "f" ou "falso" (ignorando maiúsculas/minúsculas).
            - O próprio valor se `s` já for um booleano.

    Raises:
        ValueError: Se a string fornecida não corresponder a nenhum dos valores esperados.
        TypeError: Se o tipo do argumento passado não for `str` ou `bool`.
    """
    if isinstance(s, bool):
        return s

    if isinstance(s, str):
        s_formatada = s.strip().lower()

        if s_formatada in _VALORES_VERDADEIROS:
            return True
        if s_formatada in _VALORES_FALSOS:
            return False

        raise ValueError(f"String booleana inválida: '{s}'")

    # Prevenção extra caso o decorator não levante erro para tipos não esperados (int, float, etc.)
    raise TypeError(
        f"Tipo inválido para conversão: '{type(s).__name__}'. Esperado 'str' ou 'bool'."
    )
