from typing import Any

__all__ = ["log", "recreate_logger", "inicializar_variaveis_de_ambiente"]


def __getattr__(name: str) -> Any:
    if name in ("log", "recreate_logger"):
        from .CreateLogger import log, recreate_logger

        if name == "log":
            return log
        return recreate_logger
    elif name == "inicializar_variaveis_de_ambiente":
        from .IniciarVariaveisAmbiente import inicializar_variaveis_de_ambiente

        return inicializar_variaveis_de_ambiente
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    return sorted(__all__)
