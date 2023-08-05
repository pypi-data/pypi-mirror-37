import theano
theano.config.exception_verbosity='high'
import theano.tensor as T
import numpy
import numpy as np
import scipy as sp

from fireml import fire_pb2
from fireml import weight_filler
from fireml import learning
from fireml import mlp


def get_shared(rng,  n_in, n_out, connectivity, sparse=False):
    if connectivity is None:
        connectivity = numpy.diag()
    tmp = np.asarray(
                rng.uniform(low=-W_bound, high=W_bound, size=(n_out, n_in),
                dtype=theano.config.floatX))
    if sparse:
        assert(connectivity is not None)
        shape = tmp.shape
        if shape[0] > shape[1]:
            tmp = sp.csc_matrix(tmp * connectivity)
        else:
            tmp = sp.csr_matrix(tmp * connectivity)
    if connectivity is None:
        return theano.shared(tmp, borrow=True)
    # todo: check if need to multiply symbolic variable
    return theano.shared(tmp * connectivity, borrow=True) * connectivity


class LstmLayer():
    """
    LSTM vanilla block as defined in "LSTM: A Search Space Odyssey(Klaus Greff, Rupesh K. Srivastava,
                                                 Jan Koutnı́k, Bas R. Steunebrink, Jürgen Schmidhuber)
    """
    def __init__(self, n_in, n_out, weight_filler, activation,
                 input_connectivity_matrix=None,
                 recurrent_connectivity_matrix=None):
        """
        connectivity_matrix:  len(output) x len(input) matrix
        """
        self.activation = activation
        self.weight_filler = weight_filler

        # Input weighs for input, and gates: input, forget, output
        # shape is #neurons x len(x)
        # input -> input
        self.W_zi = self.init_weights(n_in, n_out)
        #  input -> input gate
        self.W_xi = self.init_weights(n_in, n_out)
        #  input -> forget gate
        self.W_xf = self.init_weights(n_in, n_out)
        # input -> output gate
        self.W_xo = self.init_weights(n_in, n_out)

        # recurrent connections
        # output_{t-1} -> cell
        self.Rz = self.init_weights(n_out, n_out)
        # output_{t-1} -> output gate
        self.Ro = self.init_weights(n_out, n_out)
        # output_{t-1} -> input gate
        self.Ri = self.init_weights(n_out, n_out)
        # output_{t-1} -> forgate gate
        self.Rf = self.init_weights(n_out, n_out)

        # diagonal(peephole) connections for gates
        # hid -> input gate
        self.w_ci = self.init_weights(n_out, n_out, True)
        # hid -> output gate
        self.w_co = self.init_weights(n_out, n_out, True)
        # hid -> forget gate
        self.w_cf = self.init_weights(n_out, n_out, True)

        # the bias is a 1D tensor -- one bias per output
        b_values = numpy.zeros((n_out,), dtype=theano.config.floatX)
        # input bias and gates bias: input, forget, output
        self.b_z = theano.shared(value=b_values, borrow=False)
        self.b_i = theano.shared(value=b_values, borrow=False)
        self.b_f = theano.shared(value=b_values, borrow=False)
        self.b_o = theano.shared(value=b_values, borrow=False)
        self.weights = [self.W_xf, self.W_xi, self.W_xo, self.W_zi,
                        self.Rz, self.Rf, self.Ri, self.Ro,
                        self.b_f, self.b_i, self.b_o, self.b_z]

    def init_weights(self, n_in, n_out, peephole=False):
        self.weight_filler.n_in = n_in
        self.weight_filler.n_out = n_out
        if peephole:
            weights = self.weight_filler.generate_weights((n_out,))
        else:
            weights = self.weight_filler.generate_weights((n_in, n_out))
        return theano.shared(weights, borrow=True)

    def forward(self, x_t, hid_prev, out_prev):
        # block input
        # z = σ(Wz xt + Rz yt−1 + bz)
        z = self.activation(x_t.dot(self.W_zi) + out_prev.dot(self.Rz) + self.b_z)

        # input gate
        # it = σ(Wi xt + Ri yt−1 +  ci * ct−1 + bi)
        it = self.activation(x_t.dot(self.W_xi) + out_prev.dot(self.Ri) + self.w_ci * hid_prev + self.b_i)

        # forget gate
        # ft = σ (Wxf xt + Rf yt−1 + cf * ct−1 + bf )
        ft = self.activation(x_t.dot(self.W_xf) + out_prev.dot(self.Rf) + self.w_cf * hid_prev + self.b_f)

        # cell(t) vector
        # ct = ft * ct−1 + it * z
        ct = it * z + ft * hid_prev

        # output gate
        # ot = σ (Wx xt + Ro yt−1 + co ct + bo )
        ot = self.activation(x_t.dot(self.W_xo) + out_prev.dot(self.Ro) + self.w_co * ct + self.b_o)
        # cell output vector
        # yt = h(ct) * ot
        yt = self.activation(ct) * ot
        return ct, yt


