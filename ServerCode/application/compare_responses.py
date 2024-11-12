"""compare_responses.py"""
import csv
import os
import logging

def compare_csv_files(student_responses_path, correct_answers_path, output_dir):
    """
    Compares student responses with correct answers and generates a result CSV file
    indicating the number of correct answers for each student.

    Parameters:
        student_responses_path (str): Path to the CSV file containing student responses.
        correct_answers_path (str): Path to the CSV file containing correct answers.
        output_dir (str): Directory to save the output result CSV file.

    Returns:
        str: Path to the generated result CSV file.
    """
    result_data = []
    try:
        # Read correct answers
        with open(correct_answers_path, mode='r', encoding='utf-8') as file:
            correct_answers = next(csv.DictReader(file))
            question_keys = list(correct_answers.keys())[1:]  # Skip the first column (e.g., studentID)

        # Read student responses and compare with correct answers
        with open(student_responses_path, mode='r', encoding='utf-8') as file:
            student_responses = csv.DictReader(file)
            for row in student_responses:
                student_id = row['studentID']
                correct_count = sum(1 for question in question_keys if row[question] == correct_answers[question])
                total_questions = len(question_keys)
                result_data.append({
                    'studentID': student_id,
                    'correct_answers': correct_count,
                    'total_questions': total_questions
                })

        # Save results to CSV
        result_csv_path = os.path.join(output_dir, 'comparison_results.csv')
        with open(result_csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['studentID', 'correct_answers', 'total_questions'])
            writer.writeheader()
            writer.writerows(result_data)

        logging.info("Comparison results saved to %s", result_csv_path)
        return result_csv_path

    except Exception as e:
        logging.error("Error comparing CSV files: %s", e)
        return None
