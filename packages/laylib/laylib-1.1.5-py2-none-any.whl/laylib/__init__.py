

from laylib.environment import __version__ as _laylib_version
from laylib.environment import Environment
from laylib.default_engine import DefaultEngine
from laylib.resources import Resources

__author__ = 'Amardjia Amine'
__version__ = '1.1.5'

name = "laylib"

if __version__ != _laylib_version:
    raise Exception("Version number mismatch", __version__, _laylib_version)


__all__ = [

    # Modules:
    "default_engine", "resources", "util", "environment",
    # Public class
    "DefaultEngine", "Environment", "Resources"]
