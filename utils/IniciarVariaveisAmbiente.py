import os
import re
from typing import Optional
from dotenv import find_dotenv, load_dotenv
from .VerificaTipo import deco_verifica_tipo

ENV_PATTERN = re.compile(r"(\w+)\s*=\s*'([^']+)'?")


@deco_verifica_tipo
def inicializar_variaveis_de_ambiente(
    possible_locations: Optional[list[str]] = None, verbose: int = 0
) -> bool:
    """
    Inicializa as variáveis de ambiente a partir de arquivos .env ou da variável 'envs_texts'.

    O algoritmo realiza os seguintes passos:
    1. Busca por arquivos .env em uma lista de caminhos predefinidos ou fornecidos.
    2. Se encontrar e o arquivo contiver dados válidos, as variáveis são carregadas no ambiente.
    3. Caso o arquivo .env não seja encontrado ou esteja vazio, tenta extrair as variáveis
        de uma string formatada contida na variável de ambiente 'envs_texts'.

    Args:
        possible_locations (list[str] | None, opcional):
        Lista de caminhos para buscar o arquivo .env. Se None for passado, utiliza uma lista padrão de diretórios. Padrão é None.
        verbose (int, opcional): Nível de verbosidade para logs.
            0: Sem output.
            1: Informações básicas de sucesso/falha.
            2: Detalhes sobre a busca de arquivos e fallback.
            3: Logs detalhados de cada variável carregada.
            Padrão é 0.

    Returns:
        bool: Retorna True se as variáveis foram carregadas com sucesso (seja pelo .env ou
            pela variável 'envs_texts'), e False caso contrário.
    """
    if verbose >= 1:
        print("-- IniciarVariaveisAmbiente: Iniciando a inicialização de variáveis de ambiente")

    if possible_locations is None:
        possible_locations = [
            r".env",
            r"/secrets/.env",
            r"secrets/.env",
            r"/credenciais/.env",
            r"credenciais/.env",
        ]

    # 1. Tenta encontrar e carregar a partir de um arquivo .env
    if possible_locations:
        for caminho in possible_locations:
            # usecwd=True evita que o find_dotenv tente inspecionar a stack (o que falha com decorators)
            found_path = find_dotenv(caminho, usecwd=True)
            if found_path:
                if verbose >= 2:
                    print(f"Arquivo .env encontrado no caminho: {caminho}")

                if load_dotenv(found_path):
                    if verbose >= 1:
                        print(
                            "-- IniciarVariaveisAmbiente: Variáveis do arquivo .env carregadas com sucesso!"
                        )
                    return True

                if verbose >= 2:
                    print(f"Arquivo .env em {caminho} foi encontrado, mas está vazio ou inválido.")

    if verbose >= 2:
        print(
            "-- IniciarVariaveisAmbiente: Não foi possível carregar via .env. Tentando utilizar a variável 'envs_texts'."
        )

    # 2. Fallback: tenta carregar a partir da variável de ambiente 'envs_texts'
    envs_text = os.getenv("envs_texts")

    if envs_text and isinstance(envs_text, str):
        if verbose >= 2:
            print("-- IniciarVariaveisAmbiente: Extraindo variáveis da string 'envs_texts'")
        pares = ENV_PATTERN.findall(envs_text)

        if pares:
            for chave, valor in pares:
                os.environ[chave] = valor
                if verbose >= 3:
                    print(f"Variável de ambiente definida via texto: {chave}='***'")

            if verbose >= 1:
                print(
                    "-- IniciarVariaveisAmbiente: Variáveis de ambiente carregadas com sucesso através de 'envs_texts'."
                )
            return True

    if verbose >= 1:
        print("-- IniciarVariaveisAmbiente: Nenhuma variável de ambiente foi carregada.")
    return False
