"""
Module with decorators for logging function calls.
"""

import functools
from datetime import datetime
from typing import Callable, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., object])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Decorator to log function calls, results and errors.

    Args:
        filename: Optional filename to write logs to.
                 If not provided, logs will be printed to console.

    Returns:
        Decorated function with logging functionality.

    Examples:
        @log()
        def my_func(a, b):
            return a + b

        @log(filename="mylog.txt")
        def my_func(a, b):
            return a + b
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            # Prepare log message components
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                result = func(*args, **kwargs)
                log_message = f"{timestamp} - {func_name} ok\n"

                # Write to file or console
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")

                return result

            except Exception as e:
                error_type = type(e).__name__
                error_message = f"{timestamp} - {func_name} error: {error_type}. Inputs: {args}, {kwargs}\n"

                # Write to file or console
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")

                # Re-raise the exception
                raise

        return wrapper  # type: ignore

    return decorator
