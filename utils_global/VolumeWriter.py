import warnings
from utils_global.io.VolumeWriter import volume_write

warnings.warn(
    "utils_global.VolumeWriter is deprecated. Use utils_global.io.VolumeWriter or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)