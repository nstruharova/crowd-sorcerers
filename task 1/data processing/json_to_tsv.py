import json

def parse_sense(sense):
    return ",".join([s.replace(',', '\,') for s in sense])

if __name__=='__main__':
    in_json = json.load(open("toloka_data.json", 'r'))

    out_file = open("toloka_data.tsv", 'w')

    out_file.write('INPUT:id\tINPUT:phrase\tINPUT:sentence\tINPUT:sense\n')

    for task in in_json['data']:
        out_file.write(f'{task["id"]}\t{task["phrase"]}\t{task["sentence"]}\t{parse_sense(task["sense"])}\n')

    out_file.close()

