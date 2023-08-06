from importlib import import_module

version = "1.1.1"

parse = import_module(".parse", __name__)
commands = import_module(".commands", __name__)
