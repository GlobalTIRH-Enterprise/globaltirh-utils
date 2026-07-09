from json import loads
from utils_global.validation.VerificaTipo import verifica_tipo, deco_verifica_tipo


@deco_verifica_tipo
def get_dict_from_text(text: str) -> dict:
    """
    Extrai um dicionário Python de uma string de texto.

    A função tenta localizar um bloco JSON delimitado por "```json" e "```".
    Caso os delimitadores de bloco de código não sejam encontrados, a função tenta
    localizar o primeiro caractere '{' e o último '}' para extrair o conteúdo JSON.

    Args:
        text: A string de texto contendo o JSON.

    Returns:
        Um dicionário Python representando o JSON extraído.

    Raises:
        json.JSONDecodeError: Se a string extraída não for um JSON válido.
        TypeError: Se a entrada não for uma string.
        ValueError: Se não for possível encontrar um JSON válido no texto.

    """

    start_delimiter, end_delimiter = "```json", "```"

    start_index = text.find(start_delimiter)

    # Se encontrou o início do bloco de código, tenta processar como bloco markdown
    if start_index != -1:
        end_index = text.rfind(end_delimiter)
        if end_index != -1:
            json_text = text[start_index + len(start_delimiter) : end_index].strip()
            return loads(json_text)

    # Caso contrário (ou se não fechou o bloco), tenta encontrar pelo primeiro '{' e último '}'
    start_index = text.find("{")
    end_index = text.rfind("}")

    if start_index != -1 and end_index != -1 and start_index < end_index:
        json_text = text[start_index : end_index + 1].strip()
        return loads(json_text)

    raise ValueError(
        "Não foi possível encontrar um JSON válido no texto (nem via blocos de código nem via chaves {})."
    )
