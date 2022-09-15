import genanki


def create_anki_model(model_id: int) -> genanki.Model:
    return genanki.Model(
        model_id,
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
                'qfmt': '<b>{{Question}}</b><br>' + '<br>'.join(
                    ['{{PossibleAnswer' + str(i) + '}}' for i in range(1, 5)]),
                'afmt': '<b>{{Question}}</b><hr id="answer"><br>' + '<br>'.join(
                    ['{{CorrectedAnswer' + str(i) + '}}' for i in range(1, 5)]) + '</ul>'
            },
        ]
    )


def create_anki_deck(deck_id: int) -> genanki.Deck:
    return genanki.Deck(
        deck_id,
        'FFVL QCM Brevet Pilote'
    )
