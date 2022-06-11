# parse dataset, and fill in these variables for the whole group
import json
import random
# in_json = json.load(open("confusing_phrases.json", 'r'))


def get_wsd_data():
    return dict(
        phrase=PHRASE,
        sentence=SENTENCE,
        senses=random.shuffle(SENSES)  # randomize the order of senses for each player
    )


PHRASE = "This is the ambiguous word"
SENTENCE = "here is the sentence with the ambiguous word"
SENSES = [
    (0, "sense option 1"),
    (1, "sense option 2"),
    (2, "this is sense 3"),
]
GOLDEN = 1