import json
import os
from pathlib import Path
from typing import Any, Union


def volume_read(nome_arquivo: str, on_server: bool, mounted_volume_name: str) -> Union[dict, list, str, bytes, None]:
    """
    Lê conteúdo de um arquivo no volume, agnóstico à extensão.
    O nome do arquivo deve incluir a extensão (ex: 'dados.json').
    Retorna dict/list se for .json, str se for texto, bytes se binário, ou None se erro/vazio.
    """

    file_path = Path(nome_arquivo)
    nome_final = file_path.name

    if on_server:
        # No servidor: /volume_name/
        base_path = Path("/") / mounted_volume_name
    else:
        # Localmente: ./data/volume_name/
        base_path = Path.cwd() / "data" / mounted_volume_name

    caminho_completo = base_path / nome_final

    if not caminho_completo.exists():
        raise FileNotFoundError(f"Arquivo {nome_final} não encontrado em {base_path}")

    try:
        suffix = file_path.suffix.lower()

        if suffix == ".json":
            with open(caminho_completo, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Tenta ler como texto, fallback para bytes?
            # Melhor assumir texto por padrão, exceto se especificar binário?
            # Como a função é genérica, talvez retornar str por padrão.
            try:
                with open(caminho_completo, "r", encoding="utf-8") as f:
                    return f.read()
            except UnicodeDecodeError:
                with open(caminho_completo, "rb") as f:
                    return f.read()

    except Exception as e:
        raise IOError(f"Falha ao ler {nome_final}: {e}")