def gen_index(i, items_per_layer=2):
    """
    Returns slice for getting elements from list
    """
    pos = i * items_per_layer
    return slice(pos, pos + 2)


def connect(cols, x, y, diagonal, neighbour_length):
    x0 = x % cols
    y0 = x // cols
    x1 = y % cols
    y1 = y // cols
    dist = abs(x0 - x1) + abs(y0 - y1)
    if dist <= neighbour_length:
        if diagonal:
            return 1
        if x0 == x1 or y0 == y1:
            return 1
    return 0


def calculate_grid_connectivity_matrix(rows, cols, diagonal=False, neighbour_length=1):
    element_count = rows * cols
    if neighbour_length == 0:
        return np.diag((1,) * element_count)

    matrix = numpy.zeros(element_count * element_count, dtype=theano.config.floatX).reshape((element_count, element_count))
    for y in range(element_count):
        for x in range(element_count):
            matrix[y][x] = connect(cols, x, y, diagonal, neighbour_length)
    return matrix


def process_layers(layers, input, prev_hidden):
    result = list()
    out = input
    for (i,layer) in enumerate(layers):
        hidden, out = layer.forward(out, *prev_hidden[gen_index(i)])
        result += [hidden, out]
    return result


def count_circles():
    """
    simple test - slide
    over the picture and count circles
    """
    # picture 40x100
    # lstm    40x5

    layer = LstmLayer()

def sin_cos():
    """
    Predict f(t) = sin(t) + 1.25 * cos(1.25*t)
    taking as input f(t-1)
    """
    train_set_x, train_set_y = gen_sin_cos_data()
    batch_size = 30
    num_cells = 4
    input_dim = 1
    random_state = numpy.random.RandomState(23455)
    filler = weight_filler.XavierWeightFiller(2, input_dim, num_cells, random_state)
    layer = LstmLayer(input_dim, num_cells, filler, activation=T.nnet.nnet.sigmoid)
    # batch_size x len(sequnce) x size
    input_seq = T.tensor3('t')
    input_seq.tag.test_value = train_set_y[:batch_size]
    weights = []
    weights.extend(layer.weights)

    def step(inp, hid_prev, lstm_out_prev, out_prev):
        hid, lstm_out = layer.forward(inp, hid_prev, lstm_out_prev)
        product_layer = mlp.HiddenLayer(lstm_out,
                                        num_cells,
                                        1, W=None, b=None,
                                        activation=None,
                                        weight_filler=filler,
                                        bias_filler=filler)
        weights.extend(product_layer.params)
        out = product_layer.output
        return [hid, lstm_out, out]

    lstm_out_0 = numpy.random.random((batch_size, num_cells))
    hid_prev_0 = numpy.random.random((batch_size, num_cells))
    out_0 = T.unbroadcast(T.alloc(numpy.asarray(0., dtype=theano.config.floatX),
                                            batch_size, 1),1)

    [hid, lstm_out, out], up  = theano.scan(step, sequences=input_seq.transpose(1,0,2)[:-1,:,:],
                                            outputs_info=[hid_prev_0, lstm_out_0, out_0])
    out_ = out.transpose(1, 0, 2)
    err = 1 / batch_size * T.sum((out_[:,400:] - input_seq[:, 401:]) ** 2)
    grads = T.grad(err, weights)
    updates = learning.rmsprop_updates(0.01, 0.01, weights, grads)
    import pdb;pdb.set_trace()
    rec_learn = theano.function([input_seq], outputs=out, updates=updates)

    lr = 0.0043
    grad = []
    for i in range(len(train_set_x) // batch_size):
        pos = i * batch_size
        batch = train_set_y[pos: pos + batch_size]
        outs = rec_learn(batch)
        print(numpy.mean(numpy.abs(outs[-1, :] - batch[:, -1])))
    import pdb;pdb.set_trace()


def gen_sin_cos_data():
    f = lambda t: numpy.sin(t) + 1.25 * numpy.cos(1.25 * t)
    train_set_x = []
    train_set_y = []
    for i in range(20000):
        start = numpy.random.random() * 1000
        end = start + 5 * numpy.pi
        x_data = numpy.arange(start, end, 0.01)
        y_data = [f(x) for x in x_data]
        train_set_x.append(x_data)
        train_set_y.append(y_data)
    train_set_y = numpy.asarray(train_set_y)
    new_shape = list(train_set_y.shape) + [1]
    return train_set_x, train_set_y.reshape(new_shape)


if __name__ == '__main__':
    sin_cos()

