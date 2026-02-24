# from os import path
# from typing import List, Tuple, Set
# from werkzeug.datastructures import FileStorage

# def ler_e_validar_request_files(files: FileStorage | List[FileStorage], allowed_extensions: Set) -> Tuple[List[FileStorage], List[str]]:
#     """
#     Lê e valida arquivos enviados em uma requisição, verificando suas extensões.

#     Args:
#         files: Um objeto FileStorage ou uma lista de objetos FileStorage representando os arquivos enviados.
#         allowed_extensions: Um conjunto (Set) contendo as extensões de arquivo permitidas (ex: {".pdf", ".png"}).

#     Returns:
#         Uma tupla contendo:
#             - Uma lista de objetos FileStorage válidos.
#             - Uma lista de mensagens de erro encontradas durante a validação.

#     Raises:
#         ValueError: Se nenhum arquivo for enviado na requisição.
#     """
#     valid_files: List[FileStorage] = []
#     error_messages: List[str] = []

#     if not files:
#         raise ValueError("Nenhum arquivo foi enviado na requisição.")

#     if not isinstance(files, list):
#         files = [files]

#     for file in files:
#         if file.filename == '':
#             error_messages.append(f"O arquivo enviado não possui um nome definido.")
#         elif not file:
#             error_messages.append(f"O arquivo '{file.filename}' está vazio ou corrompido.")
#         elif file is None:
#             error_messages.append(f"O arquivo '{file.filename}' está nulo")
#         elif not isinstance(file.filename, str):
#             error_messages.append(f"O arquivo '{file.filename}' não é uma string válida")
#         elif path.splitext(file.filename)[1] not in allowed_extensions:
#             error_messages.append(f"O arquivo '{file.filename}' não está em um formato suportado: '{allowed_extensions}'")
#         elif file.filename:
#             valid_files.append(file)
#         else:
#             error_messages.append(f"Erro desconhecido ao processar o arquivo '{file.filename}'.")

#     return valid_files, error_messages