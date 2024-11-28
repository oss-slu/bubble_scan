"""Tests for the Flask application."""
from io import BytesIO
from .AppServer import app
import pytest

# Fixture to initialize the Flask test client
@pytest.fixture(name="test_client")
def flask_test_client():
    """Set up test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test case for uploading a Scantron sheet
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_upload_scantron(test_client):
    """Test upload function."""
    # Create a mock PDF file
    data = {
        'file': (BytesIO(b'PDF file content'), 'test_scantron.pdf'),
        'sheetType': 'scantron'
    }
    
    # Perform POST request to /api/upload
    response = test_client.post('/api/upload', data=data, content_type='multipart/form-data')

    # Assert response status and message
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'file_id' in json_data

# Test case for uploading a custom sheet
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_upload_custom(test_client):
    """Test Custom Sheet upload."""
    data = {
        'file': (BytesIO(b'PDF file content'), 'test_custom.pdf'),
        'sheetType': 'custom'
    }
    
    # Perform POST request to /api/upload
    response = test_client.post('/api/upload', data=data, content_type='multipart/form-data')

    # Assert that the response indicates custom sheets are not supported
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'custom_sheet'
    assert json_data['message'] == 'Custom sheets are not yet supported'
