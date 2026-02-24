from .VerificaTipo import deco_verifica_tipo

@deco_verifica_tipo
def list_content_is_valid(content: list):

    if not isinstance(content, list):
        return False, "Não é uma lista"
    for elem in content:
        if not isinstance(elem, dict):
            return False, "Os elementos de conteúdo anterior não são objetos"
        if "role" not in elem and "parts" not in elem:
            return (
                False,
                "A lista de conteúdos anteriores não contém as chaves necessárias 'role' e 'parts'",
            )
        if elem["role"] not in ["user", "model"]:
            return False, "Valor de 'role' deve ser 'model' ou 'user'"
        if not isinstance(elem["parts"], list):
            return False, "Campo 'parts' deve ser uma lista"
        for part in elem["parts"]:
            if not isinstance(part, dict):
                return False, "Cada elemento de 'parts' deve ser objeto"

    return True, None
