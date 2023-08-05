import sys
import timeit
import numpy
from fireml import common
import os


class Train:
    def __init__(self, train_builder, test_builder, test_interval, max_iter=None,
                 max_epoch=None, save_function=None, snapshot_interval=1000, display=20,
                 average_loss=1, solver=None):
        self.train_builder = train_builder
        self.test_builder = test_builder
        self.train_model = train_builder.theano_function(solver)
        self.test_model = test_builder.theano_function()
        self.max_iter = max_iter
        self.max_epoch = max_epoch
        self.test_interval = test_interval
        self.save_function = save_function
        self.snapshot_interval = snapshot_interval
        self.display = display
        self.n_average = average_loss

    def __call__(self):
        rng = numpy.random.RandomState(23455)

        # compute number of minibatches for training, validation and testing
        n_train_batches = self.train_builder.get_source().n_batches
        test = self.test_model is not None
        if test:
            n_test_batches = self.test_builder.get_source().n_batches
        ###############
        # TRAIN MODEL #
        ###############
        print('... training the model')
        sys.stdout.flush()
        # early-stopping parameters
        patience = 5000  # look as this many examples regardless
        patience_increase = 2  # wait this much longer when a new best is
                                      # found
        improvement_threshold = 0.995  # a relative improvement of this much is
                                      # considered significant
        test_frequency = min(self.test_interval, patience // 2)
        # go through this many
        # minibatche before checking the network
        # on the validation set; in this case we
        # check every epoch

        best_validation_loss = numpy.inf
        test_score = 0.
        start_time = timeit.default_timer()

        done_looping = False
        epoch = 0
        average_loss = -1
        iter = 0
        while ((self.max_epoch is not None and (epoch < self.max_epoch)) or
            (self.max_iter is not None and (iter < self.max_iter))) and (not done_looping):
            epoch = epoch + 1
            for minibatch_index in range(n_train_batches):

                if test and (iter) % test_frequency == 0:
                    # compute zero-one loss on validation set
                    if self.test_builder.has_loss():
                        test_loss_name = self.test_builder.loss.loss_name
                        accuracy_name = None
                        if self.test_builder.accuracy is not None:
                            accuracy_name = self.test_builder.accuracy.name
                        validation_results = [self.test_model(*self.test_builder.get_batch())
                                                 for i in range(n_test_batches)]
                        validation_losses = [v[test_loss_name] for v in validation_results]
                        this_validation_loss = numpy.mean(validation_losses)
                        print(
                            'epoch %i, minibatch %i/%i, validation loss %f ' %
                            (
                                epoch,
                                minibatch_index + 1,
                                n_train_batches,
                                this_validation_loss
                            )
                        )
                        if accuracy_name is not None:
                            accuracy = [v[accuracy_name] for v in validation_results]
                            print("test accuracy: {0} %".format(numpy.mean(accuracy) * 100))
                        # if we got the best validation score until now
                        if this_validation_loss < best_validation_loss:
                            #improve patience if loss improvement is good enough
                            if this_validation_loss < best_validation_loss *  \
                               improvement_threshold:
                                patience = max(patience, iter * patience_increase)

                            test_score = numpy.mean(numpy.mean(accuracy))
                            best_validation_loss = this_validation_loss
                            print(
                                (
                                    '     epoch %i, minibatch %i/%i, test error of'
                                    ' best model %f '
                                ) %
                                (
                                    epoch,
                                    minibatch_index + 1,
                                    n_train_batches,
                                    this_validation_loss
                                )
                            )
                    else:
                        # todo: handle accuracy
                        out = [self.test_model(*self.test_builder.get_batch())
                                                 for i in range(n_test_batches)]
                        # todo: use n_test_batches from solver
                        if 'accuracy' in out[0]:
                            print('Test accuracy: ' + str(numpy.mean([x['accuracy'] for x in out])))
                        print([x for x in out if 'accuracy' not in x])
                    sys.stdout.flush()
                #######################################
                #  training part
                #######################################
                data, labels = self.train_builder.get_batch()
                loss_name = self.train_builder.loss.loss_name
                out = self.train_model(data, labels)
                minibatch_avg_cost =  out[loss_name]
                if average_loss == -1:
                   average_loss = minibatch_avg_cost
                average_loss = common.iterative_mean(average_loss, minibatch_avg_cost, self.n_average)
                iter = (epoch - 1) * n_train_batches + minibatch_index
                current_lr = self.train_builder.get_base_learning_rate().get_value()
                if ( iter + 1 ) % self.display == 0:
                    print ("Iteration {0} Average loss: {1}, lr: {2}".format(iter + 1, average_loss, current_lr))
                    #if minibatch_avg_cost > 2:
                    print ("       Train net output {0}".format(out))
                sys.stdout.flush()
                ######################################
                # end of training part
                ######################################
                if self.snapshot_interval and (iter + 1) % self.snapshot_interval == 0:
                    print("Snapshotting")
                    self.save_function(iteration=iter + 1)
                # todo: add patience to solver settings
                #if patience <= iter:
                #    done_looping = True
                #    print("Not improving, stopping")
                #    break

        end_time = timeit.default_timer()
        print(
            (
                'Optimization complete with best validation score of %f ,'
                'with test performance %f %%'
            )
            % (best_validation_loss , test_score * 100 )
        )
        print('The code run for %d epochs, with %f epochs/sec' % (
            epoch, 1. * epoch / (end_time - start_time)))
        print(('The code for file ' +
               os.path.split(__file__)[1] +
               ' ran for %.1fs' % ((end_time - start_time))), file=sys.stderr)

