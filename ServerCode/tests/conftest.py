import sys
import os

# Add the ServerCode directory (the parent directory of conftest.py) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the app from AppServer
from application.AppServer import app

import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
