from typing import Any


def verifica_tipo(params: list[tuple[Any, type | tuple, str]]) -> None:
    """
    Verifica se os valores fornecidos correspondem aos tipos esperados.

    Args:
        params (list[tuple[Any, type | tuple, str]]): Uma lista de tuplas.
            Cada tupla deve conter:
            1. O valor da variável a ser testada.
            2. O tipo esperado (ex: str) ou múltiplos tipos esperados (ex: (int, float)).
            3. O nome da variável (usado na mensagem de erro).

    Raises:
        TypeError: Se um ou mais valores não corresponderem aos seus respectivos tipos.

    Example:
        >>> verifica_tipo([
        ...     (10, int, "idade"),
        ...     ("Maria", str, "nome")
        ... ])
    """
    errors: list[str] = []

    for value, expected_type, param_name in params:
        if not isinstance(value, expected_type):
            # Format types properly for the error message
            if isinstance(expected_type, tuple):
                expected_type_name = " ou ".join([t.__name__ for t in expected_type])
            else:
                expected_type_name = expected_type.__name__

            actual_type_name = type(value).__name__

            errors.append(
                f"Parâmetro '{param_name}' deveria ser do tipo '{expected_type_name}', "
                f"ao invés disso encontrou: '{actual_type_name}'."
            )

    if errors:
        # Join multiple errors with a newline for clear reading
        raise TypeError("\n".join(errors))
