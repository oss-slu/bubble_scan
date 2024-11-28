# compare_responses.py
import csv
import os
import logging

def compare_csv_files(student_responses_path, correct_answers_path, output_dir):
    """
    Compares student responses with correct answers row-by-row (sequentially) and generates a result CSV file.
    Parameters:
        student_responses_path (str): Path to the CSV file containing student responses.
        correct_answers_path (str): Path to the CSV file containing correct answers.
        output_dir (str): Directory to save the output result CSV file.
    Returns:
        str: Path to the generated result CSV file.
    """
    result_data = []
    total_correct_answers = 0
    total_questions_all = 0

    try:
        # Read correct answers
        with open(correct_answers_path, mode='r', encoding='utf-8') as file:
            correct_answers_reader = list(csv.reader(file))
            correct_answers_headers = correct_answers_reader[0]  # Titles (first row)
            correct_answers_rows = correct_answers_reader[1:]    # Data (remaining rows)

        # Read student responses
        with open(student_responses_path, mode='r', encoding='utf-8') as file:
            student_responses_reader = list(csv.reader(file))
            student_responses_headers = student_responses_reader[0]  # Titles (first row)
            student_responses_rows = student_responses_reader[1:]    # Data (remaining rows)

        # Ensure the headers are consistent between files
        if correct_answers_headers != student_responses_headers:
            logging.error("Mismatch in headers between ground truth and student responses.")
            return None

        # Ensure the number of rows match
        if len(correct_answers_rows) != len(student_responses_rows):
            logging.error("Mismatch in number of rows between ground truth and student responses.")
            return None

        # Compare row-by-row
        for i, (correct_row, student_row) in enumerate(zip(correct_answers_rows, student_responses_rows), start=2):
            correct_count = 0
            total_questions = len(correct_answers_headers)

            # Compare answers question by question
            for question_idx in range(len(correct_row)):
                # Normalize and handle multiple answers
                correct_answer = correct_row[question_idx].strip().upper()
                student_answer = student_row[question_idx].strip().upper()

                # Split answers for multi-answer questions
                correct_answers_set = set(correct_answer.split('|'))
                student_answers_set = set(student_answer.split('|'))

                # Check for intersection of answers
                if student_answers_set & correct_answers_set:
                    correct_count += 1

            # Calculate row accuracy
            accuracy = round((correct_count / total_questions) * 100, 2)

            # Append results for this row
            result_data.append({
                'row': i,  # Row number starting from 2
                'correct_answers': correct_count,
                'total_questions': total_questions,
                'accuracy': accuracy
            })

            # Update totals for overall accuracy calculation
            total_correct_answers += correct_count
            total_questions_all += total_questions

        # Calculate overall accuracy
        overall_accuracy = round((total_correct_answers / total_questions_all) * 100, 2)

        # Save results to CSV, including overall accuracy
        result_csv_path = os.path.join(output_dir, 'comparison_results.csv')
        os.makedirs(output_dir, exist_ok=True)
        with open(result_csv_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['row', 'correct_answers', 'total_questions', 'accuracy']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result_data)

            # Add overall accuracy row at the end of the CSV
            writer.writerow({
                'row': 'Overall',
                'correct_answers': total_correct_answers,
                'total_questions': total_questions_all,
                'accuracy': overall_accuracy
            })

        logging.info(f"Comparison results saved to {result_csv_path}")
        return result_csv_path

    except Exception as e:
        logging.error("Error comparing CSV files: %s", e)
        return None

if __name__ == "__main__":
    student_responses_file = "inputData/student_responses.csv"
    correct_answers_file = "inputData/bubblescan_answers_50.csv"
    output_directory = "inputData/"
    result_csv_path = compare_csv_files(student_responses_file, correct_answers_file, output_directory)
    if result_csv_path:
        print(f"Comparison results saved to: {result_csv_path}")
    else:
        print("Error comparing CSV files")