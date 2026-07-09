import warnings
from utils_global.text.StringToBool import string_to_bool

warnings.warn(
    "utils_global.StringToBool is deprecated. Use utils_global.text.StringToBool or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)
