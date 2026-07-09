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

A biblioteca é organizada em dois módulos principais, estruturados de acordo com o propósito de suas funções:

- **functions** → funções relacionadas a integrações de maior porte com serviços cloud  
- **utils** → utilidades granulares categorizadas por domínio de uso

```
functions/
├── cloud/
│   ├── big_query/      # Integração com Google BigQuery
│   ├── gemini/         # Integração com modelos Gemini (Vertex AI)
│   └── storage/        # Operações com Google Cloud Storage

utils/
├── config/             # Configurações de logging e leitura de variáveis de ambiente
├── datetime/           # Conversões de data e hora para fuso horário de Brasília
├── gcp/                # Integrações utilitárias com serviços GCP
│   ├── auth/           # Geração de tokens de acesso e salvamento de credenciais JSON
│   ├── big_query/      # Utilitários futuros para BigQuery
│   ├── gemini/         # Validação de conteúdo estruturado do Gemini
│   └── storage/        # Validação de links de GCS (gsutil)
├── io/                 # Operações de leitura/escrita de volumes e identificação de MimeTypes
├── text/               # Formatação, união e extração de strings e conversões textuais
└── validation/         # Decorators e utilitários de validação estrita de tipos em tempo de execução
```

---

# Funcionalidades

## 1. Integração com Google BigQuery

Módulo:

```
functions.cloud.big_query
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
functions.cloud.storage
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
functions.cloud.gemini
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

Módulo principal:

```
utils
```

Este pacote é estruturado de forma modular através de subpacotes dedicados a propósitos específicos. Todos os símbolos também continuam convenientemente importados e expostos no nível raiz do pacote (ex: `from utils import log` ou `from utils import tempo_to_brasilia`), além de estarem disponíveis para importação direta através de seus respectivos subpacotes.

---

## 4.1 Configuração e Logs (config)

Subpacote: `utils.config`

### CreateLogger
* **Módulo:** `utils.config.CreateLogger`
* **Import:** `from utils.config.CreateLogger import log, FormatadorColorido` (ou `from utils import log`)

Fornece um logger configurado com cores ANSI para terminais.

---

### IniciarVariaveisAmbiente
* **Módulo:** `utils.config.IniciarVariaveisAmbiente`
* **Import:** `from utils.config.IniciarVariaveisAmbiente import inicializar_variaveis_de_ambiente` (ou `from utils import inicializar_variaveis_de_ambiente`)

```python
inicializar_variaveis_de_ambiente(possible_locations=None, verbose=0)
```

Carrega automaticamente arquivos `.env` a partir de diretórios pré-configurados ou customizados.

---

## 4.2 Data e Hora (datetime)

Subpacote: `utils.datetime`

### TempoToBrasilia
* **Módulo:** `utils.datetime.TempoToBrasilia`
* **Import:** `from utils.datetime.TempoToBrasilia import tempo_to_brasilia` (ou `from utils import tempo_to_brasilia`)

```python
tempo_to_brasilia(dt)
```

Converte datas para o fuso horário de **Brasília (UTC-3)** com tratamento correto de timezone.

---

## 4.3 Utilitários GCP (gcp)

Subpacote: `utils.gcp`

### SalvarCredenciais
* **Módulo:** `utils.gcp.auth.SalvarCredenciais`
* **Import:** `from utils.gcp.auth.SalvarCredenciais import salvar_credenciais` (ou `from utils import salvar_credenciais`)

```python
salvar_credenciais(on_server, usar_google_application_credentials, temporary_folder, temporary_file, salvar_dividido=False)
```

Gera arquivos JSON temporários contendo credenciais de conta de serviço do GCP para autenticação de bibliotecas do Google.

---

### GenerateAccessToken
* **Módulo:** `utils.gcp.auth.GenerateAccessToken`
* **Import:** `from utils.gcp.auth.GenerateAccessToken import generate_access_token` (ou `from utils import generate_access_token`)

```python
generate_access_token(client_email, private_key_id, private_key, scope, expires_in=3600)
```

Gera tokens de acesso OAuth2 usando assinatura manual de JWTs com a chave privada da conta de serviço.

---

### CheckContentIsValid
* **Módulo:** `utils.gcp.gemini.CheckContentIsValid`
* **Import:** `from utils.gcp.gemini.CheckContentIsValid import check_content_is_valid` (ou `from utils import check_content_is_valid`)

```python
check_content_is_valid(content: list)
```

Valida o formato e estrutura de listas de conteúdo para envio à API do Gemini (`role` e `parts`).

---

### ValidarGsutilLink
* **Módulo:** `utils.gcp.storage.ValidarGsutilLink`
* **Import:** `from utils.gcp.storage.ValidarGsutilLink import validar_gsutil_link` (ou `from utils import validar_gsutil_link`)

```python
validar_gsutil_link(link, quant_parts=4, tipos_verificar=None)
```

Valida a formatação de URIs do Google Cloud Storage (`gs://...`).

