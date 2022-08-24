import argparse
from dataclasses import dataclass
from typing import List

import genanki
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
            possible_answers.append(str(answer))

        # Correct answers
        correct_answers_indices = []
        answer_index = 0
        correct_answers_start_column = 3
        for current_col in range(correct_answers_start_column, question_sheet.row_len(current_row), 2):
            points = question_sheet.cell_value(rowx=row, colx=current_col)
            if str(points).strip() == '':
                break
            if points > 0:
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
    parser.add_argument('output_file_path')
    parser.add_argument('--sheet', default='QCM complet Français')
    args = parser.parse_args()

    workbook = xlrd.open_workbook(args.input_file_path)
    question_sheet = workbook.sheet_by_name(args.sheet)
    questions = _extract_questions(question_sheet)

    my_model = genanki.Model(
        1849442606,
        'FFVL QCM Model',
        fields=[
            {'name': 'Question'},
            {'name': 'PossibleAnswer1'},
            {'name': 'PossibleAnswer2'},
            {'name': 'PossibleAnswer3'},
            {'name': 'PossibleAnswer4'},
            {'name': 'CorrectedAnswer1'},
            {'name': 'CorrectedAnswer2'},
            {'name': 'CorrectedAnswer3'},
            {'name': 'CorrectedAnswer4'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<b>{{Question}}</b><br>' + '<br>'.join(['{{PossibleAnswer' + str(i) + '}}' for i in range(1, 5)]),
                'afmt': '<b>{{Question}}</b><hr id="answer"><br>' + '<br>'.join(['{{CorrectedAnswer' + str(i) + '}}' for i in range(1, 5)]) + '</ul>'
            },
        ]
    )

    my_deck = genanki.Deck(
        1929807668,
        'FFVL QCM Brevet Pilote'
    )
    for question in questions:
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
        my_deck.add_note(genanki.Note(model=my_model, fields=fields))

    genanki.Package(my_deck).write_to_file(args.output_file_path)


if __name__ == '__main__':
    _main()
