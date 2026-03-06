from os import getenv
from typing import List, Union, Optional
from google.genai import types, Client
from utils_global.GuessMimeType import guess_mimetype
from utils_global.CreateLogger import log

def call_gemini_streaming(
    prompt: str,
    project: str,
    location: str,
    model_name: str,
    arquivos: Union[List[str], str, None] = None,
    generation_config: Optional[types.GenerateContentConfig] = None,
    return_only_text: bool = True,
):
    """
    Chama Gemini (google-genai) com streaming ativado.

    Args:
        prompt: Texto do prompt.
        project_id: ID do projeto Google Cloud.
        location: Localização (ex.: us-central1).
        model_name: Nome do modelo Gemini (ex.: gemini-1.5-pro).
        arquivos: Lista ou string com caminhos para arquivos (locais ou gs://).
        generation_config: Configuração de geração opcional.
        return_only_text: Se True, retorna apenas o texto concatenado; caso contrário, retorna o objeto stream.

    Returns:
        Se return_only_text for True, retorna uma string com o texto gerado.
        Caso contrário, retorna o objeto gerador do stream.
    """
    client = Client(vertexai=True, project=project, location=location)

    contents: List[Union[str, types.Part]] = [prompt]

    if arquivos:
        for arq in ([arquivos] if isinstance(arquivos, str) else arquivos):
            mime = guess_mimetype(arq)
            try:
                if arq.startswith("gs://"):
                    if not mime:
                        raise ValueError(f"Não foi possível inferir MIME: {arq}")
                    contents.append(types.Part.from_uri(file_uri=arq, mime_type=mime))
                elif mime == "text/plain":
                    with open(arq, "r", encoding="utf-8") as f:
                        contents.append(f.read())
                else:
                    if not mime:
                        raise ValueError(f"Não foi possível inferir MIME: {arq}")
                    with open(arq, "rb") as f:
                        contents.append(types.Part.from_bytes(data=f.read(), mime_type=mime))
            except FileNotFoundError:
                raise FileNotFoundError(f"Arquivo não encontrado: {arq}")
            except Exception as e:
                log.error(f"Erro ao anexar {arq}: {e}")
                raise

    try:
        stream_obj = client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=generation_config
        )
        if return_only_text:
            return "".join(chunk.text or "" for chunk in stream_obj if getattr(chunk, "text", None))
        return stream_obj
    except Exception as e:
        log.error(f"Erro ao chamar o modelo Gemini com streaming: {e}", exc_info=True)
        raise

