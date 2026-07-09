import warnings
from utils_global.gcp.auth.SalvarCredenciais import salvar_credenciais

warnings.warn(
    "utils_global.SalvarCredenciais is deprecated. Use utils_global.gcp.auth.SalvarCredenciais or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)
