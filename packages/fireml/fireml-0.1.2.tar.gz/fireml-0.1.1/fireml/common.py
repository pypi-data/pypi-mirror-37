#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import shutil
import pickle
import os
import random
import theano
from scipy import misc
import math
from PIL import Image
from collections import Iterable
from theano import tensor as T


# http://stackoverflow.com/questions/34876585/pythonic-way-to-round-like-javascript-math-round/34876996
def roundthemnumbers(value):
    x = math.floor(value)
    if (value - x) < .50:
        return x
    else:
        return math.ceil(value)


def calculate_conv_size(input_size, filter_size, padding, stride, border='valid'):
    """returns result image size"""

    result = []
    for i in range(min(len(input_size), 2)):
        if border == 'valid':
            result.append((input_size[i] - filter_size[i] + 1 + 2 * padding[i]) / stride[i])
        elif border == 'full':
            assert padding[i] == 0
            result.append((input_size[i] + filter_size[i] - 1 + 2 * padding[i]) / stride[i])
    return [roundthemnumbers(x) for x in result]


def calculate_pool_size(input_size, filter_size, padding, stride, ignore_border):
    """returns result image size"""

    result = []
    for i in range(min(len(input_size), 2)):
        if ignore_border:
            result.append((input_size[i] - filter_size[i] + 1 + 2 * padding[i]) / stride[i])
        else:
            result.append((input_size[i] + filter_size[i] - 1 + 2 * padding[i]) / stride[i])
            assert padding[i] == 0
    return [math.ceil(x) for x in result]


