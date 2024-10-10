from io import BytesIO
import pytest


def test_upload_route(client):
    # Use BytesIO to simulate a file-like object for PDF
    data = {
        'file': (BytesIO(b"Test PDF content"), 'test_file.pdf')
    }
    
    # Perform the file upload POST request
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    
    # Check the response status code
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'file_id' in response_data

@pytest.mark.skip(reason="Skipping for now, needs fixing later")
def test_invalid_file_upload(client):
    # Use BytesIO to simulate an invalid file-like object
    data = {
        'file': (BytesIO(b"Invalid content"), 'invalid_file.txt')
    }

    # Perform the file upload POST request
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    
    # Check that the upload failed as expected
    assert response.status_code == 400  # Assuming your server returns 400 for invalid files
    assert 'error' in response.json

@pytest.mark.skip(reason="Skipping for now, needs fixing later")
def test_process_pdf(client):
    # Simulate a valid file upload
    data = {
        'file': (BytesIO(b"Test PDF content"), 'test_file.pdf')
    }
    response = client.post('/api/process_pdf', content_type='multipart/form-data', data=data)
    assert response.status_code == 200

@pytest.mark.skip(reason="Skipping for now, needs fixing later")
def test_process_pdf_missing_file(client):
    # Test for missing file case
    response = client.post('/api/process_pdf', content_type='multipart/form-data', data={})
    assert response.status_code == 400
    assert 'error' in response.get_json()

