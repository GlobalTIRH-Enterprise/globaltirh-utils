from typing import Union
from datetime import datetime, timezone
import pytz


def tempo_to_brasilia(dt: Union[datetime, float]) -> datetime:
    """
    Converte um objeto datetime (com ou sem timezone) ou um timestamp float (segundos desde a época Unix UTC)
    para um objeto datetime com timezone de Brasília (America/Sao_Paulo).

    Args:
        dt (datetime | float): Objeto datetime (timezone-aware ou naive) ou timestamp float UTC.

    Returns:
        datetime: Objeto datetime com timezone de Brasília.
    """
    if isinstance(dt, float):
        dt = datetime.fromtimestamp(dt, tz=timezone.utc)
    elif not isinstance(dt, datetime):
        raise TypeError(f"Esperado datetime ou float, recebido {type(dt)}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    return dt.astimezone(pytz.timezone("America/Sao_Paulo"))