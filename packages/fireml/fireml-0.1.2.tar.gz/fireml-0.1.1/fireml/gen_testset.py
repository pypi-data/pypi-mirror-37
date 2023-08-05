from collections import defaultdict
from sklearn.cross_validation import train_test_split


lines = open('train.txt', 'r').readlines()
lines = [x.strip().split('.jpg') for x in lines]

data = defaultdict(list)
for item in lines:
    image, label = item[0] + '.jpg', int(item[1].strip())
    data[label].append(image)


data_train = defaultdict(list)
data_test = defaultdict(list)

for i in data.keys():
    x_train, x_test, y_train, y_test = train_test_split(data[i], [i] * len(data[i]), test_size=0.1)
    data_train[i].extend(x_train)
    data_test[i].extend(x_test)


with open('new_train.txt', 'wt') as f:
    for i in data_train.keys():
        for image in data_train[i]:
            f.write('{0} {1}\n'.format(image, i))

with open('new_test.txt', 'wt') as f:
    for i in data_test.keys():
        for image in data_test[i]:
            f.write('{0} {1}\n'.format(image, i))

