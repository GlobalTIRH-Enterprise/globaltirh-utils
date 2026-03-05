from os import environ, getenv
import json
from logging import getLogger
from pathlib import Path
from typing import Dict, Any


log = getLogger(getenv("LOGGER_NAME"))


# Constants
CREDENCIAL_KEYS = {
    "type": "CREDENCIAL_TYPE",
    "project_id": "CREDENCIAL_PROJECT_ID",
    "private_key_id": "CREDENCIAL_PRIVATE_KEY_ID",
    "private_key": "CREDENCIAL_PRIVATE_KEY",
    "client_email": "CREDENCIAL_CLIENT_EMAIL",
    "client_id": "CREDENCIAL_ID",
    "auth_uri": "CREDENCIAL_AUTH_URI",
    "token_uri": "CREDENCIAL_TOKEN_URIN",
    "auth_provider_x509_cert_url": "CREDENCIAL_AUTH_PROVIDER_X509_CERT_URL",
    "client_x509_cert_url": "CREDENCIAL_CLIENT_X509_CERT_URL",
    "universe_domain": "CREDENCIAL_UNIVERSE_DOMAIN",
}


def _deve_pular_setup(on_server: bool, usar_google_application_credentials: bool) -> bool:
    """Verifica se a criação do arquivo de credenciais deve ser ignorada."""
    if on_server:
        log.info(
            "ON_SERVER=TRUE -> Ambiente de servidor detectado. Pulando criação de arquivo de credencial local."
        )
        return True

    if not usar_google_application_credentials:
        log.info(
            "USAR GOOGLE APPLICATION CREDENTIALS = FALSE -> Configuração indica não utilizar credenciais via arquivo local (.ENV)."
        )
        return True

    if environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        log.info("GOOGLE_APPLICATION_CREDENTIALS já definida. Pulando criação.")
        return True

    return False


def _obter_dicionario_credenciais(salvar_dividido: bool) -> Dict[str, Any]:
    """Retorna o dicionário de credenciais a partir das variáveis de ambiente."""
    full_gcp_credencial = environ.get("FULL_GCP_CREDENTIAL")

    if full_gcp_credencial:
        # Cenário A: Credencial completa em uma única string JSON
        try:
            chave = json.loads(full_gcp_credencial)
        except json.JSONDecodeError as e:
            msg = f"Erro ao decodificar JSON da variável FULL_GCP_CREDENTIAL: {e}"
            log.exception(msg)
            raise ValueError(msg) from e

        # Retroalimenta as variáveis de ambiente individuais se solicitado
        if salvar_dividido:
            for json_key, env_var in CREDENCIAL_KEYS.items():
                if json_key in chave:
                    environ[env_var] = chave[json_key]
        return chave

    # Cenário B: Credencial montada via variáveis individuais
    chave: Dict[str, Any] = {}
    for json_key, env_var in CREDENCIAL_KEYS.items():
        value = environ.get(env_var)

        if not value:
            msg = f"Variável de ambiente obrigatória não encontrada: {json_key} ({env_var})"
            log.warning(msg)
            raise ValueError(msg)

        # Tratamento específico para quebras de linha em chaves RSA
        if json_key == "private_key":
            value = value.replace("\\n", "\n")

        chave[json_key] = value

    return chave


def _salvar_arquivo_json(dados: Dict[str, Any], temporary_folder: str, temporary_file: str) -> Path:
    """Salva o dicionário como arquivo JSON e retorna o caminho absoluto."""
    try:
        temp_folder = Path(temporary_folder)
        temp_folder.mkdir(parents=True, exist_ok=True)

        path_credencial = temp_folder / temporary_file

        with open(path_credencial, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)

        return path_credencial.resolve()
    except Exception as e:
        log.exception(f"Erro ao salvar arquivo de credenciais: {e}")
        raise


def salvar_credenciais(
    on_server: bool,
    usar_google_application_credentials: bool,
    temporary_folder: str,
    temporary_file: str,
    salvar_dividido: bool = False,
) -> None:
    """
    Gera o arquivo JSON de credenciais do Google Cloud a partir de variáveis de ambiente
    e define a variável 'GOOGLE_APPLICATION_CREDENTIALS'.
    """
    if _deve_pular_setup(on_server, usar_google_application_credentials):
        return

    try:
        chave = _obter_dicionario_credenciais(salvar_dividido)
        path_absolute = str(_salvar_arquivo_json(chave, temporary_folder, temporary_file))

        environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_absolute
        log.info(f"Arquivo de credenciais salvo e configurado em: {path_absolute}")

    except Exception as e:
        log.exception(f"Erro crítico na criação do arquivo de credenciais: {e}")
        raise
