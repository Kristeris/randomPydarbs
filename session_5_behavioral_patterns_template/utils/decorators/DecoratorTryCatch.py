from loguru import logger # pip install loguru

def decorator_try_catch(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            print(exc)
            print("----")
            logger.exception(exc)
    return wrapper
