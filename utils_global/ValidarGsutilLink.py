import warnings
from utils_global.gcp.storage.ValidarGsutilLink import validar_gsutil_link

warnings.warn(
    "utils_global.ValidarGsutilLink is deprecated. Use utils_global.gcp.storage.ValidarGsutilLink or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)
