"""
Extract information from wheels

``wheel-inspect`` examines Python wheel files and outputs various information
about the contents within as JSON-serializable objects.  It can be invoked in
Python code as::

    from wheel_inspect import inspect_wheel

    output = inspect_wheel(path_to_wheel_file)

or from the command line with the ``wheel2json`` command.

Visit <https://github.com/jwodder/wheel-inspect> for more information.
"""

from .inspect import inspect_wheel
from .schema  import SCHEMA

__version__      = '1.0.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'wheel-inspect@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/wheel-inspect'

__all__ = [
    'SCHEMA',
    'inspect_wheel',
]
