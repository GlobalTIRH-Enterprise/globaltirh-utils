import warnings
from utils_global.config.CreateLogger import log, FormatadorColorido

warnings.warn(
    "utils_global.CreateLogger is deprecated. Use utils_global.config.CreateLogger or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)