---

## 4.4 Entrada/Saída e Arquivos (io)

Subpacote: `utils.io`

### GuessMimeType
* **Módulo:** `utils.io.GuessMimeType`
* **Import:** `from utils.io.GuessMimeType import guess_mimetype` (ou `from utils import guess_mimetype`)

```python
guess_mimetype(path: str)
```

Detecta automaticamente o tipo MIME correto de arquivos (com fallbacks para formatos comuns de texto).

---

### VolumeReader
* **Módulo:** `utils.io.VolumeReader`
* **Import:** `from utils.io.VolumeReader import volume_read` (ou `from utils import volume_read`)

```python
volume_read(nome_arquivo, on_server, mounted_volume_name)
```

Lê arquivos de um volume de disco compartilhado montado no servidor ou de uma estrutura de pastas local simulada.

---

### VolumeWriter
* **Módulo:** `utils.io.VolumeWriter`
* **Import:** `from utils.io.VolumeWriter import volume_write` (ou `from utils import volume_write`)

```python
volume_write(nome_arquivo, content, on_server, mounted_volume_name, mounted_volume_read_only)
```

Grava com segurança diferentes formatos (JSON, strings, bytes) em volumes de disco compartilhados montados.

---

## 4.5 Processamento de Texto (text)

Subpacote: `utils.text`

### FormatarTextoIdentificador
* **Módulo:** `utils.text.FormatarTextoIdentificador`
* **Import:** `from utils.text.FormatarTextoIdentificador import formatar_texto_para_identificador` (ou `from utils import formatar_texto_para_identificador`)

```python
formatar_texto_para_identificador(text: str) -> str
```

Normaliza strings (remoção de pontuações, conversão de acentuações para ASCII e espaços para sublinhados) para criação de slugs ou identificadores de arquivos.

---

### GetDictFromText
* **Módulo:** `utils.text.GetDictFromText`
* **Import:** `from utils.text.GetDictFromText import get_dict_from_text` (ou `from utils import get_dict_from_text`)

```python
get_dict_from_text(text: str) -> dict
```

Identifica, extrai e converte blocos JSON embutidos em textos retornados por modelos LLM.

---

### ProcessaUneStrings
* **Módulo:** `utils.text.ProcessaUneStrings`
* **Import:** `from utils.text.ProcessaUneStrings import processa_une_strings` (ou `from utils import processa_une_strings`)

```python
processa_une_strings(string_list)
```

Deduz e elimina duplicatas de texto de forma estrita ou normalizada, unindo os pedaços de string resultantes.

---

### StringToBool
* **Módulo:** `utils.text.StringToBool`
* **Import:** `from utils.text.StringToBool import string_to_bool` (ou `from utils import string_to_bool`)

```python
string_to_bool(s)
```

Converte strings e representações variadas em valores booleanos do Python.

---

## 4.6 Validação de Dados (validation)

Subpacote: `utils.validation`

### VerificaTipo
* **Módulo:** `utils.validation.VerificaTipo`
* **Import:** `from utils.validation.VerificaTipo import verifica_tipo, deco_verifica_tipo` (ou `from utils import verifica_tipo, deco_verifica_tipo`)

```python
@deco_verifica_tipo
def minha_funcao(arg: str):
    pass
```

Decorator e funções auxiliares de verificação estrita de tipos dos argumentos de funções baseados em Type Hints em tempo de execução.

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