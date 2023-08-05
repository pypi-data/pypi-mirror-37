import numpy as np
import numpy
import theano
import theano.tensor as T
import cost
from softmax import softmax as softmax_t


eps = 0.00000000001


def crossentropy_loss(array, label):
    return  (label * np.log(array + eps), (1 - label) * np.log(1 - array + eps))


def softmax(arr, axis):
    exp = np.exp(arr - arr.max(axis=axis, keepdims=True))
    return exp / (exp.sum(axis=axis, keepdims=True)  + eps )


def custom_loss(i, acc, array, labels, static_idx, idx):
    idx_shape = idx.shape
    array_sorted = array[static_idx[0], static_idx[1], idx[:, i].reshape((idx_shape[0], 1, idx_shape[2]))]
    top = array_sorted[:,:,-2:]
    top_mean = top.mean(axis=-1)
    y = np.zeros_like(labels)
    y[:, i] = labels[:, i]
    pos, neg = crossentropy_loss(top_mean, labels)
    pos1, neg1 = crossentropy_loss(top_mean, y)
    tmp = (1 - y[:, i]) * (-neg1[:, i]) + y[:, i] * (-pos1 - neg1).sum(axis=1)
    return tmp.mean()

def process_np(array, labels):
    soft = array
    flattened = soft.reshape([array.shape[0], array.shape[1], np.prod(array.shape[-2:])])
    static_indices = numpy.indices(flattened.shape)
    argsort_idx = np.argsort(flattened, axis=-1)
    result = 0.0
    for i in range(labels.shape[1]):
        result += (custom_loss(i, 0.0, flattened, labels, static_indices, argsort_idx))
    return result

label_vals = np.array([[1, 0],
           [0, 1]])

val_big = np.array([[[[  2.23314574e+01,   2.12845429e-02],
         [  8.55700943e-01,   1.82172251e+00],
         [  2.57779020e+00,   2.46477683e+00]],

        [[  6.19017343e+00,   2.45660686e+01],
         [  1.77112686e+00,   5.55854171e+00],
         [  2.30523166e+01,   2.67572477e+01]]],


       [[[  9.39623229e+00,   5.52494000e+00],
         [  2.80388546e+01,   1.80280757e+01],
         [  9.43738114e+00,   1.04032077e+01]],

        [[  1.53984766e+00,   2.16774214e+00],
         [  2.09321060e+00,   1.84148443e+00],
         [  1.69082271e+00,   1.21573663e+00]]]])
label_small_vals = []
label_small_vals.append(np.array([[1, 0]]))
label_small_vals.append(np.array([[1,1]]))
label_small_vals.append(np.array([[1,1]]))


val_small = []
val_small.append( np.array([[[[0.999, 0.99],
                              [0.0, 0.0]],
                                     [[0.0, 0.0],
                                      [0.0, 0.0]]]]))

val_small.append(np.array([[[[ 0.999,  0.99 ],
                             [ 0.   ,  0.   ]], [[ 0.   ,  0.   ],
                                                [ 0.99 ,  0.9  ]]]]) )

val_small.append(np.array([[[[ 0.999,  0.99 ],
                             [ 0.   ,  0.   ]], [[ 0.95   ,  0.   ],
                                                [ 0.99 ,  0.9  ]]]]) )



static_indices = numpy.indices(val_small[0].shape)
import pdb;pdb.set_trace()
soft_b = softmax(val_big, axis=1)
res_b = process_np(soft_b, label_vals)
print(res_b)

m = theano.tensor.tensor4('m', dtype=theano.config.floatX)
m.tag.test_value = val_small[0].astype(theano.config.floatX)
label = theano.tensor.matrix('label', dtype='int32')
label.tag.test_value = label_small_vals[0].astype('int32')
#soft_m = softmax_t(m, axis=1)
soft_m = m
m_resh = soft_m.reshape((m.shape[0], m.shape[1], T.prod(m.shape[2:])))
index = theano.tensor.argsort(m_resh, axis=-1)


#test_loss = theano.function([m, label], outputs=[result], givens={ }, updates=updates)
result = cost.sortloss(m_resh, label, average=2)
test_loss = theano.function([m, label], outputs=[result], givens={ })
for i in range(len(val_small)):
    res0 = process_np(val_small[i], label_small_vals[i])
    print(res0)
    res1 = test_loss(val_small[i].astype(theano.config.floatX), label_small_vals[i].astype('int32'))
    print(res1[0])

