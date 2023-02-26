from typing import Callable, Union, Type, Any


def safe_execute(func: Callable, *args, default_value: Any = None, **kwargs) -> Any:
    try:
        return func(*args, **kwargs)
    except:
        return default_value


def get_import_full_name(obj: Union[Type, Callable]) -> str:
    return ".".join([obj.__module__, obj.__name__])
