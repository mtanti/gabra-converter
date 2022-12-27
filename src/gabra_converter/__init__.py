'''
Ġabra Extractor top level package.
'''

import os
import pkg_resources

__version__ = pkg_resources.resource_string(
    'gabra_converter',
    'version.txt',
).decode()

path = os.path.dirname(os.path.abspath(__file__))
