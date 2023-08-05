import abc


class DataReader(abc.ABC):

    @property
    def batch_size(self):
        return self._batch_size

    @property
    def size(self):
        return self._size

    @property
    def n_batches(self):
        return self.size // self.batch_size

    @abc.abstractmethod
    def get_batch(self):
        pass
