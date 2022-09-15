from typing import Iterable

from src.question import Question


def extract_questions(question_sheet) -> Iterable[Question]:
    for row in range(question_sheet.nrows):
        question_id = question_sheet.cell_value(rowx=row, colx=0)
        if question_id == '':
            continue

        possible_answers = _extract_possible_answers(question_sheet, row)
        correct_answers_indices = _extract_correct_answers(question_sheet, row)
        yield Question(
            wording=question_sheet.cell_value(rowx=row, colx=1),
            possible_answers=possible_answers,
            correct_answer_indices=correct_answers_indices
        )


def extract_fields(question):
    fields = [question.wording]
    for i, answer in enumerate(question.possible_answers):
        fields.append(f'{i + 1}. {answer}' if answer != '' else '')
    for i, answer in enumerate(question.possible_answers):
        if answer == '':
            field = ''
        else:
            answer = f'{i + 1}. {answer}'
            if i in question.correct_answer_indices:
                field = f'<p style="color:MediumSeaGreen;">{answer}</p>'
            else:
                field = f'<p style="color:Tomato;"><strike>{answer}</strike></o>'
        fields.append(field)
    return fields


def _extract_correct_answers(question_sheet, row):
    correct_answers_indices = []
    answer_index = 0
    correct_answers_start_column = 3
    row_length = question_sheet.row_len(0)
    for current_col in range(correct_answers_start_column, row_length, 2):
        points = question_sheet.cell_value(rowx=row, colx=current_col)
        if str(points).strip() == '':
            break
        if points > 0:
            correct_answers_indices.append(answer_index)
        answer_index += 1
    return correct_answers_indices


def _extract_possible_answers(question_sheet, row):
    possible_answers = []
    answers_start_column = 2
    for current_col in range(answers_start_column, question_sheet.row_len(row), 2):
        answer = question_sheet.cell_value(rowx=row, colx=current_col)
        possible_answers.append(str(answer))
    return possible_answers
