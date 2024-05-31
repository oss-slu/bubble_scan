import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import FileUploadComponent from './FileUploadComponent';
import '@testing-library/jest-dom';
import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

// Mock window.alert
window.alert = jest.fn();
// Spy on console.error
const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

// Define FileUploadComponentProps type
type FileUploadComponentProps = {
  downloadLink: string;
  // other properties...
};

// Your test cases
test('should not log any errors', () => {
    render(<FileUploadComponent />);
    expect(consoleErrorSpy).not.toHaveBeenCalled();
})

describe('FileUploadComponent', () => {
  it('renders without crashing', () => {
    render(<FileUploadComponent />);
  });

  it('displays success message when a valid PDF file is selected and submitted', async () => {
    fetchMock.mockResponseOnce(JSON.stringify({ status: 'success', file_id: '123' }));

    render(<FileUploadComponent />);
    const fileInput = screen.getByLabelText(/Upload File/i); // Case-insensitive label text match

    const pdfFile = new File(['PDF content'], 'test.pdf', {
      type: 'application/pdf',
    });

    fireEvent.change(fileInput, { target: { files: [pdfFile] } });
    fireEvent.click(screen.getByRole('button', { name: /Upload/i }));

    await waitFor(() =>
      expect(screen.getByText('File uploaded successfully!')).toBeInTheDocument()
    );
  });

  it('displays success message when CSV file is downloaded', async () => {
    fetchMock.mockResponseOnce(JSON.stringify({ status: 'success' }));

    const props: FileUploadComponentProps = {
      downloadLink: 'http://localhost:5001/api/download_csv/123'
    };

    render(<FileUploadComponent />);
    fireEvent.click(screen.getByRole('button', { name: /Download CSV/i }));

    await waitFor(() =>
      expect(screen.getByText('CSV file downloaded successfully!')).toBeInTheDocument()
    );
  });

  it('displays error message when file upload fails', async () => {
    fetchMock.mockRejectOnce(new Error('Upload failed'));

    render(<FileUploadComponent />);
    fireEvent.click(screen.getByRole('button', { name: /Upload/i }));

    await waitFor(() =>
      expect(screen.getByText('Error during file upload.')).toBeInTheDocument()
    );
  });
});
