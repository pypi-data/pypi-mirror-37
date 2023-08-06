import os
from functools import wraps


def locked(f):
    @wraps(f)
    def func(*args, **kwargs):
        path = os.getenv("data_dir")
        file = os.path.join(path, 'eth.pid')

        if os.path.exists(file):
            return False
        try:
            with open(file, "w") as fp:
                fp.write('lock')

            f(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            os.unlink(file)


    return func





