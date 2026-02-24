# globaltirh-utils

Repositório de Utilidades para Globaltirh

Este repositório contém uma coleção de funções e classes utilitárias para lidar com validações, formatações e tratamento de dados comuns em projetos da Globaltirh.

## Instalação

```bash
pip install git+https://github.com/GlobalTIRH-Enterprise/globaltirh-utils.git@deploy
```

## Utilitários Disponíveis

Abaixo estão listados os módulos e funções disponíveis nesta biblioteca:

### 1. Validação de Conteúdo (`CheckContentIsValid`)

* **Função:** `check_content_is_valid(content: list) -> None`
* **Descrição:** Valida a estrutura de uma lista de conteúdos (geralmente usada para histórico de chat). Verifica se cada item é um dicionário contendo as chaves obrigatórias `role` (user/model) e `parts`.

### 2. Formatação de Logs (`CreateLogger`)

* **Classe:** `FormatadorColorido`
* **Descrição:** Um `logging.Formatter` personalizado que adiciona cores ANSI às mensagens de log baseadas no nível de severidade (DEBUG, INFO, WARNING, ERROR, CRITICAL).

### 3. Formatação de Identificadores (`FormatarTextoIdentificador`)

* **Função:** `formatar_texto_para_identificador(text: str) -> str`
* **Descrição:** Transforma uma string em um identificador seguro. Remove acentos, pontuações, substitui espaços por underscores e converte para minúsculas.

### 4. Extração de JSON (`GetDictFromText`)

* **Função:** `get_dict_from_text(text: str) -> dict`
* **Descrição:** Tenta extrair e converter um bloco JSON contido em uma string de texto. Suporta blocos de código Markdown (` ```json ... ``` `) ou busca direta por chaves `{}`.

### 5. Inferência de MIME Type (`GuessMimeType`)

* **Função:** `guess_mimetype(path: str) -> Optional[str]`
* **Descrição:** Infere o tipo MIME de um arquivo com base no seu caminho ou nome. Possui fallbacks para PDF e arquivos de texto caso a detecção nativa do sistema falhe.

### 6. Variáveis de Ambiente (`IniciarVariaveisAmbiente`)

* **Função:** `inicializar_variaveis_de_ambiente(possible_locations: Optional[list[str]] = None, verbose: int = 0) -> bool`
* **Descrição:** Carrega variáveis de ambiente a partir de arquivos `.env` ou de strings de configuração. Busca em locais padrão ou personalizados.

### 7. Processamento de Strings (`ProcessaUneStrings`)

* **Função:** `processa_une_strings(string_list: List[str]) -> str`
* **Descrição:** Remove duplicatas de uma lista de strings (normalizando por espaços e caixa alta/baixa) e retorna uma única string com os valores únicos unidos.

### 8. Conversão Booleana (`StringToBool`)

* **Função:** `string_to_bool(s: str | bool) -> bool`
* **Descrição:** Converte strings como "true", "1", "s", "verdadeiro" (e suas variantes negativas) para valores booleanos (`True`/`False`).

### 9. Conversão de Fuso Horário (`TempoToBrasilia`)

* **Função:** `tempo_to_brasilia(dt: Union[datetime, float]) -> datetime`
* **Descrição:** Converte um objeto `datetime` ou timestamp float para o fuso horário de Brasília (`America/Sao_Paulo`).

### 10. Validação de Links Gsutil (`ValidarGsutilLink`)

* **Função:** `validar_gsutil_link(link: str, quant_parts: int = 4, tipos_verificar: Optional[Set[str]] = None) -> None`
* **Descrição:** Valida se um link segue o formato `gs://...`, verificando a quantidade de partes do caminho e opcionalmente a extensão do arquivo.

### 11. Validação de Tipos (`VerificaTipo`)

* **Decorator:** `@deco_verifica_tipo`
* **Função:** `verifica_tipo(params: list)`
* **Descrição:** Fornece um decorator e uma função auxiliar para validar dinamicamente os tipos dos argumentos passados para funções, baseando-se nas anotações de tipo (type hints).

---

## Testes

O repositório conta com uma suíte de testes unitários para garantir o funcionamento correto de cada utilitário. Os arquivos de teste podem ser encontrados no diretório `tests/`.
