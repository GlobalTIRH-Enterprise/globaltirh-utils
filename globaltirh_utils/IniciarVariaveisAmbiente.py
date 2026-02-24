from os import environ, getenv
import re
from dotenv import load_dotenv, find_dotenv
import logging
import sys

log = logging.getLogger("inicializar_variaveis_de_ambiente")
logging_level = logging.INFO

log.setLevel(logging_level)

if not log.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging_level)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    )
    log.addHandler(handler)
    log.propagate = False


def inicializar_variaveis_de_ambiente() -> bool:
    """
    Inicializa as variáveis de ambiente a partir de arquivos .env ou da variável 'envs_texts'.

    Busca por arquivos .env em locais predefinidos. Caso não encontre, tenta extrair
    as variáveis de uma string formatada na variável de ambiente 'envs_texts'.

    Returns:
        bool: True se as variáveis foram carregadas com sucesso, False caso contrário.
    """
    log.debug("Iniciando inicializacao de variaveis de ambiente")
    possible_locations = (
        r".env",
        r"/secrets/.env",
        r"secrets/.env",
        r"/credenciais/.env",
        r"credenciais/.env",
    )

    for l in possible_locations:
        if find_dotenv(l):
            log.debug(".ENV encontrada!")
            log.debug("Lendo .ENV")
            if load_dotenv(l):
                log.info(".ENV Lido!")
                return True
            log.debug(".ENV sem conteúdo setado")
            return False
    log.info("Não foi possível achar o .ENV! Tentando utilizar o 'envs_texts'")

    if envs_text := getenv("envs_texts"):
        log.debug("Carregando variáveis de ambiente da variável 'envs_texts'")
        if isinstance(envs_text, str):
            mudou_algo = False
            pairs = re.findall(r"(\w+)\s*=\s*'([^']+)", envs_text)
            for k, v in pairs:
                environ[k] = v
                log.debug(f"Variável de ambiente definida: {k}='{v}'")
                mudou_algo = True

            if mudou_algo:
                log.info("Carregado env do 'envs_texts'.")
                return True

    log.info("Nenhuma variável de ambiente carregada.")
    return False
