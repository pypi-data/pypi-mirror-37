# -*- coding: utf-8 -*-

import abc
import pickle
import functools
from collections import OrderedDict

import numpy
import theano
import theano.tensor as T
from theano.ifelse import ifelse
from theano.tensor.signal.pool import pool_2d
from fireml import common
from fireml import conv_layer
from fireml import cost
from fireml import fire_pb2
from fireml import learning
from fireml import mlp
from fireml import weight_filler
from fireml.const import TEST, TRAIN
from fireml.image_data_reader import CifarArchive
from fireml.image_data_reader import ImageDataReader, CifarDataReader
from fireml.preprocessor import Preprocessor
from fireml.softmax import softmax

np = numpy


DROP_VAR = '__drop_var'


class Top:
    def __init__(self, name, builder):
        self.writers = []
        self.name = name
        self.expression = None
        self._out = None
        self.builder = builder
        self.readers = []

    def __hash__(self):
        return hash(self.name)

    def add_writer(self, writer):
        self.writers.append(writer)

    def get_expression(self):
        pass

    def add_reader(self, reader):
        assert reader not in self.readers
        self.readers.append(reader)

    @property
    def reader_count(self):
        return len(self.readers)

    def _find_prev_layer(self, name):
        return self._find_prev(name, getter=lambda name, x: x)

    def _find_prev(self, name, getter=lambda name, x: x.top(name)):
        prev = None
        for writer in self.writers:
            if writer == name:
                # find intermidiate writer to this top
                if prev is not None:
                    return getter(self.name, self.builder.layers[prev])
            prev = writer

    def build(self, name=None):
        if name is not None:
            # check if requesting layer is
            # is in writers of this top, if so return previous writer
            result = self._find_prev(name)
            if result is not None:
                return result
        # nope: proceed to building self.builder.layers from writer[0]
        # and return output to requesting layer
        # which is not writing here, only reading
        if self._out is None:
            print("Start building {0}".format(self.name))
            for w in self.writers:
                self.builder.layers[w].top(self.name)
            if len(self.writers) == 0:
                # dummy top for Input layer which doesn't have top param - so we have 0 writers
                self._out = self.builder.layers[self.name].top(self.name)
            else:
                self._out = self.builder.layers[self.writers[-1]].top(self.name)
            print("Finished building {0}".format(self.name))
        return self._out

    def _prev_shape(self, name):
        prev = None
        for writer in self.writers:
            if writer == name:
                # find intermidiate writer to this top
                if prev is not None:
                    return self.builder.layers[prev].shape(self.name)
            prev = writer

    def shape(self, name=None):
        if name is not None:
            result = self._prev_shape(name)
            if result is not None:
                return result
        if len(self.writers) == 0:
            return self.builder.layers[self.name].shape(self.name)
        return self.builder.layers[self.writers[-1]].shape(self.name)

    def drop_grads(self, name):
        result = self._find_prev_layer(name)
        if result is not None:
            result.drop_grads()
        else:
            self.builder.layers[self.writers[-1]].drop_grads()


class LayerBuilder:
    def __init__(self, params, builder=None):
        assert builder is not None
        self.params = params
        # print(params)
        self.type = params.type
        self.name = params.name
        self.tops = params.top
        self.bottoms = params.bottom
        print("Read params {0}".format(params.name))
        self._shapes = OrderedDict()
        self._theano_data = None
        self._tops = OrderedDict()
        self.builder = builder
        self.propagate_down = len(self.params.propagate_down) == 0 or\
            all([x for x in self.params.propagate_down])
        self._drop_grads = False
        self.updates = list()

    def shape(self, name):
        return self._shapes[name]

    def build(self):
        raise NotImplementedError()

    def top(self, name):
        self.build()
        return self._tops[name]

    def drop_grads(self):
        # todo: drop only some grads?
        self._drop_grads = True
        self.propagate_down = False
        print("{0} does not need backward propagation".format(self.name))
        for b in self.bottoms:
            self.builder.tops[b].drop_grads(self.name)

    def calculate_drop(self):
        if not self.propagate_down:
            for b in self.bottoms:
                self.builder.tops[b].drop_grads(self.name)

    def get_input(self):
        b = self.bottoms[0]
        input = self.builder.tops[b].build(self.name)
        return input


class BatchNormalization(LayerBuilder):
    def get_axis(self, input):
        axis = tuple([0] + list(range(input.ndim))[2:])
        return axis

    def get_broadcast_shape(self, input):
        broadcast_shape = [1 for i in range(input.ndim)]
        broadcast_shape[1] = input.shape[1]
        return broadcast_shape

    def get_input(self):
        input = super().get_input()
        counter = theano.shared(numpy.int32(1))
        broadcast_shape = self.get_broadcast_shape(input)
        input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
        self.mean_by_layers = theano.shared(numpy.ones(shape=input_shape[1]))
        self.std_by_layers = theano.shared(numpy.ones(shape=input_shape[1]))
        axis = self.get_axis(input)
        mean = input.mean(axis=axis)
        # possible implementation: todo: check which is better
        # std = ((input - mean_new.reshape(broadcast_shape)) ** 2).mean(axis=axis) ** 0.5
        std = input.std(axis=axis)
        mean_new = common.iterative_mean(self.mean_by_layers, mean, counter)
        std_new = common.iterative_mean(self.std_by_layers, std, counter)
        self.updates.append([self.mean_by_layers, mean_new])
        self.updates.append([self.std_by_layers, std_new])
        self.updates.append([counter, ifelse(T.lt(counter, 1), counter + 1, counter)])
        batch_normalized = (input - mean_new.reshape(broadcast_shape)) / (std_new.reshape(broadcast_shape) + 0.00000001)
        return batch_normalized



