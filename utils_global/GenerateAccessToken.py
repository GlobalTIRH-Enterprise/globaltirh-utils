import warnings
from utils_global.gcp.auth.GenerateAccessToken import generate_access_token

warnings.warn(
    "utils_global.GenerateAccessToken is deprecated. Use utils_global.gcp.auth.GenerateAccessToken or import directly from utils_global.",
    DeprecationWarning,
    stacklevel=2
)
