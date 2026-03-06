# globaltirh-utils

Repositório de utilidades para projetos da **GlobalTIRH**.

Este pacote fornece um conjunto de funções utilitárias para integração com serviços do **Google Cloud Platform (GCP)** e ferramentas auxiliares para manipulação de dados, validação, formatação, autenticação e logging.

O objetivo da biblioteca é **padronizar operações comuns utilizadas nos projetos da organização**, facilitando reutilização de código e reduzindo duplicação de lógica.

O import do pacote globaltirh-utils está presente somente nos seguintes repositórios:

Compara-es-Gemini

Backend-SES-SaudeDigital

ses-go-portal-transparencia

---

# Instalação

O pacote pode ser instalado diretamente do repositório GitHub utilizando `pip`.

```bash
pip install git+https://github.com/GlobalTIRH-Enterprise/globaltirh-utils.git@deploy
```

Após a instalação, os módulos ficam disponíveis para importação nos projetos Python.

---

# Estrutura do Pacote

A biblioteca é organizada em dois módulos principais:

- **functions_global** → funções relacionadas a integrações com serviços cloud  
- **utils_global** → utilidades gerais usadas em diversos projetos

```
functions_global/
├── cloud/
│   ├── big_query/      # Integração com Google BigQuery
│   ├── gemini/         # Integração com modelos Gemini (Vertex AI)
│   └── storage/        # Operações com Google Cloud Storage

utils_global/
```

---

# Funcionalidades

## 1. Integração com Google BigQuery

Módulo:

```
functions_global.cloud.big_query
```

Fornece funções utilitárias para gerenciamento de datasets, tabelas e execução de consultas no **Google BigQuery**.

### Funções disponíveis

#### create_dataset

Arquivo: `CreateDataset.py`

```python
create_dataset(client, dataset_id, location="US", description=None)
```

Cria um dataset no BigQuery.

Retorno:
- `True` caso o dataset seja criado ou já exista.

---

#### create_table

Arquivo: `CreateTable.py`

```python
create_table(client, dataset_id, table_id, schema)
```

Cria uma tabela dentro de um dataset com o schema informado.

---

#### insert_data

Arquivo: `InsertData.py`

```python
insert_data(client, dataset_id, table_id, rows_to_insert, schema)
```

Insere dados em uma tabela do BigQuery.

Retorno:
- Lista de erros caso existam falhas na inserção.

---

#### delete_table

Arquivo: `DeleteTable.py`

```python
delete_table(client, dataset_id, table_id, must_exist=False)
```

Remove uma tabela do dataset.

---

#### get_data

Arquivo: `GetData.py`

```python
get_data(client, dataset_id, table_id, where_clauses=None, limit=0)
```

Executa consulta em uma tabela do BigQuery com filtros opcionais.

---

#### run_select_query

Arquivo: `RunSelectQuery.py`

```python
run_select_query(client, query, output_format="list")
```

Executa uma query `SELECT` no BigQuery.

Retorno pode ser:

- `list` → lista de dicionários  
- `DataFrame` → dataframe do pandas

---

# 2. Google Cloud Storage

Módulo:

```
functions_global.cloud.storage
```

Fornece funções para manipulação de arquivos no **Google Cloud Storage (GCS)**.

### Funções disponíveis

#### get_bucket

Arquivo: `GetBucket.py`

```python
get_bucket(client, bucket_name)
```

Obtém uma referência para um bucket existente.

Caso o bucket não exista, uma exceção é lançada.

---

#### upload_file_to_gcs

Arquivo: `UploadFileToGcs.py`

```python
upload_file_to_gcs(client, bucket_name, filename, destination_blob_name, temporary_folder=None)
```

Realiza upload de um arquivo local para o bucket.

Retorno:

```
gs://bucket/path/file
```

---

#### listar_conteudo

Arquivo: `ListarConteudo.py`

```python
listar_conteudo(client, bucket_name, prefixo=None)
```

Lista arquivos do bucket e retorna metadados.

---

#### deletar_arquivo

Arquivo: `DeletarArquivo.py`

```python
deletar_arquivo(client, bucket_name, nome_arquivo)
```

Remove um arquivo do bucket.

---

#### download_arquivo

Arquivo: `DownloadArquivo.py`

```python
download_arquivo(client, bucket_name, nome_arquivo)
```

Baixa um arquivo para um diretório temporário.

Retorno:
- Caminho local do arquivo.

---

#### obter_metadados

Arquivo: `ObterMetadados.py`

```python
obter_metadados(client, bucket_name, nome_arquivo)
```

Retorna metadados de um arquivo.

---

#### valida_existencia_do_arquivo

Arquivo: `ValidaExistenciaDoArquivo.py`

```python
valida_existencia_do_arquivo(client, bucket_name, nome_arquivo)
```

Verifica se o arquivo existe no bucket.

Retorno:

- objeto `Blob` caso exista  
- exceção caso não exista

---

# 3. Google Gemini (Vertex AI)

Módulo:

```
functions_global.cloud.gemini
```

