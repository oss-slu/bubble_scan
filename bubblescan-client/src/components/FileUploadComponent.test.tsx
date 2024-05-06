import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FileUploadComponent from "./FileUploadComponent";
import "@testing-library/jest-dom";

describe("FileUploadComponent", () => {
  beforeEach(() => {
    jest.resetAllMocks(); // Clear mocks before each test
  });

  it("should allow a PDF file to be selected", () => {
    render(<FileUploadComponent />);
    const input = screen.getByLabelText(/upload/i) as HTMLInputElement;
    const file = new File(["pdf content"], "test.pdf", {
      type: "application/pdf",
    });
    userEvent.upload(input, file);
    if (input.files) {
      expect(input.files[0]).toStrictEqual(file);
      expect(input.files.item(0)).toStrictEqual(file);
      expect(input.files).toHaveLength(1);
    } else {
      throw new Error("The file list is null");
    }
  });

  it("should give an alert when a non-PDF file is selected", () => {
    jest.spyOn(window, "alert").mockImplementation(() => {});
    render(<FileUploadComponent />);
    const input = screen.getByLabelText(/upload/i) as HTMLInputElement;
    const file = new File(["content"], "test.png", { type: "image/png" });
    userEvent.upload(input, file);
    expect(window.alert).toHaveBeenCalledWith("Please select a PDF file.");
  });

  it("should handle form submission with a selected PDF file", async () => {
    const mockFetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ status: "success", file_id: "123" }),
        headers: new Headers(),
        redirected: false,
        status: 200,
        statusText: "OK",
        type: "basic",
        url: "",
      })
    ) as jest.Mock;

    global.fetch = mockFetch;
    render(<FileUploadComponent />);
    const file = new File(["pdf content"], "test.pdf", {
      type: "application/pdf",
    });
    const input = screen.getByLabelText(/upload/i) as HTMLInputElement;
    userEvent.upload(input, file);
    const submitButton = screen.getByRole("button", { name: /upload/i });
    userEvent.click(submitButton);
    await screen.findByText(/file uploaded successfully!/i);
    expect(mockFetch).toHaveBeenCalledTimes(1);
  });

  it("should enable the download CSV button after successful upload", async () => {
    const mockFetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ status: "success", file_id: "123" }),
        headers: new Headers(),
        redirected: false,
        status: 200,
        statusText: "OK",
        type: "basic",
        url: "",
      })
    ) as jest.Mock;

    global.fetch = mockFetch;
    render(<FileUploadComponent />);
    const file = new File(["pdf content"], "test.pdf", {
      type: "application/pdf",
    });
    const input = screen.getByLabelText(/upload/i) as HTMLInputElement;
    userEvent.upload(input, file);
    const submitButton = screen.getByRole("button", { name: /upload/i });
    userEvent.click(submitButton);
    await screen.findByText(/file uploaded successfully!/i);
    const downloadButton = screen.getByRole("button", {
      name: /download csv/i,
    });
    expect(downloadButton).toBeEnabled();
  });

  it("should clear the form and reset states when the clear button is clicked", () => {
    render(<FileUploadComponent />);
    const clearButton = screen.getByRole("button", { name: /clear/i });
    userEvent.click(clearButton);
    expect(screen.queryByLabelText(/upload/i)).toBeNull();
  });
});
