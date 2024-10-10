import os
import pytest
from io import BytesIO
from application.AppServer import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.skip(reason="Skipping for now, needs fixing later")
def test_file_upload(client):
    # Use BytesIO to simulate file upload
    data = {
        'file': (BytesIO(b"Test PDF content"), 'test_file.pdf')
    }

    # Perform the file upload POST request
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)

    # Check the response status code
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['status'] == 'success'
    assert 'file_id' in response_data

    file_id = response_data['file_id']

    # Now perform the download CSV request
    download_response = client.get(f'/api/download_csv/{file_id}')

    # Log the response if it fails to help with debugging
    if download_response.status_code != 200:
        print(download_response.data)

    # Check the response for CSV
    assert download_response.status_code == 200
    assert download_response.mimetype == 'text/csv'


def test_valid_csv_acknowledgment(client):
    # First, upload a file
    data = {'file': (BytesIO(b"Test PDF content"), 'test_file.pdf')}
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    response_data = response.get_json()
    file_id = response_data['file_id']

    # Now, send acknowledgment with the valid file_id
    acknowledgment_response = client.post(f'/api/csv_acknowledgment/{file_id}')
    assert acknowledgment_response.status_code == 200
    assert acknowledgment_response.get_json()['status'] == 'success'
    
@pytest.mark.skip(reason="Skipping for now, needs fixing later")
def test_invalid_csv_acknowledgment(client):
    # Simulate an invalid file_id for acknowledgment
    invalid_file_id = "non_existent_file_id"
    acknowledgment_response = client.post(f'/api/csv_acknowledgment/{invalid_file_id}')
    assert acknowledgment_response.status_code == 404
    assert 'error' in acknowledgment_response.get_json()



def test_large_file_upload(client):
    # Simulate a large file upload
    large_data = BytesIO(b"a" * (10 * 1024 * 1024))  # 10MB file
    data = {
        'file': (large_data, 'large_file.pdf')
    }
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 200

@pytest.mark.skip(reason="Skipping for now, needs fixing later")
def test_invalid_file_upload(client):
    # Simulate an invalid file upload
    data = {
        'file': (BytesIO(b"Invalid content"), 'invalid_file.txt')
    }
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 400  # Assuming invalid file types return 400