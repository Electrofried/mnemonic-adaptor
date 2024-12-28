"""
Utility modules for text processing, file operations, and API interactions.
"""

from functools import wraps
from typing import Callable, Any

def utils(func: Callable) -> Callable:
    """
    Decorator to mark utility functions and provide consistent error handling.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Utility error in {func.__name__}: {str(e)}")
            raise
    return wrapper 