import theano.tensor as T


class ConcatLayer:
    def __init__(self, inputs):
        self.inputs = inputs
        self.output = T.concatenate(self.inputs, axis=1)
