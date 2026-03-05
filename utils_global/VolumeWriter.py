import json
import os
from pathlib import Path
from typing import Any

def volume_write(nome_arquivo: str, content: Any, on_server: bool, mounted_volume_name: str, mounted_volume_read_only:str) -> None:
    """
    Salva conteúdo em um arquivo no volume, agnóstico à extensão.
    O nome do arquivo deve incluir a extensão (ex: 'dados.json', 'log.txt').
    Se a extensão for .json e o conteúdo for dict/list, salva como JSON.
    Caso contrário, tenta salvar como string ou bytes.
    """
    
    file_path = Path(nome_arquivo)
    nome_final = file_path.name # Usa o nome completo com extensão

    if on_server:
        if mounted_volume_read_only:
            raise PermissionError("Volume configurado como apenas leitura!")
        
        # No servidor: /volume_name/
        base_path = Path("/") / mounted_volume_name
    else:
        # Localmente: ./data/volume_name/
        base_path = Path.cwd() / "data" / mounted_volume_name

    try:
        # Cria a árvore de diretórios se não existir
        base_path.mkdir(parents=True, exist_ok=True)
        
        caminho_completo = base_path / nome_final

        # Lógica de salvamento baseada na extensão
        suffix = file_path.suffix.lower()

        if suffix == '.json':
            if isinstance(content, (dict, list)):
                with open(caminho_completo, "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=4, ensure_ascii=False)
            else:
                 # Se for string mas extensão json, salva string
                with open(caminho_completo, "w", encoding="utf-8") as f:
                    f.write(str(content))
        else:
            # Outras extensões (txt, log, etc)
            mode = "wb" if isinstance(content, bytes) else "w"
            encoding = None if isinstance(content, bytes) else "utf-8"
            
            with open(caminho_completo, mode, encoding=encoding) as f:
                f.write(content)
            
    except Exception as e:
        raise IOError(f"Falha crítica ao salvar {nome_final} em {base_path}: {e}")
