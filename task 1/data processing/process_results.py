from cmath import isnan
import pandas

if __name__=='__main__':
    data=pandas.read_csv('results/res_not_banned.tsv',sep='\t')
    
    answers = {}

    for i in range(len(data['INPUT:id'])):
        if pandas.isna(data['INPUT:id'][i]):
            continue
    
        id = int(data['INPUT:id'][i])
        ans = data['OUTPUT:answer'][i]

        if id not in answers:
            answers[id] = {}
        if ans not in answers[id]:
            answers[id][ans] = 0
        answers[id][ans] += 1
    
    nums = {}
    for ans in answers:
        nums[ans] = sorted([answers[ans][i] for i in answers[ans]])
    
    print('done')
