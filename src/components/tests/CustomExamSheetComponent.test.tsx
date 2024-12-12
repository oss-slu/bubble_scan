import { render, screen, fireEvent } from "@testing-library/react";
import CustomExamSheetComponent from "../CustomExamSheetComponent";
import "@testing-library/jest-dom";

beforeEach(() => {
  // Mock window.alert
  jest.spyOn(window, "alert").mockImplementation(() => {});

  // Mock window.open
  Object.defineProperty(window, "open", {
    writable: true,
    value: jest.fn(() => ({
      document: {
        write: jest.fn(),
        close: jest.fn(),
      },
      focus: jest.fn(),
      print: jest.fn(),
    })),
  });
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe("CustomExamSheetComponent", () => {
  test("should render the form with required inputs and buttons", () => {
    render(<CustomExamSheetComponent />);
    expect(screen.getByLabelText(/Exam Title:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Number of Questions:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Number of Answer Options:/i)).toBeInTheDocument();
    expect(screen.getByText(/Generate Exam Sheet/i)).toBeInTheDocument();
    expect(screen.getByText(/Print Stored Exam/i)).toBeInTheDocument();
  });

  test("should allow the user to input exam title, number of questions, and number of answer options", () => {
    render(<CustomExamSheetComponent />);
    const titleInput = screen.getByLabelText(/Exam Title:/i);
    const questionsInput = screen.getByLabelText(/Number of Questions:/i);
    const optionsInput = screen.getByLabelText(/Number of Answer Options:/i);

    fireEvent.change(titleInput, { target: { value: "Math Test" } });
    fireEvent.change(questionsInput, { target: { value: "10" } });
    fireEvent.change(optionsInput, { target: { value: "4" } });

    expect(titleInput).toHaveValue("Math Test");
    expect(questionsInput).toHaveValue(10);
    expect(optionsInput).toHaveValue(4);
  });

  test("should generate exam content when the form is submitted", () => {
    render(<CustomExamSheetComponent />);
    const titleInput = screen.getByLabelText(/Exam Title:/i);
    const questionsInput = screen.getByLabelText(/Number of Questions:/i);
    const optionsInput = screen.getByLabelText(/Number of Answer Options:/i);
    const submitButton = screen.getByText(/Generate Exam Sheet/i);

    fireEvent.change(titleInput, { target: { value: "Math Exam" } });
    fireEvent.change(questionsInput, { target: { value: "5" } });
    fireEvent.change(optionsInput, { target: { value: "4" } });
    fireEvent.click(submitButton);

    const storedExam = localStorage.getItem("storedExam");
    expect(storedExam).not.toBeNull();
    expect(storedExam).toContain("Math Exam");
  });

  test("should alert if no stored exam is found when the print button is clicked", () => {
    render(<CustomExamSheetComponent />);
    const printButton = screen.getByText(/Print Stored Exam/i);

    // Ensure localStorage is empty
    localStorage.clear();

    fireEvent.click(printButton);

    // Debugging to ensure mock works
    console.log((window.alert as jest.Mock).mock.calls);

    expect(window.alert).toHaveBeenCalledWith("No stored exam found.");
  });
});
