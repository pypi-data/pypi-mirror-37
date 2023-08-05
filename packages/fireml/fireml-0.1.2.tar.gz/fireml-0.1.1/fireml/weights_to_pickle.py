import sys

net_CAM = caffe.Net('forward.prototxt', models[os.getcwd()], caffe.TEST)
train_set = open('test1.txt', 'rt').readlines()
k = -1

params = net_CAM.params
weigths = dict()
for key in params.keys():
    weigths[key] = [x.data[...] for x in params[key]]
import pickle
pickle.dump(weigths, open('nin_acc_1.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
