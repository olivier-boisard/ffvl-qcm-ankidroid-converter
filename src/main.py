import argparse
from dataclasses import dataclass
from typing import List

import xlrd


@dataclass
class Question:
    wording: str
    possible_answers: List[str]
    correct_answer_indices: List[int]


def _extract_questions(question_sheet):
    current_row = 0
    for row in range(question_sheet.nrows):
        question_id = question_sheet.cell_value(rowx=row, colx=0)
        if question_id == '':
            continue

        # Get all answers
        possible_answers = []
        answers_start_column = 2
        for current_col in range(answers_start_column, question_sheet.row_len(row), 2):
            answer = question_sheet.cell_value(rowx=row, colx=current_col)
            possible_answers.append(answer)

        # Correct answers
        correct_answers_indices = []
        answer_index = 0
        correct_answers_start_column = 3
        for current_col in range(correct_answers_start_column, question_sheet.row_len(current_row), 2):
            points = question_sheet.cell_value(rowx=row, colx=current_col)
            if str(points).strip() == '':
                break
            if points < 0:
                correct_answers_indices.append(answer_index)
            answer_index += 1

        # Build question
        yield Question(
            wording=question_sheet.cell_value(rowx=row, colx=1),
            possible_answers=possible_answers,
            correct_answer_indices=correct_answers_indices
        )


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path')
    parser.add_argument('--sheet', default='QCM complet Français')
    args = parser.parse_args()

    workbook = xlrd.open_workbook(args.input_file_path)
    question_sheet = workbook.sheet_by_name(args.sheet)
    questions = _extract_questions(question_sheet)

    questions


if __name__ == '__main__':
    _main()
