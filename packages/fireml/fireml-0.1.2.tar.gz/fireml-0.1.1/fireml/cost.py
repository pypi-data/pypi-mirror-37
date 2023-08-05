import theano.tensor as T
import theano
import numpy


def negative_log_likelihood(p_y_given_x, y):
    # y.shape[0] is (symbolically) the number of rows in y, i.e.,
    # number of examples (call it n) in the minibatch
    # T.arange(y.shape[0]) is a symbolic vector which will contain
    # [0,1,2,... n-1] T.log(self.p_y_given_x) is a matrix of
    # Log-Probabilities (call it LP) with one row per example and
    # one column per class LP[T.arange(y.shape[0]),y] is a vector
    # v containing [LP[0,y[0]], LP[1,y[1]], LP[2,y[2]], ...,
    # LP[n-1,y[n-1]]] and T.mean(LP[T.arange(y.shape[0]),y]) is
    # the mean (across minibatch examples) of the elements in v,
    # i.e., the mean log-likelihood across the minibatch.
    return -T.mean(T.log(p_y_given_x)[T.arange(y.shape[0]), y])


epsilon = 0.00000001
def cross_entropy(p_y_given_x, y):
    """Return the mean of the negative log-likelihood of the prediction
    of this model under a given target distribution.
    """
    norm_low = T.switch(T.lt(p_y_given_x, epsilon), p_y_given_x + epsilon, p_y_given_x)
    norm_top = T.switch(T.lt(1 - norm_low, epsilon), norm_low - epsilon, norm_low)
    #return T.nnet.binary_crossentropy(norm_top, y).mean()
    return -T.mean(T.sum(y * T.log(p_y_given_x + epsilon) + (1 - y) * T.log(1 - p_y_given_x + epsilon), axis=1))


# todo: add to theano.tensor
def get_expanded_dim(a, i):
    index_shape = [1] * a.ndim
    index_shape[i] = a.shape[i]
    # it's a way to emulate
    # numpy.ogrid[0: a.shape[0], 0: a.shape[1], 0: a.shape[2]]
    index_val = T.arange(a.shape[i]).reshape(index_shape)
    return index_val


def sortloss(x, label, average):
    """
    crossentropy over max values in flattened feature maps

   Parameters
    ----------
    x : T.tensor3 - flattened feature maps of shape (batch, num_maps, map_size)
    label : T.matrix - labels for each feature map, shape (batch, num_maps)
    average: int - take that count of top values for computing loss
    """
    assert x.ndim == 3
    assert label.ndim == 2
    # todo: make simple sort into separate pooling mode
    def simple_sort():
        x_sorted = T.sort(x, axis=-1)
        x_sorted.name = 'x_sorted'
        top = x_sorted[:, :, -average:]
        top_mean = top.mean(axis=-1)
        # verify max equal with pool2d
        return cross_entropy(top_mean, label)
    return simple_sort()

    # todo: verify with max pooling and simple sort
    def custom_loss_theano(i, acc, array, labels, idx):
        stat_idx_0 = get_expanded_dim(array, 0)
        stat_idx_1 = get_expanded_dim(array, 1)
        sorting_idx = idx[:, i].reshape((idx.shape[0], 1, idx.shape[2]))
        array_sorted = array[stat_idx_0, stat_idx_1, sorting_idx]
        top = array_sorted[:, :, -average:]
        top_mean = top.mean(axis=-1)
        p_y_given_x = top_mean
        y_fix = T.zeros_like(labels)
        y = T.set_subtensor(y_fix[:, i], labels[:, i])
        pos_elwise = y * T.log(p_y_given_x + epsilon)
        neg_elwise = (1 - y) * T.log(1 - p_y_given_x + epsilon)
        # using both positive and negative part would result in
        # inforcing that some class is present somewere where maximum for absent class is
        # 1) function should enforce absence of all other classes for current positive y[:, i]
        # 2) enforce only absence of target in case of y[:, i] == 0
        tmp = T.switch(T.lt(y[:, i], epsilon), -neg_elwise[:, i], -T.mean(pos_elwise + neg_elwise, axis=1))
        return acc + tmp.mean()
    index = theano.tensor.argsort(x, axis=-1)
    result, updates = theano.scan(fn=custom_loss_theano,
                              outputs_info=T.as_tensor_variable(getattr(numpy, theano.config.floatX)(0.0)),
                              sequences=[T.arange(x.shape[1])],
                              non_sequences=[x, label, index])
    return result[-1]


def accuracy(x, label):
    assert (x.ndim == label.ndim)
    assert (x.ndim == 2)
    thres = x > 0.5
    eq = T.all(T.eq(thres, label), axis=1)
    eq.name = "equal_label"
    accuracy = T.mean(eq)
    return accuracy


def cross_entropy_test():
    import numpy as np
    o = T.imatrix('o')
    W = T.matrix('W', dtype=theano.config.floatX)
    b = T.vector('b', dtype=theano.config.floatX)
    x = T.vector('x', dtype=theano.config.floatX)
    y = T.nnet.softmax(T.dot(W, x) + b)
    cost = T.nnet.categorical_crossentropy(y, o)
    cost1 = -T.mean(T.mean(o * T.log(y) + (1 - o) * T.log(1 - y)))
    f = theano.function(inputs=[x, W, b, o], outputs=[cost])
    f1 = theano.function(inputs=[x, W, b, o], outputs=[cost1])
    vo = np.asarray([1, 0, 1]).reshape((1,3))
    vW = [[0.4, 0.1], [0.9, -0.7], [-1.2, 0.34]]
    vx = [0.2, 0.3]
    vb = [1, 1, 1]
    f(vx, vW, vb, vo)   # = [array([ 2.19690657])]
    f1(vx, vW, vb, vo)  # = [array(0.8648481002783766)]
    y_out = y.eval({W: vW, x:vx, b:vb})
    -(vo * np.log(y_out)).sum()                                  # = 2.19690657
    -(vo * np.log(y_out) + (1 - vo) * np.log(1 - y_out)).mean()  #  = 0.
