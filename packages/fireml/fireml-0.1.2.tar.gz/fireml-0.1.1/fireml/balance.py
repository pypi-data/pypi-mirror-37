import random
train_f = open('train.txt', 'rt').readlines()


test_f = open('test.txt', 'rt').readlines()

from collections import defaultdict

test_set = defaultdict(list)

train_set = defaultdict(list)

def process_set(d, items):
    for item in items:
        value, key = item.strip().split()
        d[key].append(value)


    max_num = 0
    index = -1
    for i, value in enumerate(d.values()):
        num = len(value)
        if max_num < num:
           max_num = num
           index = i
    for key in d.keys():
        while len(d[key]) < max_num:
            d[key].append(random.choice(d[key]))

def write_set(path, d):
    with open(path, 'wt') as f:
        for key, value in d.items():
            for item in value:
                f.write('{0} {1}\n'.format(item, key))

process_set(train_set, train_f)
write_set('train_balanced.txt', train_set)


process_set(test_set, test_f)
write_set('test_balanced.txt', test_set)

