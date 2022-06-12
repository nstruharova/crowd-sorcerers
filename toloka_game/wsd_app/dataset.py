# parse dataset, and fill in these variables for the whole group
import json
import random

PHRASE = 'example phrase'
SENTENCE = 'example sentence'
SENSES = ['example 1', 'example 2', 'example 3']
in_json = json.load(open('wsd_app/confusing_phrases.json', 'r'))

def get_wsd_data(idx):
    global SENSES
    PHRASE = in_json[idx]['phrase']
    SENTENCE = in_json[idx]['sentence']
    SENSES = in_json[idx]['sense']
    # print(PHRASE)
    # print(SENTENCE)
    print("we're in the get_wsd function")
    print(SENSES)
    return dict(
        phrase=PHRASE,
        sentence=SENTENCE,
        senses=SENSES  # randomize the order of senses for each player
    )


