import theano
import theano.tensor as T
import numpy
import pickle
import time
import itertools
from concurrent.futures import ThreadPoolExecutor

from conv_layer import LeNetConvPoolLayer
import common
import learning


WEIGHTS_DIR = '/run/media/leron/KINGSTON/DeepLearningTutorials/weights/'
WEIGHTS_DIR = '../weights6/'


def prepare_datasets():
    dict_files = pickle.load(open('file_dict.save', 'rb'))


def evaluate_conv(ishape, learning_rate=0.00001, n_epochs=40,
                        nkerns=[30, 30, 50, 50, 50], batch_size=100, padding=0):
    """ Demonstrates lenet on MNIST dataset

    :type learning_rate: float
    :param learning_rate: learning rate used (factor for the stochastic
                          gradient)

    :type n_epochs: int
    :param n_epochs: maximal number of epochs to run the optimizer

    :type dataset: string
    :param dataset: path to the dataset used for training /testing (MNIST here)

    :type nkerns: list of ints
    :param nkerns: number of kernels on each layer
    """

    rng = numpy.random.RandomState(23455)

    directory = '../../K'

    base_shape = ishape

    shapes = itertools.cycle(common.linspace_image_sizes(base_shape, 1, 2.2, 18))
    iterator = common.get_iterator(directory, 2000, cut_target=True, grayscale=False)
    pool = ThreadPoolExecutor(max_workers=1)
    next(iterator)
    shape = next(shapes)
    dataset = iterator.send(shape)

    train_set_x, train_set_y_shared = common.shared_dataset(dataset[0])
    train_set_y = T.cast(train_set_y_shared, 'int32')

    test_set_x, test_set_y_shared = common.shared_dataset(dataset[1])
    test_set_y = T.cast(test_set_y_shared, 'int32')

    # compute number of minibatches for training, validation and testing
    n_train_batches = train_set_x.get_value(borrow=True).shape[0]
    #n_valid_batches = valid_set_x.get_value(borrow=True).shape[0]
    n_test_batches = test_set_x.get_value(borrow=True).shape[0]
    n_train_batches //= batch_size
    #n_valid_batches /= batch_size
    n_test_batches //= batch_size

    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch
    index.tag.test_value = 1
    x = T.ftensor4('x')
    x.tag.test_value = numpy.random.random((batch_size, 3, ishape[0] * 2, ishape[1] * 2)).astype(theano.config.floatX)   # the data is presented as rasterized images
    y = T.ivector('y')
    y.tag.test_value = numpy.random.randint(0, 2, size=batch_size).astype(numpy.int32)  # the labels are presented
                                                                                       # as 1D vector of [int] labels

    ######################
    # BUILD ACTUAL MODEL #
    ######################
    print ('... building the model')

    layers = []
    # Reshape matrix of rasterized images of shape (batch_size,640*480)
    # to a 4D tensor, compatible with our LeNetConvPoolLayer
    layer0_input = x #= x.reshape((batch_size, 3, row, col))

    # Construct the first convolutional pooling layer:
    # filtering reduces the image size to (480-15+1,640-15+1)=(466,626)
    # maxpooling reduces this further to (466/2,626/2) = (233,313)
    # 4D output tensor is thus of shape (batch_size,nkerns[0],233,313)
    layer0 = LeNetConvPoolLayer(rng, input=layer0_input,
            image_shape=(batch_size, 3, None, None),
            filter_shape=(nkerns[0], 3, 3, 3),
            poolsize=None,
            stride=(1, 1),
            )

    layers.append(layer0)
    layer0.output.name = 'layer0_out'

    layer1 = LeNetConvPoolLayer.build_layer(rng, layer0,
            filter_shape=(nkerns[1], nkerns[0], 2, 2), poolsize=None, border='full')

    layers.append(layer1)

    layer1.output.name = 'layer2_input'
    layer2 = LeNetConvPoolLayer.build_layer(rng, layer1,
            filter_shape=(nkerns[2], nkerns[1], 2, 2), poolsize=(2,2),
            border='full')

    layers.append(layer2)

    layer2.output.name = 'layer3_input'

    layer3 = LeNetConvPoolLayer.build_layer(rng, layer2,
            filter_shape=(nkerns[3], nkerns[2], 2, 2), poolsize=None,
            border='full')

    layers.append(layer3)

    layer4 = LeNetConvPoolLayer.build_layer(rng, layer3,
        filter_shape=(nkerns[4], nkerns[3], 2, 2), poolsize=None,
        border='full')

    layers.append(layer4)
    hidden_size = 30


    # construct a fully-connected sigmoidal layer
    #row5, col5 = layer4.get_output_shape()
    row5, col5 = 17,17#layers[-1].get_output_shape()
    layer5 = LeNetConvPoolLayer.build_layer(rng, layer4,
                               filter_shape=(hidden_size, nkerns[4], row5, col5),
                               poolsize=None)

    layers.append(layer5)

    # classify the values of the fully-connected sigmoidal layer
    layer6 = LeNetConvPoolLayer.build_layer(rng, layer5,
                                filter_shape=(2, hidden_size, 1, 1),
                                poolsize=None)

    layers.append(layer6)


    # load weights

    layers_src = common.load_layers(WEIGHTS_DIR)
    common.copy_weights(layers_src, layers)
    del layers_src
    L1_reg=0.00001
    L2_reg=0.00000001

    reg = T.sum([x.reg(L1_reg, L2_reg) for x in layers])


    # create a function to compute the mistakes that are made by the model
    test_model = theano.function([index], layers[-1].errors(y),
            givens={
                 x: test_set_x[index * batch_size: (index + 1) * batch_size],
                 y: test_set_y[index * batch_size: (index + 1) * batch_size]
                 }
                 )
    evaluete_map = theano.function([x], layers[-1].p_y_given_x)
    evaluete = theano.function([x], layers[-1].downsample_prob)


    # create a list of all model parameters to be fit by gradient descent
    params = []
    for l in layers:
       params += l.params

    # the ciost we minimize during training is the NLL of the model
    cost = layers[-1].negative_log_likelihood(y) + reg
    #cost = layers[-1].binary_cross_entropy(y) + reg

    # create a list of gradients for all model parameters
    grads = T.grad(cost, params)

    # train_model is a function that updates the model parameters by
    # SGD Since this model has many parameters, it would be tedious to
    # manually create an update rule for each model parameter. We thus
    # create the updates list by automatically looping over all
    # (params[i],grads[i]) pairs.