class LayerBuilderWithWeights(BatchNormalization):
    def __init__(self, params, random_state: numpy.random.RandomState,
                 weights=None, builder=None, shared_weights=None):
        super().__init__(params, builder)
        self.random_state = random_state
        self.weights = weights
        self.shared_weights = shared_weights
        self.learn_params = OrderedDict()

    @abc.abstractmethod
    def number_of_parameters(self):
        raise NotImplementedError()

    @property
    def weight_filler_params(self):
        return getattr(self.params, self._layer_param_name).weight_filler

    @abc.abstractproperty
    def _layer_param_name(self) -> str:
        pass

    @property
    def bias_filler_params(self):
        return getattr(self.params, self._layer_param_name).bias_filler

    def get_weights(self):
        raise NotImplementedError

    def get_shared(self):
        raise NotImplementedError

    def drop_grads(self):
        super().drop_grads()
        for key in self.learn_params:
            self.learn_params[key] = 0

    def get_learning_rates(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_fan_in(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_fan_out(self, **kwargs):
        pass

    def get_weight_filler(self) -> weight_filler.WeightFiller:
        filler = weight_filler.build_weight_filler(self.weight_filler_params,
                                                   self.get_fan_in(), self.get_fan_out(),
                                                   self.random_state)
        print("Weight filler: " + str(filler))
        return filler

    def get_bias_filler(self) -> weight_filler.WeightFiller:

        filler = weight_filler.build_weight_filler(self.bias_filler_params,
                                                   self.get_fan_in(), self.get_fan_out(),
                                                   self.random_state)
        print("Bias filler: " + str(filler))
        return filler


class ConvolutionLayerBuilder(LayerBuilderWithWeights):
    def __init__(self, params, random_state, weights=None, builder=None, shared_weights=None):
        super().__init__(params, random_state=random_state, weights=weights,
                         builder=builder, shared_weights=shared_weights)

        len(params.param) == 2
        self.read_param()
        self.convolution_param = OrderedDict()
        # print(params.convolution_param)
        cv = params.convolution_param
        self.convolution_param['filters'] = cv.num_output

        if len(cv.pad) == 0:
            self.convolution_param['pad'] = 0
        else:
            assert len(cv.pad) == 1
            self.convolution_param['pad'] = cv.pad[0]
        assert len(cv.kernel_size) == 1
        self.convolution_param['kernel_size'] = cv.kernel_size[0]
        if len(cv.stride) == 0:
            self.convolution_param['stride'] = [1, 1]
        else:
            self.convolution_param['stride'] = [x for x in cv.stride] * 2
        self.filter_shape = (self.convolution_param['filters'],
                             self.convolution_param['kernel_size'],
                             self.convolution_param['kernel_size'])
        self.input_shape = None
        # todo: stride_h, stride_w

    def number_of_parameters(self):
        return numpy.prod(self.filter_shape) * self.input_feature_maps

    @property
    def input_feature_maps(self):
        return self.builder.tops[self.bottoms[0]].shape(self.name)[1]

    def get_fan_out(self, num_out_feature_maps: int, filter_height: int, filter_width: int, pooling_shape=(1, 1)):
        """
        each unit in the lower layer receives a gradient from:
        "num output feature maps * filter height * filter width" / pooling size
           approximate by not using pooling size

        :param num_out_feature_maps: int
        :param filter_height: int
        :param filter_width: int
        :param pooling_shape: tuple
            Pooling shape - like 2x2 or 4x3
        :return: number of receives of output of each neuron
        """
        return num_out_feature_maps * filter_height * filter_width / numpy.prod(pooling_shape)

    def get_fan_in(self, filter_height: int, filter_width: int, num_feature_maps: int):
        """
        There are "num feature maps * filter height * filter width"
        inputs to each hidden unit

        :param filter_height: int

        :param filter_width: int

        :param num_feature_maps: int
            Number of feature maps
        :return: int
            Number of inputs for each neuron
        """

        return filter_height * filter_width * num_feature_maps

    def read_param(self):
        param = self.params.param
        if len(param) == 1:
            self.learn_params['w_lr_mult'] = param[0].lr_mult
            self.learn_params['w_dec_mult'] = param[0].decay_mult
            self.learn_params['b_lr_mult'] = param[0].lr_mult
            self.learn_params['b_dec_mult'] = param[0].decay_mult
        elif len(param) == 0:
            self.learn_params['w_lr_mult'] = 1
            self.learn_params['w_dec_mult'] = 1
            self.learn_params['b_lr_mult'] = 1
            self.learn_params['b_dec_mult'] = 1
        else:
            raise NotImplementedError

    def shape(self, name):
        if not self._shapes:
            self.input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            out_shape = self._out_shape()
            self._shapes = {self.tops[0]: (self.input_shape[0], self.filter_shape[0]) + tuple(out_shape)}
        return super().shape(name)

    def _out_shape(self):
        out_shape = common.calculate_conv_size(self.input_shape[-2:], filter_size=self.filter_shape[-2:],
                                               padding=self.padding, stride=self.stride, border='valid')
        return out_shape

    @property
    def padding(self):
        return (self.convolution_param['pad'],) * 2

    @property
    def stride(self):
        return self.convolution_param['stride']

    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            assert len(self.bottoms) == 1
            b = self.bottoms[0]
            input = self.get_input()
            self.input_shape = self.builder.tops[b].shape(self.name)
            weight_fill = self.get_weight_filler()
            bias_fill = self.get_bias_filler()
            self._theano_data = conv_layer.ConvLayer.build_layer(input, input_shape=self.input_shape,
                                                                 filter_shape=self.filter_shape,
                                                                 stride=self.stride,
                                                                 border_mode=self.padding,
                                                                 weights=self.weights,
                                                                 name=self.name,
                                                                 shared_weights=self.shared_weights,
                                                                 weight_filler=weight_fill,
                                                                 bias_filler=bias_fill)
            if hasattr(self._theano_data.output.tag, 'test_value'):
                assert all([x == y for (x, y) in
                            zip(self._out_shape(), self._theano_data.output.tag.test_value.shape[-2:])])
            self._tops = {self.tops[0]: self._theano_data.output}
            print("{0} -> {1}".format(b, self.name))
            print("{0} shape : {1}".format(self.name, self.shape(self.tops[0])))

    def get_weights(self):
        return self._theano_data.weights()

    def get_shared(self):
        return self._theano_data.get_shared()

    def get_learning_rates(self):
        return self.learn_params['w_lr_mult'], self.learn_params['b_lr_mult']

    def get_weight_filler(self) -> weight_filler.WeightFiller:

        pool_shape = self.compute_pooling()

        height, num_input_feature_maps, num_out_feature_maps, width = self.__get_filler_data()
        filler = weight_filler.build_weight_filler(self.weight_filler_params,
                                                   self.get_fan_in(height, width, num_input_feature_maps),
                                                   self.get_fan_out(num_out_feature_maps, height, width,
                                                                    pooling_shape=pool_shape),
                                                   self.random_state)
        print("Weight filler: " + str(filler))
        return filler

    def compute_pooling(self):
        def next_reader(layer):
            return self.builder.layers[self.builder.tops[layer.tops[-1]].readers[-1].name]

        next_layer = self
        pool_shape = (1, 1)
        while True:
            next_layer = next_reader(next_layer)
            if isinstance(next_layer, LayerBuilderWithWeights):
                break
            elif isinstance(next_layer, ConcatLayerBuilder):
                continue
            elif isinstance(next_layer, PoolingLayerBuilder):
                pool_shape = next_layer.pooling_shape   # pylint:  no-member
                break
            elif isinstance(next_layer, MaxoutLayerBuilder):
                pool_shape = (next_layer.size, )
                break
            elif isinstance(next_layer, ActivationFunction):
                continue
            else:
                raise NotImplementedError(next_layer)
        return pool_shape

    def __get_filler_data(self):
        height = self.filter_shape[1]
        width = self.filter_shape[2]
        num_input_feature_maps = self.input_shape[1]
        num_out_feature_maps = self.filter_shape[0]
        return height, num_input_feature_maps, num_out_feature_maps, width

    def get_bias_filler(self) -> weight_filler.WeightFiller:
        height, num_input_feature_maps, num_out_feature_maps, width = self.__get_filler_data()
        pool_shape = self.compute_pooling()
        filler = weight_filler.build_weight_filler(self.bias_filler_params,
                                                   self.get_fan_in(height, width, num_input_feature_maps),
                                                   self.get_fan_out(num_out_feature_maps, height, width,
                                                                    pooling_shape=pool_shape),
                                                   self.random_state)
        print("Bias filler: " + str(filler))
        return filler

    @property
    def _layer_param_name(self) -> str:
        return 'convolution_param'


class ActivationFunction(LayerBuilder):
    def get_function(self):
        raise NotImplementedError()

    def shape(self, name):
        if not self._shapes:
            self._shapes[self.tops[0]] = self.builder.tops[self.bottoms[0]].shape(self.name)
        return super().shape(name)

    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            assert len(self.bottoms) == 1
            input = self.get_input()
            self._theano_data = self.get_function()(input)
            for t in self.tops:
                self._tops[t] = self._theano_data
            b = self.bottoms[0]
            print("{0} -> {1}".format(b, self.name))
            print("{0} shape : {1}".format(self.name, self.shape(self.tops[0])))


class ReLULayerBuilder(ActivationFunction):
    def get_function(self):
        return T.nnet.relu


class SeLULayerBuilder(ActivationFunction):
    def get_function(self):
        return T.nnet.selu


class ELULayerBuilder(ActivationFunction):
    def get_function(self):
        return T.nnet.elu


class ConcatLayerBuilder(LayerBuilder):

    def shape(self, name):
        if not self._shapes:
            input_shapes = []
            for b in self.bottoms:
                input_shapes.append(self.builder.tops[b].shape(self.name))
            out_shape = list(input_shapes[0])
            for j, input_shape1 in enumerate(input_shapes):
                for input_shape2 in input_shapes[j:]:
                    if not all(x == y for (i, (x, y)) in enumerate(zip(input_shape1, input_shape2)) if i != self.axis):
                        print("input shapes {0} neq {1}".format(input_shape1, input_shape2))
                        raise RuntimeError("Shapes not equal {0}, {1}".format(*[self.builder.tops[x].name for x in self.bottoms]))
            out_shape[self.axis] = sum([x[self.axis] for x in input_shapes])
            self._shapes = {self.tops[0]: tuple(out_shape)}
        return super().shape(name)

    @property
    def axis(self):
        return self.params.concat_param.axis

    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            inputs = []
            for b in self.bottoms:
                inputs.append(self.builder.tops[b].build(self.name))
                print("{0} -> {1}".format(b, self.name))
            self._theano_data = T.concatenate(inputs, axis=self.axis)
            self._theano_data.name = 'concatenete_axis_{0}'.format(self.axis)
            self._tops[self.tops[0]] = self._theano_data
            print("{0} shape : {1}".format(self.name, self.shape(self.tops[0])))


class MaxoutLayerBuilder(LayerBuilder):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.size = params.maxout_param.size

    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            x = self.get_input()
            size = self.size
            if hasattr(x.tag, 'test_value'):
                assert x.tag.test_value.shape[1] % size == 0
            xsh = self._get_reshape(x)
            x_reshaped = x.reshape(xsh)
            t_lambda = getattr(self.params.maxout_param, 'lambda')
            if t_lambda:
                # algorithm is somewhat incorrect but fast
                # for [0.1, 0.5, 0.4] it will select first element with p = 0.09, 0.54, 0.37
                x_soft = softmax(x_reshaped * t_lambda, axis=2)
                rs = T.shared_randomstreams.RandomStreams()
                sample = x_soft - rs.uniform(size=x_soft.shape, dtype=x_soft.dtype)
                argmax_indices = common.get_argmax_indices(sample, axis=2)
                self._theano_data = x_reshaped[argmax_indices]
            else:
                self._theano_data = x.reshape(xsh).max(axis=2)
            self._theano_data.name = 'maxout_{0}'.format(self.size)
            self._tops[self.tops[0]] = self._theano_data

    def _get_reshape(self, x):
        xsh = []
        for i in range(x.ndim):
            if i == 1:
                xsh.append(x.shape[1] // self.size)
                xsh.append(self.size)
            else:
                xsh.append(x.shape[i])
        return xsh

    def shape(self, name):
        if not self._shapes:
            bottom_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            assert bottom_shape[1] % self.size == 0
            current_shape = tuple(x // self.size if i == 1 else x for (i, x) in enumerate(bottom_shape))
            self._shapes[self.tops[0]] = current_shape
        return super().shape(name)


class PoolingLayerBuilder(LayerBuilder):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.pooling_params = OrderedDict()
        p = self.pooling_params
        if params.pooling_param.pool == 1:
            p['mode'] = 'average_exc_pad'
        elif params.pooling_param.pool == 0:
            p['mode'] = 'max'
        else:
            raise NotImplementedError(str(params.pooling_param))
        p['pad'] = params.pooling_param.pad
        p['kernel_size'] = params.pooling_param.kernel_size
        p['stride'] = params.pooling_param.stride
        p['global_pooling'] = params.pooling_param.global_pooling

    def shape(self, name):
        if not self._shapes:
            b, input_shape, new_shape, p, padding, shape, stride = self.__get_parameters()
            if p['global_pooling']:
                self._shapes[self.tops[0]] = (input_shape[0], input_shape[1])
            else:
                self._shapes[self.tops[0]] = (input_shape[0], input_shape[1]) + tuple(new_shape)
        return super().shape(name)

    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            b, input_shape, new_shape, p, padding, shape, stride = self.__get_parameters()
            input = self.builder.tops[b].build(self.name)
            if hasattr(input.tag, 'test_value'):
                assert input_shape == input.tag.test_value.shape
            pooled = pool_2d(input, shape, ignore_border=True, pad=padding, stride=stride, mode=p['mode'])
            if p['global_pooling']:
                print("Global pooling layer: {0}".format(self.name))
                self._theano_data = pooled.reshape((input_shape[0], input_shape[1]))
            else:
                self._theano_data = pooled
            print("{0} shape : {1}".format(self.name, self.shape(self.tops[0])))
            self._tops[self.tops[0]] = self._theano_data

    def __get_parameters(self):
        assert len(self.bottoms) == 1
        b = self.bottoms[0]
        p = self.pooling_params
        input_shape = self.builder.tops[b].shape(self.name)
        stride = (p['stride'],) * 2
        if p['global_pooling']:
            shape = input_shape[-2], input_shape[-1]
            stride = shape
        else:
            shape = (p['kernel_size'],) * 2
        padding = (self.pooling_params['pad'],) * 2
        new_shape = common.calculate_pool_size(input_shape[-2:], shape,
                                               padding=padding,
                                               stride=stride,
                                               ignore_border=True)
        if all([x == 0 for x in padding]):
            padding = None
        return b, input_shape, new_shape, p, padding, shape, stride

    @property
    def pooling_shape(self):
        return self.__get_parameters()[-2]


class SameShapeMixin(LayerBuilder):
    @abc.abstractmethod
    def build(self, builder=None):
        raise NotImplementedError()

    def shape(self, name):
        if not self._shapes:
            self._shapes[self.tops[0]] = self.builder.tops[self.bottoms[0]].shape(self.name)
        return super().shape(name)


class SoftmaxLayerBuilder(ActivationFunction):
    def get_function(self):
        axis = self.params.softmax_param.axis
        return functools.partial(softmax, axis=axis)


class SigmoidLayerBuilder(ActivationFunction):
    def get_function(self):
        return T.nnet.nnet.sigmoid


class TanHLayerBuilder(ActivationFunction):
    def get_function(self):
        return T.tanh


class DataSource(LayerBuilder):
    def has_label(self) -> bool:
        raise NotImplementedError


class ImageDataLayerBuilder(DataSource):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.image_params = params.image_data_param
        self.transform_params = params.transform_param
        self._y = None
        self._data_shape = (self.image_params.batch_size,
                            1 if self.transform_params.force_gray else 3,
                            self.image_params.new_height,
                            self.image_params.new_width)
        self._preprocessor = None

    def shape(self, name):
        if not self._shapes:
            self._shapes[self.tops[0]] = self.get_shape()
            n_labels = self.get_num_labels()
            if n_labels == 0:
                size = (self.image_params.batch_size,)
            else:
                size = (self.image_params.batch_size, n_labels)
            self._shapes[self.tops[1]] = size
        return self._shapes[name]

    def get_shape(self):
        assert self._data_shape is not None
        return self._data_shape

    def build(self):
        print("building {0}".format(self.name))
        if self._theano_data is None:
            self._add_source()
            self._make_variables()

    def _add_source(self):
        if self._preprocessor is None:
            new_shape = self._get_new_shape()
            if len(self.transform_params.mean_value) == 0:
                mean = None
            else:
                mean = [x for x in self.transform_params.mean_value]
            p = Preprocessor(new_shape, mean, self.transform_params.scale)
            self._add_source_to_builder(mean, p)
            self._preprocessor = p

    def _get_new_shape(self):
        new_shape = self.image_params.new_width, self.image_params.new_height
        if 0 in new_shape:
            new_shape = None
            # todo: read from file
            raise NotImplementedError
        return new_shape

    def _add_source_to_builder(self, mean, p):
        self.builder.add_data_source(self.name, ImageDataReader(self.image_params.source,
                                                                self.image_params.batch_size,
                                                                p, self.image_params.shuffle,
                                                                self.transform_params.mirror,
                                                                mean,
                                                                self.transform_params.equalize_histogram,
                                                                self.transform_params.force_gray,
                                                                scale=self.transform_params.scale,
                                                                standard_params=self.transform_params.standard_params))

    def _make_variables(self):
        if self._theano_data:
            return
        # data
        x = T.tensor4(self.tops[0], dtype=theano.config.floatX)
        x.tag.test_value = np.random.random(self._shapes[self.tops[0]]).astype(theano.config.floatX)
        self._tops[self.tops[0]] = x
        self.builder.add_input_var(self.tops[0], x, self._shapes[self.tops[0]])
        self._theano_data = x
        # todo: image size
        if self.has_label():
            # for classification: (batch_size, n_classes) matrix
            self.builder.label_name = self.tops[1]
            n_labels = self.get_num_labels()
            if n_labels == 0:
                y = T.ivector(self.tops[1])
            else:
                y = T.matrix(self.tops[1], theano.config.floatX)
            y.tag.test_value = np.random.randint(0, 2, size=self.shape(self.tops[1])).astype(theano.config.floatX)
            self.builder.add_input_var(self.tops[1], y, self.shape(self.tops[1]))
            self._y = y
            self._tops[self.tops[1]] = y

    def get_num_labels(self):
        n_labels = 0
        if hasattr(self.image_params, 'n_labels'):
            n_labels = self.image_params.n_labels
        return n_labels

    def has_label(self):
        return len(self.tops) == 2

    def set_label_shape(self, shape):
        self._y.tag.test_value = np.random.randint(0, 2, size=shape).astype(theano.config.floatX)


class CifarBuilder(ImageDataLayerBuilder):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.path = params.image_data_param.source
        self.data_reader = None
        height = self.image_params.new_height if self.image_params.new_height else 32
        width = self.image_params.new_width if self.image_params.new_width else 32
        self._data_shape = (self.image_params.batch_size,
                            1 if self.transform_params.force_gray else 3,
                            height,
                            width)

    def _add_source_to_builder(self, mean, p: Preprocessor):
        load_test = self.builder.get_current_phase() == fire_pb2.TEST
        self.data_reader = CifarDataReader(self.image_params.source,
                                           self.image_params.batch_size, p,
                                           self.image_params.shuffle,
                                           self.transform_params.mirror, mean,
                                           self.transform_params.equalize_histogram,
                                           self.transform_params.force_gray,
                                           load_test=load_test,
                                           scale=self.transform_params.scale,
                                           standard_params=self.transform_params.standard_params)

        self.builder.add_data_source(self.name, self.data_reader)

    def get_num_labels(self):
        self._add_source()
        if self.data_reader.coarse_labels:
            raise NotImplementedError("Coarse labels are not implemented!")
        if self.data_reader.cifar_type == CifarArchive.CIFAR10:
            return 10
        elif self.data_reader.cifar_type == CifarArchive.CIFAR100:
            return 100
        else:
            raise RuntimeError("Unexpected cifar type: {0}".format(self.data_reader.cifar_type))

    def _get_new_shape(self):
        new_shape = self.image_params.new_width, self.image_params.new_height
        if 0 in new_shape:
            new_shape = None
        return new_shape


def get_image_data_layer_builder(params, builder=None):
    if params.image_data_param.source.endswith('.tar.gz'):
        return CifarBuilder(params, builder=builder)
    return ImageDataLayerBuilder(params, builder=builder)


class LayerWithLoss(LayerBuilder):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self._label_shape = None
        self.loss_name = None

    @abc.abstractmethod
    def build(self):
        raise NotImplementedError()

    def loss(self):
        return self._theano_data


class LossShapeMixin(LayerBuilder):
    def shape(self, name):
        if not self._shapes:
            self._shapes[self.tops[0]] = (1,)
        return super().shape(name)


class CrossEntropyLossLayerBuilder(LossShapeMixin, LayerWithLoss):
    """
    Multilabel logloss
    """
    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            p_y_given_x = self.builder.tops[self.bottoms[0]].build(self.name)
            input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            # label
            y = self.builder.tops[self.bottoms[1]].build(self.name)
            label_shape = self.builder.tops[self.bottoms[1]].shape(self.name)
            assert sum(input_shape) == sum(label_shape)
            self._theano_data = cost.cross_entropy(p_y_given_x.reshape(label_shape), y)
            self._tops[self.tops[0]] = self._theano_data
            self.loss_name = self.tops[0]


class SigmoidCrossEntropyLossLayerBuilder(LossShapeMixin, LayerWithLoss):
    """
    Multilabel logloss
    """
    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            p_y_given_x = T.nnet.sigmoid(self.builder.tops[self.bottoms[0]].build(self.name))
            input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            # label
            y = self.builder.tops[self.bottoms[1]].build(self.name)
            label_shape = self.builder.tops[self.bottoms[1]].shape(self.name)
            assert sum(input_shape) == sum(label_shape)
            self._theano_data = cost.cross_entropy(p_y_given_x.reshape(label_shape), y)
            self._tops[self.tops[0]] = self._theano_data
            self.loss_name = self.tops[0]


class SoftmaxWithLossLayerBuilder(LossShapeMixin, LayerWithLoss):
    """
    Multilabel logloss
    """
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.axis = params.softmax_param.axis
        # todo
        assert self.axis == 1

    def build(self):
        if self._theano_data is None:
            # expecting matrix
            # batch x dim
            print("building {0}".format(self.name))
            x = self.builder.tops[self.bottoms[0]].build(self.name)
            input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            assert len(input_shape) == 2
            # matrix: (batch_size, n_classes)
            self._label_shape = input_shape[:2]
            y = self.builder.tops[self.bottoms[1]].build(self.name)
            axis = self.params.softmax_param.axis
            p_y_given_x = softmax(x, axis=axis)
            y_norm = y
            if y.ndim == 2:
                print("normalize label")
                y_norm = y/y.sum(axis=1, keepdims=True)
            self._theano_data = cost.cross_entropy(p_y_given_x, y_norm)
            self._tops[self.tops[0]] = self._theano_data
            self.loss_name = self.tops[0]


class SortLossLayerBuilder(LossShapeMixin, LayerWithLoss):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.average = params.sortloss_param.average

    def build(self):
        if self._theano_data is None:
            # expecting 4 or 3 dimentional tensor
            # (batch, layers, feature_map(s))
            print("building {0}".format(self.name))
            x = self.builder.tops[self.bottoms[0]].build(self.name)
            input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            x_resh = x
            if len(input_shape) == 4:
                # reshape
                assert x.ndim == 4
                x_resh = x.reshape((x.shape[0], x.shape[1], T.prod(x.shape[2:])))
            # matrix: (batch_size, n_classes)
            self._label_shape = input_shape[:2]
            y = self.builder.tops[self.bottoms[1]].build(self.name)
            self._theano_data = cost.sortloss(x_resh, y, self.average)
            self._tops[self.tops[0]] = self._theano_data
            self.loss_name = self.tops[0]


class DropoutLayerBuilder(SameShapeMixin, LayerBuilder):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.dropout_ratio = params.dropout_param.dropout_ratio

    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            x = self.builder.tops[self.bottoms[0]].build(self.name)
            training = self.builder.get_current_phase() == TRAIN
            if training:
                self._theano_data = learning.dropout(x, self.dropout_ratio)
            else:
                print("skipping droput in current phase")
                if 0 < self.dropout_ratio:
                    self._theano_data = x
                    #self._theano_data = x * self.dropout_ratio
                else:
                    self._theano_data = x
            input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            self._shapes[self.tops[0]] = input_shape
            self._tops[self.tops[0]] = self._theano_data


class InferedParams:
    def __init__(self, name, type, input_dim):
        self.name = name
        self.type = type
        self.bottom = []
        self.top = [self.name]
        self.input_dim = input_dim
        self.propagate_down = []


class AccuracyLayerBuilder(LossShapeMixin, LayerBuilder):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.propagate_down = [False, False]

    def build(self):
        print("building {0}".format(self.name))
        if self._theano_data is None:
            x = self.builder.tops[self.bottoms[0]].build(self.name)
            label = self.builder.tops[self.bottoms[1]].build(self.name)
            self._theano_data = cost.accuracy(x, label)
            input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            label_shape = self.builder.tops[self.bottoms[1]].shape(self.name)
            assert all([x == y for (x,y) in zip(input_shape, label_shape)])
            assert all([x == y for (x,y) in zip(input_shape, label.tag.test_value.shape)])
            self._tops[self.tops[0]] = self._theano_data


class InputLayer(LayerBuilder):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)

    def shape(self, name):
        if not self._shapes:
            self._shapes[self.tops[0]] = tuple(self.params.input_param.shape[0].dim)
        return super().shape(name)

    def build(self):
        print("building {0}".format(self.name))
        if self._theano_data is None:
            if len(self.params.input_param.shape) != 1:
                raise NotImplementedError
            shape = self.shape(self.tops[0])
            ndim = len(shape)
            if ndim == 4:
                self._theano_data = T.tensor4(self.tops[0])
            elif ndim == 3:
                self._theano_data = T.tensor3(self.tops[0])
            elif ndim == 2:
                self._theano_data = T.matrix(self.tops[0])
            elif ndim == 1:
                self._theano_data = T.scalar(self.tops[0])
            else:
                raise NotImplementedError("Not implemented number of dimentions: {0}".format(ndim))
            self._theano_data.tag.test_value = np.random.random(shape).astype(theano.config.floatX)
            self._tops[self.tops[0]] = self._theano_data
            print("{0} shape: {1}".format(self.name, shape))
            self.builder.add_input_var(self.tops[0], self._theano_data, shape)

    def set_input(self, input):
        self._theano_data = input
        self._tops[self.tops[0]] = self._theano_data
        print("{0} shape: {1}".format(self.name, self.params.input_param.shape[0].dim))
        self._shapes[self.tops[0]] = tuple(self.params.input_param.shape[0].dim)
        self.builder.add_input_var(self.tops[0], self._theano_data, self._shapes[self.tops[0]])


def dbg(arg, name):
    return arg
#     return debug(arg, name, 1, raise_on_failed_nan_check=True, check_not_all_nan=True)


class ExpressionLayerBuilder(SameShapeMixin, LayerBuilder):
    def __init__(self, params, builder=None):
        super().__init__(params, builder)
        self.expression_param = params.expression_param

    def build(self):
        print("building {0}".format(self.name))
        if self._theano_data is None:
            expr = self.expression_param.expression
            x = self.builder.tops[self.bottoms[0]].build(self.name)  # pylint: unused-variable
            self._theano_data = dbg(eval(expr), 'expr') # pylint: eval-used
            self._theano_data.name = expr
            self._tops[self.tops[0]] = self._theano_data


class InnerProductLayerBuilder(LayerBuilderWithWeights):
    def number_of_parameters(self):
        return self.n_in * self.n_out

    def __init__(self, params, random_state, weights=None, builder=None, shared_weights=None):
        super().__init__(params, random_state=random_state, weights=weights,
                         builder=builder, shared_weights=shared_weights,
                         weight_filler=weight_filler)
        self._n_in = -1
        self.n_out = self.params.inner_product_param.num_output

    @property
    def n_in(self):
        if self._n_in == -1:
            input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            self._n_in = input_shape[self.axis]
        return self._n_in

    def shape(self, name):
        if not self._shapes:
            input_shape = self.builder.tops[self.bottoms[0]].shape(self.name)
            out_shape = common.calculate_product_shape(input_shape, self.n_out)
            # assert all([x == y for (x,y) in zip(out_shape, self._theano_data.output.tag.test_value.shape)])
            self._shapes = {self.tops[0]: tuple(out_shape)}
        return self._shapes[name]

    @property
    def axis(self):
        return self.params.inner_product_param.axis

    def build(self):
        if self._theano_data is None:
            print("building {0}".format(self.name))
            assert len(self.bottoms) == 1
            b = self.bottoms[0]
            input = self.get_input()
            assert(self.axis == 1)
            W, bias = (self.weights if self.weights is not None else (None, None))
            W, bias = (self.shared_weights if self.shared_weights is not None else (W, bias))
            if 'exp' in [k for k in self.builder.layers.keys()]:
                if W is not None and not isinstance(W, numpy.ndarray):
                    W = dbg(W, self.name + '.W')
                    bias = dbg(bias, self.name + '.bias')
            weight_fill = self.get_weight_filler()
            bias_fill = self.get_bias_filler()
            self._theano_data = mlp.HiddenLayer(input,
                                                self.n_in,
                                                self.n_out, W=W, b=bias,
                                                activation=None,
                                                weight_filler=weight_fill,
                                                bias_filler=bias_fill)


            if 'exp' in [k for k in self.builder.layers.keys()]:
                out = dbg(self._theano_data.output, str(self.name))
                self._tops = {self.tops[0]: out}
            else:
                self._tops = {self.tops[0]: self._theano_data.output}
            print("{0} -> {1}".format(b, self.name))
            if 'b' in "{0} -> {1}".format(b, self.name):
                import pdb;pdb.set_trace()
            print("{0} shape : {1}".format(self.name, self.shape(self.tops[0])))

    def get_weights(self):
        return [x.get_value() for x in self._theano_data.params]

    def get_shared(self):
        return self._theano_data.params

    def get_learning_rates(self):
        return self.learn_params['w_lr_mult'], self.learn_params['b_lr_mult']

    def get_fan_in(self, **kwargs):
        return self.n_in

    def get_fan_out(self, **kwargs):
        return self.n_out

    @property
    def _layer_param_name(self) -> str:
        return 'inner_product_param'


class Builder:
    def add_input_var(self, name, variable, shape):
        if 'exp' in [k for k in self.layers.keys()]:
            variable = dbg(variable, name)
        if name in self.input_vars:
            print("replacing input variable {0}, new shape: {1}".format(name, shape))
        else:
            print("new input variable {0}, shape: {1}".format(name, shape))
            self.inputs.append(name)
        self.input_vars[name] = variable
        self.input_shapes[name] = shape

    def theano_function(self, solver=None, **theano_kwargs):
        if self.get_current_phase() == TRAIN:
            assert solver is not None
            if self._train_func is None:
                self._train_func = self.build_train(solver, **theano_kwargs)
            return self._train_func
        elif self.get_current_phase() == TEST:
            if self._test_func is None:
               self._test_func = self.build_test(solver, **theano_kwargs)
            return self._test_func
        else:
            raise NotImplementedError

    def build_train(self, solver, **kwargs):
        print("Building train model")
        shared = self.get_shared()
        weights = []
        lr_mults = []
        # L1 norm ; one regularization option is to enforce L1 norm to
        # be small
        L1 = []

        # square of L2 norm ; one regularization option is to enforce
        # square of L2 norm to be small
        L2 = []

        for key in sorted(shared.keys()):
            for w, lr in zip(shared[key], self.get_learning_rates(key)):
                if lr != 0:
                    weights.append(w)
                    lr_mults.append(1.0)
                    L1.append(abs(w).sum())
                    L2.append((w ** 2).sum())

        print("weight decay {0}".format(solver.weight_decay))
        grads = T.grad(self.loss.loss() + solver.weight_decay * T.sum(L2) + solver.weight_decay * T.sum(L1), weights)
        print("momentum {0}".format(solver.momentum))
        print("base learning rate {0}".format(solver.base_lr))
        self._base_lr = theano.shared(solver.base_lr, name='learning_rate')

        if solver.type == "RMSProp":
            print("rms_decay: {0}".format(solver.rms_decay))
            updates = learning.rmsprop_updates(solver.rms_decay, self._base_lr, weights, grads)
        elif solver.type == "SGD":
            updates = learning.gradient_updates_momentum(grads, weights, lr_mults, self._base_lr, solver.momentum)
        else:
            raise NotImplementedError("Not implemented algorithm {0}".format(solver.type))
        for layer in self.layers.values():
            updates.extend(layer.updates)
        lr_update = self._learning_rate_updates(solver)
        updates.extend(lr_update)
        inputs = [self.input_vars[name] for name in self.inputs]
        train_model = theano.function(inputs=inputs,
                                      outputs=self.outputs,
                                      updates=updates, **kwargs)
        return train_model

    def _learning_rate_updates(self, solver):
        result = []
        iter_var = theano.shared(1, 'iteration')
        result.append((iter_var, iter_var + 1))
        if solver.lr_policy == 'poly':
            ratio = (solver.max_iter - iter_var) / solver.max_iter
            result.append((self._base_lr, solver.base_lr * ratio ** solver.power + solver.min_lr * (1 - ratio) ** solver.power))
        elif solver.lr_policy == 'fixed':
            pass
        elif solver.lr_policy == 'cyclical':
            assert(solver.stepsize != 0)
            switch_flag = theano.shared(numpy.int8(1))
            switch = T.switch(switch_flag, (solver.base_lr - solver.min_lr) *  # pylint: disable=assignment-from-no-return
                                           (1 - iter_var % solver.stepsize/solver.stepsize) + solver.min_lr,  # decreasing from max_lr to base
                              (solver.base_lr - solver.min_lr) *
                              (iter_var % solver.stepsize / solver.stepsize) + solver.min_lr)

            is_zero = T.eq(switch_flag, 0)  # pylint: disable=assignment-from-no-return
            is_iter_end = T.eq(iter_var % solver.stepsize, 0)  # pylint: disable=assignment-from-no-return
            result.append((switch_flag, ifelse(is_iter_end, ifelse(is_zero, 1, 0), switch_flag.astype('int8'))))
            result.append((self._base_lr, switch))
        else:
            raise NotImplementedError("Not implemented policy {0}".format(solver.lr_policy))
        return result

    def build_test(self, solver, **kwargs):
        "Building test model"
        inputs = [self.input_vars[name] for name in self.inputs]
        test_model = theano.function(inputs=inputs,
                                     outputs=self.outputs, **kwargs)
        return test_model

    def add_data_source(self, name, data_source):
        self.data_sources[name] = data_source

    def has_input_variable(self, name):
        return name in self.input_vars

    def __init__(self, net, phase, weights=None, shared_builder=None):
        self.net = net

        # layer_name -> Top
        self.tops = OrderedDict()

        # layer_name -> LayerBuilder
        self.layers = OrderedDict()
        self.loaded = OrderedDict()
        if weights is not None:
            self.loaded = weights
        self.input_vars = OrderedDict()
        self.current_phase = phase
        self.shared_builder = shared_builder
        self.outputs = OrderedDict()
        self.data_sources = OrderedDict()
        self.loss = None
        self.accuracy = None
        self.inputs = list()
        self.input_shapes = OrderedDict()
        self._test_func = None
        self._train_func = None
        self._base_lr = None
        self.label_name = None

    def label_shape(self):
        return self.input_shapes[self.label_name]

    def has_label(self):
        return self.label_name is not None

    def transform_multilabel(self, items):
        expected_shape = self.label_shape()
        result = np.zeros(expected_shape, theano.config.floatX)
        for i, item in enumerate(items):
            result[i][item] = 1
        return result

    def get_source(self):
        for source in self.data_sources.values():
            return source

    def get_batch(self):
        for source in self.data_sources.values():
            if self.has_label() and 1 < len(self.label_shape()):
                data, label = source.get_batch()
                label = self.transform_multilabel(label)
                return data, label
            else:
                data = source.get_batch()
                return data

    def has_loss(self):
        return self.loss is not None

    def get_current_phase(self):
        return self.current_phase

    def __call__(self, **inputs) -> OrderedDict:
        """
        Build new computation, with replaced input layer

        Parameters
        __________
        inputs: OrderedDict[str] -> Tensor
        inputs to computation

        Returns
        -------
        OrderedDict[name] -> simbolic variable(s) representing output
        """
        if not self.layers:
            self.build()
        new_builder = Builder(self.net, self.current_phase, weights=None, shared_builder=self)
        new_builder.load_layers()
        for (name, variable) in inputs.items():
            new_builder.layers[name].set_input(variable)
        new_builder.build()
        #assert self.get_shared() == new_builder.get_shared()
        return new_builder.outputs

    def load_layers(self):
        net = self.net
        tops = self.tops
        layers = self.layers
        loaded = self.loaded
        shared = OrderedDict()
        random_state = numpy.random.RandomState(23455)
        if self.shared_builder is not None:
            shared = self.shared_builder.get_shared()
        # todo: maybe it is better to make LayersWithWeights to request shared weights from the builder
        if hasattr(net, 'input') and len(net.input) != 0:
            assert len(net.input) == 1
            name = net.input[0]
            # InferedParams(name, 'Input', input_dim=self.net.input_dim)
            layer_param = self.input_to_layer_param(self.net.input_dim, name)
            layers[name] = InputLayer(layer_param, builder=self)
            tops[name] = Top(layers[name].tops[0], self)
            tops[name].add_writer(name)

        for layer in net.layer:
            print("reading layer {0}".format(layer.name))
            if hasattr(layer, 'include'):
                phases = [x.phase for x in layer.include]
                # if not empty and current phase not in phases
                if len(phases) != 0 and self.get_current_phase() not in phases:
                    print("skipping layer {0}".format(layer.name))
                    continue
            for top in layer.top:
                if top not in tops:
                    print ("adding top {0}".format(top))
                    tops[top] = Top(top, self)
                tops[top].add_writer(layer.name)
            print (layer.name)
            assert layer.name not in layers
            if layer.type == "Convolution":
                layers[layer.name] = ConvolutionLayerBuilder(layer, random_state, loaded.get(layer.name, None), builder=self,
                                                             shared_weights=shared.get(layer.name, None))
            elif layer.type == 'ReLU':
                layers[layer.name] = ReLULayerBuilder(layer, builder=self)
            elif layer.type == 'SeLU':
                layers[layer.name] = SeLULayerBuilder(layer, builder=self)
            elif layer.type == 'ELU':
                layers[layer.name] = ELULayerBuilder(layer, builder=self)
            elif layer.type == "Pooling":
                layers[layer.name] = PoolingLayerBuilder(layer, builder=self)
            elif layer.type == "ImageData":
                layers[layer.name] = get_image_data_layer_builder(layer, builder=self)
            elif layer.type == "Expression":
                layers[layer.name] = ExpressionLayerBuilder(layer, builder=self)
            elif layer.type == "Sigmoid":
                layers[layer.name] = SigmoidLayerBuilder(layer, builder=self)
            elif layer.type == 'TanH':
                layers[layer.name] = TanHLayerBuilder(layer, builder=self)
            elif layer.type == "SoftmaxWithLoss":
                layers[layer.name] = SoftmaxWithLossLayerBuilder(layer, builder=self)
                assert self.loss is None
                self.loss = layers[layer.name]
            elif layer.type == "SigmoidCrossEntropyLoss":
                layers[layer.name] = SigmoidCrossEntropyLossLayerBuilder(layer, builder=self)
                assert self.loss is None
                self.loss = layers[layer.name]
            elif layer.type == "Accuracy":
                layers[layer.name] = AccuracyLayerBuilder(layer, builder=self)
                self.accuracy = layers[layer.name]
            elif layer.type == "Concat":
                layers[layer.name] = ConcatLayerBuilder(layer, builder=self)
            elif layer.type == "Dropout":
                layers[layer.name] = DropoutLayerBuilder(layer, builder=self)
            elif layer.type == 'Softmax':
                layers[layer.name] = SoftmaxLayerBuilder(layer, builder=self)
            elif layer.type == 'SortLoss':
                layers[layer.name] = SortLossLayerBuilder(layer, builder=self)
                assert self.loss is None
                self.loss = layers[layer.name]
            elif layer.type == 'CrossEntropyLoss':
                layers[layer.name] = CrossEntropyLossLayerBuilder(layer, builder=self)
                assert self.loss is None
                self.loss = layers[layer.name]
            elif layer.type == 'InnerProduct':
                layers[layer.name] = InnerProductLayerBuilder(layer, random_state, loaded.get(layer.name, None), builder=self,
                                                              shared_weights=shared.get(layer.name, None))
            elif layer.type == 'Input':
                layers[layer.name] = InputLayer(layer, builder=self)
            elif layer.type == 'Maxout':
                layers[layer.name] = MaxoutLayerBuilder(layer, builder=self)
            else:
                print("No type {0}".format(layer.type))
                assert False
            for bot in layer.bottom:
                if bot in tops:
                    tops[bot].add_reader(layer)

    def build(self):
        if not self.layers:
            self.load_layers()

        for (key, item) in self.tops.items():
            if item.reader_count == 0:
                self.outputs[item.name] = item.build()

        for layer in self.layers.values():
            layer.calculate_drop()

    @staticmethod
    def input_to_layer_param(input_dim, name):
        layer_param = fire_pb2.LayerParameter()
        layer_param.input_param.shape.add()   # pylint: disable=no-member
        layer_param.top.append(name)          # pylint: disable=no-member
        for d in input_dim:
            layer_param.input_param.shape[0].dim.append(d)   # pylint: disable=no-member
        return layer_param

    def save_net(self, prefix, iteration):
        save_net(self.layers, prefix, iteration)

    def get_shared(self):
        shared = OrderedDict()
        for (name, layer) in self.layers.items():
            if isinstance(layer, LayerBuilderWithWeights):
                shared[name] = layer.get_shared()
        return shared

    def get_weights(self):
        return {key: [v.get_value(borrow=False) for v in value] for (key, value) in self.get_shared().items()}

    def set_weights(self, weights):
        shared = self.get_shared()
        for key, value in weights.items():
            for i, w in enumerate(value):
                shared[key][i].set_value(w)

    def get_learning_rates(self, name):
        return self.layers[name].get_learning_rates()

    def get_base_learning_rate(self):
        return self._base_lr

    def number_of_parameters(self):
        if not self.layers:
            self.load_layers()
        result = OrderedDict()
        for layer_id, layer in self.layers.items():
            if isinstance(layer, LayerBuilderWithWeights):
                result[layer_id] = layer.number_of_parameters()
        return result


def save_net(layers, prefix, iteration):
    to_save = OrderedDict()
    for layer in layers:
        if isinstance(layers[layer], LayerBuilderWithWeights):
            to_save[layer] = layers[layer].get_weights()

    with open('{0}-{1}.dat'.format(prefix, iteration), 'wb') as outfile:
        pickle.dump(to_save, outfile, protocol=pickle.HIGHEST_PROTOCOL)
