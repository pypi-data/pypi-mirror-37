from flask import Flask
from .version import __version__

app = Flask(__name__)

import nuclei_viewer.main