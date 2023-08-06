# See http://peak.telecommunity.com/DevCenter/setuptools
try:
     __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
     from pkgutil import extend_path
     __path__ = extend_path(__path__, __name__)

import os

with open(os.path.join(os.path.join(os.path.dirname(__file__), "version.txt"))) as f:
    __version__ = f.read().strip()

if __name__ == '__main__':
    print(__version__)
