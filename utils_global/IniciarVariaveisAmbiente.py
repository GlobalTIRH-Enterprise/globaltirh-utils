import warnings
from utils_global.config.IniciarVariaveisAmbiente import inicializar_variaveis_de_ambiente

warnings.warn(
    "utils_global.IniciarVariaveisAmbiente is deprecated. Use utils_global.config.IniciarVariaveisAmbiente or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)
