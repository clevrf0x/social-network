import os

class EnvVariableNotFoundError(Exception):
    """Exception raised when an environment variable is not found."""
    def __init__(self, key: str):
        self.key = key
        self.message = f"Environment variable '{key}' is not set."
        super().__init__(self.message)

def unsafe_get_env(key: str) -> str:
    """
    Retrieves an environment variable's value or raises an exception if not found.

    This function is unsafe for use in views or non-critical environments, as it
    raises an exception when the variable is missing. Use only in critical contexts.

    Args:
        key (str): Environment variable name.

    Returns:
        str: The value of the environment variable.

    Raises:
        EnvVariableNotFoundError: If the environment variable is not set.
    """
    value = os.getenv(key)
    if value is None:
        raise EnvVariableNotFoundError(key)
    
    return value
