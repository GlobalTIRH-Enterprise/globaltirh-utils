from typing import Any, Callable, get_origin, get_args, Union
from functools import wraps
import inspect
import types


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
        is_valid = False
        origin = get_origin(expected_type)

        # 1. Trata os tipos Union e Optional (incluindo sintaxe do Python 3.10+ com pipe '|')
        if origin is Union or (hasattr(types, "UnionType") and origin is types.UnionType):
            args = get_args(expected_type)
            # Verifica se o valor corresponde a algum dos argumentos da Union
            match_found = False
            for arg in args:
                # Se o argumento for NoneType (ou seja, parte de um Optional)
                if arg is type(None):
                    if value is None:
                        match_found = True
                        break
                    continue

                # Para outros tipos dentro da Union
                arg_origin = get_origin(arg) or arg
                try:
                    if isinstance(value, arg_origin):
                        match_found = True
                        break
                except TypeError:
                    continue

            if match_found:
                is_valid = True

        # 2. Comportamento original para os outros tipos
        else:
            try:
                is_valid = isinstance(value, expected_type)
            except TypeError:
                if origin is not None:
                    try:
                        is_valid = isinstance(value, origin)
                    except TypeError:
                        is_valid = True
                else:
                    is_valid = True

        if not is_valid:
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
        raise TypeError("\n".join(errors))
