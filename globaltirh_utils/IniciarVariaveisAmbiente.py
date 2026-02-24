import logging
import os
import re
import sys
from typing import Optional
from dotenv import find_dotenv, load_dotenv

# Configuração do Logger
log = logging.getLogger("inicializar_variaveis_de_ambiente")
log.setLevel(logging.INFO)

if not log.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.propagate = False

ENV_PATTERN = re.compile(r"(\w+)\s*=\s*'([^']+)'?")


def inicializar_variaveis_de_ambiente(possible_locations: Optional[list[str]] = None) -> bool:
    """
    Inicializa as variáveis de ambiente a partir de arquivos .env ou da variável 'envs_texts'.

    O algoritmo realiza os seguintes passos:
    1. Busca por arquivos .env em uma lista de caminhos predefinidos ou fornecidos.
    2. Se encontrar e o arquivo contiver dados válidos, as variáveis são carregadas no ambiente.
    3. Caso o arquivo .env não seja encontrado ou esteja vazio, tenta extrair as variáveis
        de uma string formatada contida na variável de ambiente 'envs_texts'.

    Args:
        possible_locations (list[str] | None, opcional): Lista de caminhos para buscar o arquivo .env.
            Se None for passado, utiliza uma lista padrão de diretórios. Padrão é None.

    Returns:
        bool: Retorna True se as variáveis foram carregadas com sucesso (seja pelo .env ou
            pela variável 'envs_texts'), e False caso contrário.
    """
    log.debug("Iniciando a inicialização de variáveis de ambiente")

    if possible_locations is None:
        possible_locations = [
            r".env",
            r"/secrets/.env",
            r"secrets/.env",
            r"/credenciais/.env",
            r"credenciais/.env",
        ]

    # 1. Tenta encontrar e carregar a partir de um arquivo .env
    for caminho in possible_locations:
        if find_dotenv(caminho):
            log.debug(f"Arquivo .env encontrado no caminho: {caminho}")

            if load_dotenv(caminho):
                log.info("Variáveis do arquivo .env carregadas com sucesso!")
                return True

            log.debug(f"Arquivo .env em {caminho} foi encontrado, mas está vazio ou inválido.")

    log.info("Não foi possível carregar via .env. Tentando utilizar a variável 'envs_texts'.")

    # 2. Fallback: tenta carregar a partir da variável de ambiente 'envs_texts'
    envs_text = os.getenv("envs_texts")

    if envs_text and isinstance(envs_text, str):
        log.debug("Extraindo variáveis da string 'envs_texts'")
        pares = ENV_PATTERN.findall(envs_text)

        if pares:
            for chave, valor in pares:
                os.environ[chave] = valor
                log.debug(f"Variável de ambiente definida via texto: {chave}='***'")

            log.info("Variáveis de ambiente carregadas com sucesso através de 'envs_texts'.")
            return True

    log.info("Nenhuma variável de ambiente foi carregada.")
    return False
