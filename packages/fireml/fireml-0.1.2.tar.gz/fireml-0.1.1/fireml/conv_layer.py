import theano
from theano.tensor.nnet import conv2d


class ConvLayer(object):
    NUM_FILTERS = 0
    NUM_FEATURE_MAPS = 1
    FILTER_HEIGHT_WIDTH = slice(-2, None, 1)

    @staticmethod
    def build_layer(input, input_shape, filter_shape, stride=(1, 1), border_mode=(0, 0),
                    weights=None, name=None, shared_weights=None,
                    weight_filler=None, bias_filler=None):
        """
        Allocate a ConvLayer with shared variable internal parameters.

        :type input: theano.tensor.dtensor4
        :param input: symbolic image tensor, of shape image_shape

        :type filter_shape: tuple or list of length 3
        :param filter_shape: (number of filters,
                              filter height,filter width)

        :type image_shape: tuple or list of length 4
        :param image_shape: (batch size, num input feature maps,
                             image height, image width)

        :param shared_weights: tuple
            shared variable from another builder
        """

        assert len(input_shape) == 4
        return ConvLayer(input, image_shape=input_shape,
                         filter_shape=filter_shape,
                         stride=stride, border_mode=border_mode,
                         weights=weights, name=name, shared_weights=shared_weights,
                         weight_filler=weight_filler, bias_filler=bias_filler)

    def __init__(self, input, image_shape, filter_shape, stride,
                 border_mode, weights, name, shared_weights,
                 weight_filler=None, bias_filler=None):
        self.input = input
        self.image_shape = image_shape
        self.filter_shape = (filter_shape[self.NUM_FILTERS],
                             image_shape[self.NUM_FEATURE_MAPS]) + filter_shape[self.FILTER_HEIGHT_WIDTH]

        if weights is not None:
            w, b = weights
            expected_w_shape = tuple(self.filter_shape)
            expected_b_shape = (filter_shape[self.NUM_FILTERS], )
            if tuple(w.shape) != expected_w_shape or \
                    tuple(b.shape) != expected_b_shape:
                print("Skipping weights for {0}".format(name))
                print("{0} - {1}".format(w.shape, expected_w_shape))
                print("{0} - {1}".format(b.shape, expected_b_shape))
                weights = None
        self.border_mode = border_mode
        self.stride = stride
        self.W = None
        self.b = None

        self.weight_filler = weight_filler
        self.bias_filler = bias_filler

        self.init_weights(weights, shared_weights)
        # convolve input feature maps with filters
        conv_out = conv2d(input=input,
                               filters=self.W,
                               filter_shape=self.filter_shape,
                               subsample=stride,
                               input_shape=image_shape,
                               border_mode=self.border_mode)

        self.output = conv_out + self.b.dimshuffle('x', 0, 'x', 'x')

        # store parameters of this layer
        self.params = [self.W, self.b]
        #todo: repr, json

    def init_weights(self, weights=None, shared_weights=None):

        if shared_weights is None:
            if weights is None:
                #import numpy
                #rng = self.weight_filler.rng
                # there are "num feature maps * filter height * filter width"
                # inputs to each hidden unit

                #fan_in = numpy.prod(self.filter_shape[1:])
                # each unit in the lower layer receives a gradient from:
                # "num output feature maps * filter height * filter width" /
                #   pooling size
                #fan_out = self.filter_shape[0]

                # initialize weights with random weights
                #W_bound = numpy.sqrt(6. / (fan_in + fan_out))
                #w_values = numpy.asarray(
                #    rng.uniform(low=-W_bound, high=W_bound, size=self.filter_shape),
                #     dtype=theano.config.floatX)

                # the bias is a 1D tensor -- one bias per output feature map
                #b_values = numpy.zeros((self.filter_shape[0],), dtype=theano.config.floatX)
                #print("Old Xavier(low=-sqrt(6. / {0}), high=sqrt(6. / {0}))".format((fan_in + fan_out)))
                w_values = self.weight_filler.generate_weights(shape=self.filter_shape)
                b_values = self.bias_filler.generate_weights(shape=(self.filter_shape[0],))
            else:
                w_values, b_values = weights
            self.W = theano.shared(w_values.astype(theano.config.floatX), borrow=True)
            self.b = theano.shared(value=b_values.astype(theano.config.floatX), borrow=True)
        else:
            self.W, self.b = shared_weights
        # todo: names for weights

    def weights(self):
        return self.W.get_value(), self.b.get_value()

    def get_shared(self):
        return self.W, self.b
