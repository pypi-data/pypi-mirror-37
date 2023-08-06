from importlib import import_module

__version__ = "1.3.1"

parse = import_module(".parse", __name__)
commands = import_module(".commands", __name__)