def shared_dataset(data_xy, borrow=True):
    """ Function that loads the dataset into shared variables

    The reason we store our dataset in shared variables is to allow
    Theano to copy it into the GPU memory (when code is run on GPU).
    Since copying data into the GPU is slow, copying a minibatch everytime
    is needed (the default behaviour if the data is not in a shared
    variable) would lead to a large decrease in performance.
    """
    data_x, data_y = data_xy
    shared_x = theano.shared(numpy.asarray(data_x,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    shared_y = theano.shared(numpy.asarray(data_y,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    # When storing data on the GPU it has to be stored as floats
    # therefore we will store the labels as ``floatX`` as well
    # (``shared_y`` does exactly that). But during our computations
    # we need them as ints (we use labels as index, and if they are
    # floats it doesn't make sense) therefore instead of returning
    # ``shared_y`` we will have to cast it to int. This little hack
    # lets ous get around this issue
    return shared_x, shared_y


def save_layers(layers, directory):
    """writes layers using pickle in separate files in directory
    alongside list.txt with layers list"""

    txt_list = []
    if not os.path.exists(directory):
        os.makedirs(directory)
    i = 0
    for layer in layers:
        layer_name = 'layer' + str(i) + '.save'
        tmp = '/tmp'
        with open(os.path.join(tmp, layer_name), 'wb') as f:
            pickle.dump(layer, f, protocol=pickle.HIGHEST_PROTOCOL)
            dir_path = os.path.join(directory, layer_name)
            if os.path.exists(dir_path):
                shutil.move(dir_path, dir_path + '.old')
            shutil.move(os.path.join(tmp, layer_name), dir_path)
        txt_list.append(layer_name)
        i += 1
    with open(os.path.join(directory, 'list.txt'), 'wt') as f:
        for l in txt_list:
            f.write(l + '\n')


def load_layers(directory):
    layers = []
    txt_list = [s.strip() for s in open(os.path.join(directory, 'list.txt'), 'rt').readlines()]
    for layer_name in txt_list:
        with open(os.path.join(directory, layer_name), 'rb') as f:
            layers.append(pickle.load(f))
    return layers


def rgb2gray(rgb):
    return numpy.dot(rgb[...,:3], [0.299, 0.587, 0.144])


def linspace_image_sizes(base_size, lower_scale, upper_scale,  count):
    """
    base_size - image size (rows, cols)
    count  - count of samples
    """
    pairs_list = list(zip(*[numpy.linspace(x//lower_scale, x * upper_scale, num=count) for x in base_size]))
    return numpy.asarray(pairs_list, dtype=numpy.int32)


def copy_weights(layers_src, layers_target):
    assert len(layers_src) == len(layers_target)
    for src, target in zip(layers_src, layers_target):
        if target.W.get_value(borrow=True).shape != src.W.get_value(borrow=True).shape:
            continue
        target.W.set_value(src.W.get_value(borrow=False))
        target.b.set_value(src.b.get_value(borrow=False))


def cut_region(image, rect):
    """returns part of image defined by rect

    rect is 4-tuple: (x, y, width, height) where x, y is top left corner
    """
    x, y, width, height = rect
    assert(x + width < image.shape[1])
    assert(y + height < image.shape[0])
    return image[y: y + height, x: x + width, :]


def zero_pad(image, expected_size):
    """
    image - image with shape (rows, cols, channels)
    expected_size - tuple of size (new_rows, new_cols
    """

    result = image
    for index, value in enumerate(result.shape[0:2]):
        size_to_pad = expected_size[index] - value
        res_index = index - 1 if index else index + 1
        padding = numpy.zeros(size_to_pad * result.shape[res_index] * min(result.shape), dtype=int)
        if index == 0: # height
            padding = padding.reshape(size_to_pad, result.shape[res_index], min(result.shape))
        else:
            padding = padding.reshape(result.shape[res_index], size_to_pad, min(result.shape))
        r = numpy.random.randint(0, 2)
        if size_to_pad:
            if r: # padding from random side
                result = numpy.concatenate([result, padding], axis=index)
            else:
                result = numpy.concatenate([padding, result], axis=index)
    assert result.shape[0] == expected_size[0]
    assert result.shape[1] == expected_size[1]
    return result


def calculate_product_shape(input_shape, n_out):
    result = list(input_shape)
    result[-1] = n_out
    return result


def resize(image, expected_size):
    maxwidth, maxheight = [float(x) for x in expected_size]
    ratio = min(maxwidth/image.shape[0], maxheight/image.shape[1])
    result = misc.imresize(image, (int(image.shape[0] * ratio), int(image.shape[1] * ratio)))
    return result


def resize_and_zero_pad(image, expected_size):
    result = resize(image, expected_size)
    return zero_pad(result, expected_size)


def reverse_transpose(im_tr):
    """converts from (x, y, 3) to pylab's (3, x, y)"""
    return im_tr.transpose(1, 2, 0)


def transpose(im):
    """converts from (x, y, 3) to pylab's (3, x, y)"""
    if len(im.shape) == 2:
        return im.reshape([1,] + list(im.shape))
    return im.transpose(2, 0, 1)


def get_datset_dicts(with_car_dict, without_car_dict):

    # pairs [with_car, without_car]
    test_set = [{}, {}]
    train_set = [{}, {}]
#    validation_set = [{}, {}]
    for i, d in enumerate((with_car_dict, without_car_dict)):
        length = len(d)
        train_set_l = int(length * 0.9)
#        test_set_l = int(length * 0.9)
        #validation_set_l = length

        counter = 0
        for key, value in d.items():
            if counter < train_set_l:
                train_set[i][key] = value
#            elif counter < test_set_l:
#                test_set[i][key] = value
            else:
                #validation_set[i][key] = value
                test_set[i][key] = value
            counter += 1
    return test_set, train_set#, validation_set


def get_iterator(directory, size, cut_target, grayscale):
    directory = os.path.abspath(directory)
    dict_files = pickle.load(open(os.path.join(directory, 'file_dict.save'), 'rb'))

    with_car_dict = dict_files['false']['with_car']
    with_car_dict.update(dict_files['false']['with_car'])
    without_car_dict = dict_files['true']['without_car']

    train_dicts, test_dicts = get_datset_dicts(with_car_dict, without_car_dict)

    image_dir = directory + '/images'
    image_size = yield
    train_set = gen_dataset(image_dir, train_dicts[0], train_dicts[1], size - (1 * size // 10), image_size, cut_target, grayscale)
    test_set = gen_dataset(image_dir, test_dicts[0], test_dicts[1], size // 10, image_size, cut_target, grayscale)
    # validation_set = gen_dataset(image_dir, validation[0], validation[1], size // 10, image_size)

    yield train_set, test_set#, validation_set
    while(True):
        image_size = yield
        #, validation =
        for data in ((train_dicts, train_set, size - (1 * size // 10)), (test_dicts, test_set, size // 10)): #, (validation, validation_set, size // 10)):
            cars_dicts = data[0]
            # data[2] - size of set
            x_values, y_values = gen_dataset(image_dir, cars_dicts[0], cars_dicts[1], data[2], image_size, cut_target, grayscale)
            # data[1] - (inputs, targets)
            data[1][0] = x_values
            data[1][1] = y_values
        yield train_set, test_set#, validation_set


def gen_dataset(top_dir, with_car, without_car, count, target_image_size, cut_target=False, grayscale=True):
    """generates list of key value pairs,
    with key being and image, and value is floating point value

    file_dict - dict({'true': {'with_car':{'file0.jpg':[rect_coords]...
    count     - expected size of dataset
    target_image_size - size of images in target dataset
    cut_target - boolean - True if need to cut target patches
    grayscale - boolean - True - default - if need to convert to grayscale
    """

    flag = True
    result = [[], []]
    # devide becouse adding mirror image
    for i in range(count // 2):
        if flag:
            path = random.choice([x for x  in with_car.keys()])
            im = misc.imread(os.path.join(top_dir, path))
            rect = random.choice(with_car[path])
        else:
            path = random.choice([x for x in without_car.keys()])
            im = misc.imread(os.path.join(top_dir, path))
            h = w = numpy.random.randint(27, 200)
            heigth, width, z = im.shape
            rect = [numpy.random.randint(0, width - w - 1),
                    numpy.random.randint(0, heigth - h - 1),
                    h,
                    w,]
        # to do: change cut region to use different sizes


 #       plt.imshow(im);
 #       plt.show()
        if cut_target:
            im = cut_region(im, rect)

   #        plt.imshow(im);
   #        plt.show()
        im = resize_and_zero_pad(im, target_image_size)
        if grayscale:
            im = rgb2gray(im)

        result[0].append(transpose(im))
        result[0].append(transpose(numpy.fliplr(im)))
        if flag: # with car
            result[1] += [1, 1]
        else: # without car
            result[1] += [0, 0]
        flag = not flag
    return [numpy.asarray(result[0], dtype=theano.config.floatX) / 255, numpy.asarray(result[1], dtype='float32')]


def test():
    directory = "../../Конкурс/"
    directory = os.path.abspath(directory)
    image_size = (128, 128)
    iter = get_iterator(directory, 1000, image_size)
    next(iter)


def scale(image, new_width, new_height, method=Image.ANTIALIAS):
    """
    Vlad Mis'ko implementation of resize, depends on PIL
    """
    height = 1
    width = 0
    if isinstance(image, numpy.ndarray):
        image = Image.fromarray(image)
    if new_width == image.size[width] and new_height == image.size[height]:
        return image
    im_aspect = float(image.size[width])/float(image.size[1])
    out_aspect = float(new_width)/float(new_height)
    if im_aspect >= out_aspect:
        scaled = image.resize((new_width, int((float(new_width)/im_aspect) + 0.5)), method)
    else:
        scaled = image.resize((int((float(new_height)*im_aspect) + 0.5), new_height), method)

    offset = (((new_width - scaled.size[width]) // 2), ((new_height - scaled.size[height]) // 2))
    back = Image.new("RGB", (new_width, new_height), "black")
    back.paste(scaled, offset)
    return back


def mean_substraction(image, mean_pixel=numpy.array([104.008, 116.669, 122.675])):
    image = numpy.array(image)
    H, W, _ = image.shape
    image = image[:, :, [2, 1, 0]]
    image = image - mean_pixel
    return image


def iterative_mean(current, new, t):
    return current + 1.0/t  * (new - current)


def _flatten(lst, acc=None):
    if acc is None:
        acc = []
    if isinstance(lst, Iterable):
        # some of theano types are iterable but
        # does not support iteration o_o
        try:
            for item in lst:
                _flatten(item, acc=acc)
        except (TypeError, ValueError) as e:
            acc.append(lst)
    else:
        acc.append(lst)

def flatten(lst):
    result = []
    _flatten(lst, result)
    return result


def get_expanded_dim(a, i):
    """
    Equivalent to numpy.indices(a)[i]
    """
    index_shape = [1] * a.ndim
    index_shape[i] = a.shape[i]
    result = T.ones_like(a)
    index_val = T.arange(a.shape[i]).reshape(index_shape)
    return index_val * result


def get_argmax_indices(a, axis):
    """
    Calculates indices which can be used to apply result of a.argsort(axis=axis) to get a.max(axis=axis).

    """

    idx = a.argmax(axis=axis)
    indices = []
    axis_data = axis + a.ndim if axis < 0 else axis
    for i in range(idx.ndim):
        if i == axis:
            indices.append(idx)
        indices.append(get_expanded_dim(idx, i))
    return tuple(indices)


if __name__ == '__main__':
    test()
