"""
    Application configuation.
"""

import os


# Database location
DATABASE_URI = 'sqlite:///catalog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'super_secret_key'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

