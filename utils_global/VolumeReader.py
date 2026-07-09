import warnings
from utils_global.io.VolumeReader import volume_read

warnings.warn(
    "utils_global.VolumeReader is deprecated. Use utils_global.io.VolumeReader or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)