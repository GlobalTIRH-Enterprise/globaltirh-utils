from os import getenv
from typing import List, Union, Optional
from google.genai import types, Client
from globaltirh_utils.GuessMimeType import guess_mimetype
from globaltirh_utils.CreateLogger import log


def call_gemini(
    prompt: str,
    project_id: str,
    location: str,
    model_name: str,
    arquivos: Union[List[str], str, None] = None,
    generation_config: Optional[types.GenerateContentConfig] = None,
    stream: bool = False,
    return_only_text: bool = True,
):
    """Chama Gemini (google-genai) com prompt + anexos (gs:// ou locais)."""
    
    # model_name e generation_config devem ser passados explicitamente se necessário

    client = Client(
        vertexai=True,
        project=project_id,
        location=location
    )

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
        if stream:
            stream_obj = client.models.generate_content_stream(
                model=model_name, 
                contents=contents,
                config=generation_config
            )
            if return_only_text:
                return "".join(chunk.text or "" for chunk in stream_obj if getattr(chunk, "text", None))
            return stream_obj
        
        else:
            resp = client.models.generate_content(
                model=model_name, 
                contents=contents,
                config=generation_config
            )
            return resp.text if return_only_text else resp
        
    except Exception as e:
        log.error(f"Erro ao chamar o modelo Gemini: {e}", exc_info=True)
        raise
