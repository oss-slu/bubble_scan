import pytest
from io import BytesIO
from application.AppServer import app

# Fixture to initialize the Flask test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test case for uploading a Scantron sheet
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_upload_scantron(client):
    # Create a mock PDF file
    data = {
        'file': (BytesIO(b'PDF file content'), 'test_scantron.pdf'),
        'sheetType': 'scantron'
    }
    
    # Perform POST request to /api/upload
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')

    # Assert response status and message
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'file_id' in json_data

# Test case for uploading a custom sheet
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_upload_custom(client):
    # Create a mock PDF file
    data = {
        'file': (BytesIO(b'PDF file content'), 'test_custom.pdf'),
        'sheetType': 'custom'
    }
    
    # Perform POST request to /api/upload
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')

    # Assert that the response indicates custom sheets are not supported
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'custom_sheet'
    assert json_data['message'] == 'Custom sheets are not yet supported'