#    updates = []
#    for param_i, grad_i in zip(params, grads):
#        updates.append((param_i, param_i - learning_rate * grad_i))

    updates = learning.rmsprop_updates(decay_rate=0.99, learning_rate=learning_rate, params=params, grads=grads)

    train_model = theano.function([index], cost, updates=updates,
      givens={
        x: train_set_x[index * batch_size: (index + 1) * batch_size],
        y: train_set_y[index * batch_size: (index + 1) * batch_size]},
        )
    ###############
    # TRAIN MODEL #
    ###############
    print ('... training')

    best_params = None
    best_validation_loss = numpy.inf
    best_iter = 0
    test_score = 0.
    start_time = time.clock()

    epoch = 0
    done_looping = False

    test_losses_best = numpy.finfo(numpy.float32).max
    test_loss_list = []
    while (epoch < n_epochs) and (not done_looping):
        epoch = epoch + 1

        next(iterator)
        next_shape = next(shapes)
        data_generation = pool.submit(iterator.send, next_shape)
        for minibatch_index in range(n_train_batches):

            iter = epoch * n_train_batches + minibatch_index

            if iter % 100 == 0:
                print ('training @ iter = ', iter)
            print ("minibatch_index = %d" % minibatch_index)
            print ("-----                                 shape {} ".format(shape))
            #print (test_model(1))
            if minibatch_index % 7 == 0:
                test_losses = numpy.mean([test_model(i) for i in range(n_test_batches)])
                if test_losses < test_losses_best:
                    pass
                    #common.save_layers(layers, WEIGHTS_DIR)
                test_losses_best = test_losses
                test_loss_list.append(test_losses)
                print(('     epoch %i, minibatch %i/%i, test error of best '
                       'model %f %%') %
                      (epoch, minibatch_index + 1, n_train_batches,
                       test_losses * 100.))
            minibatch_avg_cost = train_model(minibatch_index)
            print(minibatch_avg_cost)


        dataset = data_generation.result()
        train_set_x.set_value(dataset[0][0])
        train_set_y_shared.set_value(dataset[0][1])

        test_set_x.set_value(dataset[1][0])
        test_set_y_shared.set_value(dataset[1][1])
        shape = next_shape

    import pdb;pdb.set_trace()
    import scipy.misc
    test_matrix = test_set_x.get_value()
    for i in range(35):
        temp = numpy.copy(test_matrix)
        for i in range(test_matrix.shape[0]):
            row = test_matrix[i]
            row_rotated = scipy.misc.imrotate(row.reshape(get_optimal_shape(row.size)), i)
            temp[i] = row_rotated.reshape((row.size))
        test_set_x.set_value(temp)
        test_losses = [test_model(i) for i in xrange(n_test_batches)]
        test_score = numpy.mean(test_losses)
        print(('     angle %i, test error of best '
               'model %f %%') %
              (i,test_score * 100.))


    end_time = time.clock()
    print('Optimization complete.')
#    print('Best validation score of %f %% obtained at iteration %i,'\
#          'with test performance %f %%' %
#          (best_validation_loss * 100., best_iter, test_score * 100.))
    print >> sys.stderr, ('The code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((end_time - start_time) / 60.))


if __name__ == '__main__':
    theano.config.compute_test_value = 'raise'
    theano.config.floatX = 'float32'
    theano.config.mode = 'FAST_COMPILE'
    theano.config.optimizer = 'None'
    evaluate_conv(ishape=(30, 30))
