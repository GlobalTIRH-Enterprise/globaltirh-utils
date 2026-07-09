import warnings
from utils_global.io.GuessMimeType import guess_mimetype

warnings.warn(
    "utils_global.GuessMimeType is deprecated. Use utils_global.io.GuessMimeType or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)
