import mimetypes
from typing import Optional
from .VerificaTipo import deco_verifica_tipo


@deco_verifica_tipo
def guess_mime(path: str) -> Optional[str]:
    mt = mimetypes.guess_type(path)[0]
    if mt:
        return mt
    if path.endswith(".pdf"):
        return "application/pdf"
    if path.endswith((".txt", ".md", ".csv", ".log")):
        return "text/plain"
    return None  # deixa o SDK decidir/errar cedo
