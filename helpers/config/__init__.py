"""
Subpacote de configuração com suporte a lazy-loading (carregamento sob demanda).

O bloco 'if TYPE_CHECKING' é utilizado para guiar analisadores estáticos de tipo (como o Pylance/IDE).
Isso foi feito especificamente para permitir que 'inicializar_variaveis_de_ambiente' seja importada
e executada de forma completamente limpa antes de carregar e instanciar o logger global 'log'.
"""
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .CreateLogger import log, recreate_logger
    from .IniciarVariaveisAmbiente import inicializar_variaveis_de_ambiente

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
