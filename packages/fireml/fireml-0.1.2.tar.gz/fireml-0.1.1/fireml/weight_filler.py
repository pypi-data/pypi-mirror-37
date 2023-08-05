import abc

import numpy
import numpy.random
import theano

from fireml import fire_pb2


class WeightFiller:
    def __init__(self, fan_in: int, fan_out: int, random_state: numpy.random.RandomState, sparse=-1):
        """
        Weight filler class

        :param fan_in: int
            for fully connected layers: size of output of previous layers
        :param fan_out: int
            for fully connected layers: size of outputs in this layer
        :param random_state: numpy.random.RandomState
        :param sparse: int

        """
        self.n_in = fan_in
        self.n_out = fan_out
        self.rng = random_state
        # todo: sparse initialization
        self.sparse = sparse

    @abc.abstractmethod
    def generate_weights(self, shape) -> numpy.ndarray:
        pass


class GaussianWeightFiller(WeightFiller):
    def __init__(self, mean, std, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mean = mean
        self.std = std

    def generate_weights(self, shape) -> numpy.ndarray:
        return self.rng.normal(loc=self.mean, scale=self.std, size=shape).astype(theano.config.floatX)

    def __str__(self):
        return "Gaussian(mean={0}, std={1})".format(self.mean, self.std)


class WeightFillerWithNormalization(WeightFiller):
    def __init__(self, variance_normalization_type: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.var_norm = variance_normalization_type

    def _get_denominator(self):
        if self.var_norm == fire_pb2.FillerParameter.FAN_IN:
            denominator = self.n_in
        elif self.var_norm == fire_pb2.FillerParameter.FAN_OUT:
            denominator = self.n_out
        elif self.var_norm == fire_pb2.FillerParameter.AVERAGE:
            denominator = self.n_in + self.n_out
        else:
            raise NotImplementedError("Normalization type: {0} is not implemented".format(self.var_norm))
        return denominator

    @property
    def variance_norm_str(self):
        return [name for name, value in fire_pb2.FillerParameter.VarianceNorm.items() if value == self.var_norm][0]


class XavierWeightFiller(WeightFillerWithNormalization):
    def generate_weights(self, shape) -> numpy.ndarray:
        denominator = self._get_denominator()
        half_range = numpy.sqrt(6. / denominator)
        return self.rng.uniform(
            low=-half_range,
            high=half_range,
            size=shape
        ).astype(theano.config.floatX)

    def __str__(self):
        denominator = self._get_denominator()
        return "Xavier(low=-sqrt(6. / {0}), high=sqrt(6. / {0}), var_norm={1})".format(denominator,
                                                                                       self.variance_norm_str)


class UniformWeightFiller(WeightFiller):
    def __init__(self, low, high, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.low = low
        self.high = high

    def generate_weights(self, shape) -> numpy.ndarray:
        return self.rng.uniform(
            low=self.low,
            high=self.high,
            size=shape
        ).astype(theano.config.floatX)

    def __str__(self):
        return "Uniform(low={0}, high={1})".format(self.low, self.high)


class ConstantWeightFiller(WeightFiller):
    def __init__(self, constant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.const = constant

    def generate_weights(self, shape) -> numpy.ndarray:
        return numpy.ones(shape=shape).astype(theano.config.floatX) * self.const

    def __str__(self):
        return "Constant({0})".format(self.const)

def build_weight_filler(params, fan_in, fan_out, random_state) -> WeightFiller:
    """
    Build weight filler object

    :param params: fire_pb2.FillerParameter
        Filler object parameters as in prototxt file
    :param fan_in: int
        Numer of inputs to current layer
    :param fan_out:
        Number of outputs of current layer
    :param random_state: numpy.random.RandomState
        Numpy random generator
    :return: weight_filler.WeightFiller object
    """

    sparse = params.sparse
    if sparse != -1:
        raise NotImplementedError("Sparse initialization is not implemented!")
    base_kwargs = dict(fan_in=fan_in, fan_out=fan_out, random_state=random_state, sparse=sparse)
    # constant is default type
    if params.type == 'constant':
        return ConstantWeightFiller(constant=params.value, **base_kwargs)
    elif params.type == 'xavier':
        return XavierWeightFiller(params.variance_norm, **base_kwargs)
    elif params.type == 'gaussian':
        mean = params.mean
        std = params.std
        return GaussianWeightFiller(mean=mean, std=std, **base_kwargs)
    elif params.type == 'uniform':
        low = params.min
        high = params.max
        return UniformWeightFiller(low=low, high=high, **base_kwargs)
    else:
        raise NotImplementedError("Filler {0} is not implemented".format(params.type))
