from __future__ import print_function as _

import os
import sys
import json

import dash

from ._imports_ import *
from ._imports_ import __all__

__version__ = '0.0.0'

if not hasattr(dash, 'development'):
    print('Dash was not successfully imported. '
          'Make sure you don\'t have a file '
          'named \n"dash.py" in your current directory.', file=sys.stderr)
    sys.exit(1)

package_name = __name__.split('.')[-1]
current_path = os.path.dirname(os.path.abspath(__file__))
components = dash.development.component_loader.load_components(
    os.path.join(current_path, 'metadata.json'),
    __name__
)

_this_module = sys.modules[__name__]

_js_dist = [
    {
        'relative_package_path': '{}.min.js'.format(package_name),
        'namespace': __name__
    }
]

_css_dist = [
    {
        'relative_package_path': '{}.css'.format(package_name),
        'namespace': __name__
    }
]

for _component in components:
    setattr(_this_module, _component.__name__, _component)
    setattr(_component, '_js_dist', _js_dist)
    setattr(_component, '_css_dist', _css_dist)
