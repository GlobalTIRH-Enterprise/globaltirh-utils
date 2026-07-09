import jwt  # Da bib PyJWT
import time
import requests
from utils_global.validation.VerificaTipo import deco_verifica_tipo


@deco_verifica_tipo
def generate_access_token(
    client_email: str,
    private_key_id: str,
    private_key: str,
    scope: str,
    expires_in: int = 3600,
) -> str:
    """
    Gera token OAuth 2.0 via conta de serviço Google.

    Args:
        client_email: Email da conta de serviço.
        private_key_id: ID da chave privada.
        private_key: Chave privada RSA.
        scope: Escopos de permissão.
        expires_in: Expiração em segundos (padrão 3600).

    Returns:
        Token de acesso.
    """

    if "\\n" in private_key:
        private_key = private_key.replace("\\n", "\n")

    # Cria cabeçalho JWT
    jwt_headers = {"kid": private_key_id, "alg": "RS256", "typ": "JWT"}

    # Cria payload JWT
    now = int(time.time())

    jwt_payload = {
        "iss": client_email,
        "sub": client_email,
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now,
        "exp": now + expires_in,
        "scope": scope,
    }

    # Assina JWT
    signed_jwt = jwt.encode(jwt_payload, private_key, algorithm="RS256", headers=jwt_headers)

    # Troca JWT por Access Token
    token_endpoint = "https://oauth2.googleapis.com/token"
    request_body = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": signed_jwt,
    }

    print("Solicitando token de acesso do Google...")
    response = requests.post(token_endpoint, data=request_body)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        print("Token de acesso obtido com sucesso.")
        return access_token
    else:
        print(f"Erro ao obter o token de acesso: {response.status_code} - {response.text}")
        raise Exception(
            f"Falha ao obter o token de acesso. Status: {response.status_code}, Resposta: {response.text}"
        )
