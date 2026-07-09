import warnings
from utils_global.validation.VerificaTipo import verifica_tipo, deco_verifica_tipo

warnings.warn(
    "utils_global.VerificaTipo is deprecated. Use utils_global.validation.VerificaTipo or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)
