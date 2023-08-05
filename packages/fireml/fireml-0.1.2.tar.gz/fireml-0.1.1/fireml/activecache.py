import abc
import threading


class ActiveCache:
    def __init__(self):
        self._thread = None

    def get_batch(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self._get_batch)
            self._thread.start()
        self._thread.join()
        result = self._get_data()
        assert result is not None
        self._thread = threading.Thread(target=self._get_batch)
        self._thread.start()
        return result

    @abc.abstractmethod
    def _get_batch(self):
        pass

    @abc.abstractmethod
    def _get_data(self):
        pass