Integração com modelos **Gemini da Vertex AI**, com suporte a prompts, anexos e streaming de resposta.

---

### call_gemini_non_streaming

Arquivo: `CallGemini.py`

```python
call_gemini_non_streaming(
    prompt,
    project_id,
    location,
    model_name,
    arquivos=None,
    generation_config=None,
    return_only_text=True
)
```

Executa chamada síncrona ao modelo Gemini.

---

### call_gemini_streaming

Arquivo: `CallGeminiStreaming.py`

```python
call_gemini_streaming(
    prompt,
    project_id,
    location,
    model_name,
    arquivos=None,
    generation_config=None,
    return_only_text=True
)
```

Executa chamada com **streaming de resposta**.

---

# 4. Utilitários Gerais

Módulo:

```
utils_global
```

Contém diversas funções auxiliares reutilizáveis.

---

## CheckContentsValid

Arquivo:

```
CheckContentsValid.py
```

```python
check_content_is_valid(content: list)
```

Valida estrutura de lista de mensagens (`role` e `parts`).

---

## CreateLogger

Arquivo:

```
CreateLogger.py
```

Fornece um logger configurado com cores ANSI.

Componentes:

- `FormatadorColorido`
- `log`

---

## FormatarTextoIdentificador

Arquivo:

```
FormatarTextoIdentificador.py
```

```python
formatar_texto_para_identificador(text: str) -> str
```

Remove acentos, substitui espaços por `_` e converte para minúsculas.

Exemplo:

```
"Nome do Arquivo" -> "nome_do_arquivo"
```

---

## GenerateAccessToken

Arquivo:

```
GenerateAccessToken.py
```

```python
generate_access_token(
    client_email,
    private_key_id,
    private_key,
    scope,
    expires_in=3600
)
```

Gera **access token OAuth2** usando credenciais de conta de serviço.

---

## GetDictFromText

Arquivo:

```
GetDictFromText.py
```

```python
get_dict_from_text(text: str) -> dict
```

Extrai JSON de textos, incluindo blocos ```json.

---

## GuessMimeType

Arquivo:

```
GuessMimeType.py
```

```python
guess_mimetype(path: str)
```

Detecta automaticamente o tipo MIME de um arquivo.

---

## IniciarVariaveisAmbiente

Arquivo:

```
IniciarVariaveisAmbiente.py
```

```python
inicializar_variaveis_de_ambiente(possible_locations=None, verbose=0)
```

Carrega automaticamente arquivos `.env`.

---

## ProcessaUneStrings

Arquivo:

```
ProcessaUneStrings.py
```

```python
processa_une_strings(string_list)
```

Remove duplicatas e concatena strings únicas.

---

## SalvarCredenciais

Arquivo:

```
SalvarCredenciais.py
```

```python
salvar_credenciais(
    on_server,
    usar_google_application_credentials,
    temporary_folder,
    temporary_file,
    salvar_dividido=False
)
```

Gera arquivo JSON de credenciais do Google a partir de variáveis de ambiente.

---

## StringToBool

Arquivo:

```
StringToBool.py
```

```python
string_to_bool(s)
```

Converte diferentes representações para booleano.

Exemplos aceitos:

```
true
false
1
0
s
n
```

---

## TempoToBrasilia

Arquivo:

```
TempoToBrasilia.py
```

```python
tempo_to_brasilia(dt)
```

Converte datas para o fuso horário de **Brasília (UTC-3)**.

---

## ValidarGsutilLink

Arquivo:

```
ValidarGsutilLink.py
```

```python
validar_gsutil_link(link, quant_parts=4, tipos_verificar=None)
```

Valida links no formato:

```
gs://bucket/path/file
```

---

## VerificaTipo

Arquivo:

```
VerificaTipo.py
```

Decorator que valida automaticamente tipos de parâmetros.

```python
@deco_verifica_tipo
```

Também inclui função auxiliar:

```python
verifica_tipo(params)
```

---

## VolumeReader

Arquivo:

```
VolumeReader.py
```

```python
volume_read(nome_arquivo, on_server, mounted_volume_name)
```

Lê arquivos de um volume montado.

Retorno:

- `.json` → `dict` ou `list`
- texto → `str`
- binário → `bytes`

Caminho utilizado:

- Servidor → `/mounted_volume_name/`
- Local → `./data/mounted_volume_name/`

---

## VolumeWriter

Arquivo:

```
VolumeWriter.py
```

```python
volume_write(nome_arquivo, content, on_server, mounted_volume_name, mounted_volume_read_only)
```

Escreve conteúdo em um volume montado.

Comportamento:

- `dict` ou `list` com extensão `.json` → salvo como JSON formatado
- outros tipos → salvos como `str` ou `bytes`

A função cria automaticamente os diretórios necessários e, quando executada no servidor, verifica se o volume está configurado como somente leitura antes de gravar.

# Testes

Os testes unitários estão no diretório:

```
tests/
```

Para executar os testes:

```bash
pytest tests/
```

---


# Licença

Projeto de uso interno da **GlobalTIRH**.