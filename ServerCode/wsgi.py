"""
Module docstring goes here
"""
import os

from application.app import create_app

os.environ.setdefault('FLASK_CONFIG', 'development')
app = create_app(os.environ["FLASK_CONFIG"])
