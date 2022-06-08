import xml.etree.ElementTree as ET
import random
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
import re
import json

nltk.download("wordnet")
nltk.download("omw-1.4")

tree = ET.parse('ALL.data.xml')
# df = pd.read_csv("ALL.gold.key.txt", usecols=[0,1], delimiter=" ", header=None, names=["id", "wordnet"])
# df["wordnet"] = df["wordnet"].apply(lambda x: x.split("%")[0])
data = {'data': []}
count = 0
with open("toloka_data.json", 'w') as csvdata:
    for elem in tree.iter():
        if(elem.tag == "sentence"):
            wsd_words = []
            for words in elem.iter():
                if(words.tag == "instance"):
                    wsd_words.append(words)
            if len(wsd_words) > 0:
                # print(random.choice(wsd_words))
                string = ""
                for words in elem.iter():
                    if not words.get('pos') == ".":
                        string = string +  " " + words.text
                    else:
                        string = string + words.text
                sentence = string.lstrip()
                chosen_word = random.choice(wsd_words)
                chosen_word_text = chosen_word.text
                synsets = wn.synsets(chosen_word.get("lemma"))
                definitions = list(map(lambda x : x.definition(), synsets))
                if(len(synsets) < 11 and len(synsets) > 1):
                    data['data'].append({"id": count, "phrase": chosen_word_text, "sentence": sentence, "sense": definitions})
                    # csvdata.write("'" + sentence + "', '" + chosen_word_text + "', " + str(definitions) + "\n")
                    count = count + 1
    json_string = json.dumps(data)
    csvdata.write(json_string)
print(count)