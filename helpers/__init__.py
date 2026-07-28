from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .config import log, recreate_logger, inicializar_variaveis_de_ambiente
    from .datetime import tempo_to_brasilia
    from .gcp import (
        generate_access_token,
        salvar_credenciais,
        check_content_is_valid,
        validar_gsutil_link,
    )
    from .io import guess_mimetype, volume_read, volume_write
    from .text import (
        formatar_texto_para_identificador,
        get_dict_from_text,
        processa_une_strings,
        string_to_bool,
    )
    from .validation import verifica_tipo, deco_verifica_tipo

__all__ = [
    "log",
    "inicializar_variaveis_de_ambiente",
    "recreate_logger",
    "tempo_to_brasilia",
    "generate_access_token",
    "salvar_credenciais",
    "check_content_is_valid",
    "validar_gsutil_link",
    "guess_mimetype",
    "volume_read",
    "volume_write",
    "formatar_texto_para_identificador",
    "get_dict_from_text",
    "processa_une_strings",
    "string_to_bool",
    "verifica_tipo",
    "deco_verifica_tipo",
]


def __getattr__(name: str) -> Any:
    if name in ("log", "recreate_logger"):
        from .config import log, recreate_logger

        if name == "log":
            return log
        return recreate_logger

    elif name == "inicializar_variaveis_de_ambiente":
        from .config import inicializar_variaveis_de_ambiente

        return inicializar_variaveis_de_ambiente

    elif name == "tempo_to_brasilia":
        from .datetime import tempo_to_brasilia

        return tempo_to_brasilia

    elif name in (
        "generate_access_token",
        "salvar_credenciais",
        "check_content_is_valid",
        "validar_gsutil_link",
    ):
        from .gcp import (
            generate_access_token,
            salvar_credenciais,
            check_content_is_valid,
            validar_gsutil_link,
        )

        if name == "generate_access_token":
            return generate_access_token
        elif name == "salvar_credenciais":
            return salvar_credenciais
        elif name == "check_content_is_valid":
            return check_content_is_valid
        return validar_gsutil_link

    elif name in ("guess_mimetype", "volume_read", "volume_write"):
        from .io import guess_mimetype, volume_read, volume_write

        if name == "guess_mimetype":
            return guess_mimetype
        elif name == "volume_read":
            return volume_read
        return volume_write

    elif name in (
        "formatar_texto_para_identificador",
        "get_dict_from_text",
        "processa_une_strings",
        "string_to_bool",
    ):
        from .text import (
            formatar_texto_para_identificador,
            get_dict_from_text,
            processa_une_strings,
            string_to_bool,
        )

        if name == "formatar_texto_para_identificador":
            return formatar_texto_para_identificador
        elif name == "get_dict_from_text":
            return get_dict_from_text
        elif name == "processa_une_strings":
            return processa_une_strings
        return string_to_bool

    elif name in ("verifica_tipo", "deco_verifica_tipo"):
        from .validation import verifica_tipo, deco_verifica_tipo

        if name == "verifica_tipo":
            return verifica_tipo
        return deco_verifica_tipo

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    return sorted(__all__)
