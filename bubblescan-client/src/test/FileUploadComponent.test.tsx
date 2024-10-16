import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import FileUploadComponent from "./../components/FileUploadComponent";

describe('FileUploadComponent', () => {
  it('renders file input', () => {
    render(<FileUploadComponent />);
    const fileInput = screen.getByLabelText(/exampleScans.pdf/i);
    expect(fileInput).toBeInTheDocument();
  });

  it('uploads a file', () => {
    render(<FileUploadComponent />);
    const fileInput = screen.getByLabelText(/exampleScans.pdf/i);
    
    const file = new File(['dummy content'], 'example.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [file] } });

    expect(fileInput.files[0]).toEqual(file);
    expect(fileInput.files).toHaveLength(1);
  });

  it('displays error message for non-PDF files', () => {
    render(<FileUploadComponent />);
    const fileInput = screen.getByLabelText(/exampleScans.pdf/i);
    
    const file = new File(['dummy content'], 'example.txt', { type: 'text/plain' });
    fireEvent.change(fileInput, { target: { files: [file] } });

    const errorMessage = screen.getByText(/Only PDF files are allowed/i);
    expect(errorMessage).toBeInTheDocument();
  });
});
