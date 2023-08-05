import theano
import theano.tensor as T
import numpy as np


def rmsprop_updates(decay_rate, learning_rate, params, grads):
    assert 0 < decay_rate < 1
    updates = []
    for param_i, grad_i in zip(params, grads):
        cache_i = theano.shared(param_i.get_value(borrow=True) * 0.0)
        cache_i_new =  cache_i * decay_rate + (1 - decay_rate) * grad_i ** 2
        updates.append((cache_i, cache_i_new))
        updates.append((param_i, param_i - learning_rate * \
                       (grad_i / T.sqrt(cache_i_new + 1e-8))))
    return updates


def gradient_updates_momentum(grads, weights, lr_mults, base_lr, momentum):
    '''
    Compute updates for gradient descent with momentum

    :parameters:
        - weights : list of theano.tensor.var.TensorVariable
            Parameters to compute gradient against
        - bas_lr : float
            Gradient descent learning rate
        - momentum : float
            Momentum parameter, should be at least 0 (standard gradient descent) and less than 1

    :returns:
        updates : list
            List of updates, one for each parameter
    '''
    # Make sure momentum is a sane value
    assert momentum < 1 and momentum >= 0
    # List of update steps for each parameter
    updates = []

    # Just gradient descent on cost
    for w, lr, grad_i in zip(weights, lr_mults, grads):

        # For each parameter, we'll create a previous_step shared variable.
        # This variable will keep track of the parameter's update step across iterations.
        # We initialize it to 0
        previous_step = theano.shared(w.get_value()*0., broadcastable=w.broadcastable)
        # Each parameter is updated by taking a step in the direction of the gradient.
        # However, we also "mix in" the previous step according to the given momentum value.
        step = momentum * previous_step + base_lr * lr * grad_i
        step.name = 'step'
        # Add an update to store the previous step value
        updates.append((previous_step, step))
        # Add an update to apply the gradient descent step to the parameter itself
        updates.append((w, w - step))
    return updates


def nesterov_momentum_simplified(grads, weights, lr_mults, base_lr, alpha):
    """
    Simplified update equations from ADVANCES IN OPTIMIZING RECURRENT NETWORKS (Y. Bengio, N. Boulanger-Lewandowski,
    Razvan Pascanu)


    Parameters
    ----------
    grads
        Gradients w.r.t weights.
    weights
        Wights - shared variable.
    lr_mults
        Iterable of learing rate for each element of weights
    base_lr
        Base learning rate. Learing rate used in updates equals base_lr * lr_mults[i]
    alpha
        Paramere in (0, 1) - determines how much of previous velocity to retain:
        new  velocity = current * alpha + lr * grad
    Returns
    -------
    None
    """
    # Make sure momentum is a sane value
    assert alpha < 1 and alpha > 0
    # List of update steps for each parameter
    updates = []

    # Just gradient descent on cost
    for w, lr, grad_i in zip(weights, lr_mults, grads):

        # For each parameter, we'll create a previous_step shared variable.
        # This variable will keep track of the parameter's update step across iterations.
        # We initialize it to 0
        velocity = theano.shared(w.get_value(borrow=False)*0., broadcastable=w.broadcastable)

        updates.append((w, w + alpha * alpha * velocity - (1 + alpha) * base_lr * lr_mults * grad_i))
        # update velocity
        updates.append((velocity, alpha * velocity - base_lr * lr_mults * grad_i ))
    return updates


def nesterov_momentum(grads, weights, lr_mults, base_lr, alpha):
    # Make sure momentum is a sane value
    assert alpha < 1 and alpha >= 0
    # List of update steps for each parameter
    updates = []

    # Just gradient descent on cost
    for w, lr, grad_i in zip(weights, lr_mults, grads):

        # For each parameter, we'll create a previous_step shared variable.
        # This variable will keep track of the parameter's update step across iterations.
        # We initialize it to 0
        velocity = theano.shared(w.get_value(borrow=False)*0., broadcastable=w.broadcastable)
        w_actual = theano.shared(w.get_value(borrow=False), broadcastable=w.broadcastable)

        # set w to test value - test at distance (velocity * a)
        updates.append((w, w_actual + velocity * alpha ))
        # update weights - move at larger distance according to velocity
        updates.append((w_actual, w_actual + velocity))
        # update velocity
        updates.append((velocity, alpha * velocity - base_lr * lr_mults * grad_i ))
    return updates


# https://gist.github.com/kastnerkyle/816134462577399ee8b2
class rmsprop_nesterov(object):
    """
    RMSProp with nesterov momentum and gradient rescaling
    """
    def __init__(self, params):
        self.running_square_ = [theano.shared(np.zeros_like(p.get_value()))
                                for p in params]
        self.running_avg_ = [theano.shared(np.zeros_like(p.get_value()))
                             for p in params]
        self.memory_ = [theano.shared(np.zeros_like(p.get_value()))
                        for p in params]

    def updates(self, params, grads, learning_rate, momentum, rescale=5.):
        grad_norm = T.sqrt(sum(map(lambda x: T.sqr(x).sum(), grads)))
        not_finite = T.or_(T.isnan(grad_norm), T.isinf(grad_norm))
        grad_norm = T.sqrt(grad_norm)
        scaling_num = rescale
        scaling_den = T.maximum(rescale, grad_norm)
        # Magic constants
        combination_coeff = 0.9
        minimum_grad = 1E-4
        updates = []
        for n, (param, grad) in enumerate(zip(params, grads)):
            grad = T.switch(not_finite, 0.1 * param,
                            grad * (scaling_num / scaling_den))
            old_square = self.running_square_[n]
            new_square = combination_coeff * old_square + (
                1. - combination_coeff) * T.sqr(grad)
            old_avg = self.running_avg_[n]
            new_avg = combination_coeff * old_avg + (
                1. - combination_coeff) * grad
            rms_grad = T.sqrt(new_square - new_avg ** 2)
            rms_grad = T.maximum(rms_grad, minimum_grad)
            memory = self.memory_[n]
            update = momentum * memory - learning_rate * grad / rms_grad
            update2 = momentum * momentum * memory - (
                1 + momentum) * learning_rate * grad / rms_grad
            updates.append((old_square, new_square))
            updates.append((old_avg, new_avg))
            updates.append((memory, update))
            updates.append((param, param + update2))
        return updates



def dropout(x, p_drop=0.0):
    """
    x - variable to apply dropout
    p_drop - probability of dropping out
    """

    if 0.0 < p_drop and p_drop < 1:
         srng = T.shared_randomstreams.RandomStreams(np.random.randint(100000))
         return T.switch(srng.binomial(size=x.shape, p=p_drop), 0, x)
    return X

