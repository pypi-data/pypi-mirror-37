import theano.tensor as T


def softmax(x, axis):
    e_x = T.exp(x - x.max(axis=axis, keepdims=True))
    result = e_x / e_x.sum(axis=axis, keepdims=True)
    return result

