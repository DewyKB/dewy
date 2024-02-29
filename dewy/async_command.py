import asyncio
from functools import wraps

def async_command(f):
    """Decorator for creating async commands.

    Based on https://github.com/pallets/click/issues/85#issuecomment-503464628.

    Examples
    --------

    ::

        @click.command()
        @async_command
        async def command_name():
            pass
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper