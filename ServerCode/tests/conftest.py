"""
Test configuration module.
"""

import pytest

from application.app import create_app


@pytest.fixture
def app():

    """
    Fixture to set up the 'app' object for testing.

    Returns: 
        Flask App: The Flask application instance.
    """
    app = create_app("testing")

    return app
