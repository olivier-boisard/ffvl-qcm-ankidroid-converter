import argparse

import genanki
import xlrd

from src.anki_utils import create_anki_model, create_anki_deck
from src.extraction import extract_questions, extract_fields


def _main():
    # Get input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path')
    parser.add_argument('output_file_path')
    parser.add_argument('--sheet', default='QCM complet Français')
    args = parser.parse_args()

    # Define constant parameters
    model_id = 1849442606
    deck_id = 1929807668

    # Run process
    workbook = xlrd.open_workbook(args.input_file_path)
    question_sheet = workbook.sheet_by_name(args.sheet)
    questions = extract_questions(question_sheet)
    model = create_anki_model(model_id)
    deck = create_anki_deck(deck_id)
    for question in questions:
        fields = extract_fields(question)
        deck.add_note(genanki.Note(model=model, fields=fields))

    genanki.Package(deck).write_to_file(args.output_file_path)


if __name__ == '__main__':
    _main()
