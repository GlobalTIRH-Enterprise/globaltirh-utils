from typing import Any, Callable, get_origin, get_args
from functools import wraps
import inspect


def verifica_tipo(params: list[tuple[Any, Any, str]]) -> None:
    """
    Verifica se os valores fornecidos correspondem aos tipos esperados.

    Args:
        params: Lista de tuplas contendo (valor, tipo_esperado, nome_parametro).

    Raises:
        TypeError: Se um ou mais valores não corresponderem aos seus respectivos tipos.
    """
    _check_params(params)


def deco_verifica_tipo(fn: Callable) -> Callable:
    """
    Decorator que verifica automaticamente os tipos dos argumentos passados para a função
    com base nas anotações de tipo (type hints).

    Args:
        fn: A função a ser decorada.

    Returns:
        A função decorada com verificação de tipos.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(fn)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        checks = []
        for param_name, value in bound.arguments.items():
            param = sig.parameters[param_name]
            annotation = param.annotation

            if annotation is not inspect.Parameter.empty and annotation is not Any:
                checks.append((value, annotation, param_name))

        if checks:
            _check_params(checks)

        return fn(*args, **kwargs)

    return wrapper


def _check_params(params: list[tuple[Any, Any, str]]) -> None:
    errors: list[str] = []

    for value, expected_type, param_name in params:
        # Tenta usar isinstance diretamente (funciona para tipos simples e Unions no Python recente)
        try:
            is_valid = isinstance(value, expected_type)
        except TypeError:
            # Se falhar (ex: list[str] lança TypeError), tenta usar o tipo base (list)
            origin = get_origin(expected_type)
            if origin is not None:
                is_valid = isinstance(value, origin)
            else:
                # Se não for possível validar, assume válido para não quebrar execução
                # Ou poderia logar um aviso. Aqui optamos por ignorar validação complexa.
                is_valid = True

        if not is_valid:
            # Format types properly for the error message
            if isinstance(expected_type, tuple):
                expected_type_name = " ou ".join(
                    [getattr(t, "__name__", str(t)) for t in expected_type]
                )
            else:
                expected_type_name = getattr(expected_type, "__name__", str(expected_type))

            actual_type_name = type(value).__name__

            errors.append(
                f"Parâmetro '{param_name}' deveria ser do tipo '{expected_type_name}', "
                f"ao invés disso encontrou: '{actual_type_name}'."
            )

    if errors:
        # Join multiple errors with a newline for clear reading
        raise TypeError("\n".join(errors))
