import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './../App';

describe('App Component', () => {
  it('renders the welcome message', () => {
    render(<App />);
    const welcomeMessage = screen.getByText(/Welcome to Bubble Scan/i);
    expect(welcomeMessage).toBeInTheDocument();
  });

  it('renders upload button', () => {
    render(<App />);
    const uploadButton = screen.getByRole('button', { name: /Upload/i });
    expect(uploadButton).toBeInTheDocument();
  });

  it('renders custom sheet creation button', () => {
    render(<App />);
    const customSheetButton = screen.getByRole('button', { name: /Custom Sheet/i });
    expect(customSheetButton).toBeInTheDocument();
  });
});
