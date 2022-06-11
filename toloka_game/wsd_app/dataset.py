# parse dataset, and fill in these variables for the whole group
import json

# in_json = json.load(open("toloka_data.json", 'r'))


def get_wsd_data():
    return dict(
        phrase=PHRASE,
        sentence=SENTENCE,
        senses=SENSES
    )

PHRASE = "This is the ambiguous word"
SENTENCE = "here is the sentence with the ambiguous word"
SENSES = [
    (0, "sense option 1"),
    (1, "sense option 2"),
    (2, "this is sense 3"),
]
GOLDEN = 1