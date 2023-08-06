from importlib import import_module

__version__ = "1.0.0"

usage_parser = import_module(".usage_parser", __name__)
application = import_module(".application", __name__)
utils = import_module(".utils", __name__)
