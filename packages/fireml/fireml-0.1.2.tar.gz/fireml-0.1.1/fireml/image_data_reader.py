import tarfile
import pickle
import threading
import random
from fireml.const import LABEL, IMAGE
from PIL import Image
from fireml import data_reader


class ImageDataReaderBase(data_reader.DataReader):
    def __init__(self, batch_size, processor, shuffle, mirror, mean, equalize_histogram, force_grayscale, scale, standard_params):
        self.items = []
        self._batch_size = batch_size
        self.processor = processor
        self._size = len(self.items)
        self.position = -1
        self.mirror = mirror
        self._cache = dict()
        self.mean = mean
        self.scale = scale
        self.equalize_histogram = equalize_histogram
        self.force_grayscale = force_grayscale
        assert (not (self.equalize_histogram and self.mean))
        self.shuffle = shuffle
        self._thread = None
        self._batch_data = None
        self._standard_params = standard_params

    def _read_from_txt(self, txt_path):
        with open(txt_path, 'rt') as f:
            for line in f:
                tmp = line.strip().replace('  ', ' ').split(' ')
                path, label = tmp[0], tmp[1:]
                label = [int(x) for x in label]
                self.items.append((path, label))
        self._size = len(self.items)

    def get_batch(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self._get_batch)
            self._thread.start()
        self._thread.join()
        result = self._batch_data
        self._thread = threading.Thread(target=self._get_batch)
        self._thread.start()
        return result

    def _get_batch(self):
        size = self.size
        result_im, result_lab = list(), list()
        while len(result_im) < self.batch_size:
            self.position += 1
            if self.position == size:
                self.position = 0
                if self.shuffle:
                    random.shuffle(self.items)
            i = self.position
            if self.items[i][IMAGE] in self._cache:
                image = self._cache[self.items[i][IMAGE]]
                if self.mirror:
                    image = self.processor.mirror(image)
            else:
                image = self._get_image(i)
                image = self.preprocess_image(image)
                self._cache[self.items[i][IMAGE]] = image
            label = self.items[i][LABEL]
            result_im.append(image)
            result_lab.append(label)
        self._batch_data = (result_im, result_lab)

    def preprocess_image(self, image):
        image = self.processor.resize(image)
        if self.mirror:
            image = self.processor.mirror(image)
        if self.force_grayscale:
            image = self.processor.grayscale(image)
        if self.mean or self._standard_params.mean_average:
            image = self.processor.substract(image, self._standard_params.mean_average, self._standard_params.mean_per_channel)
        if self.equalize_histogram:
            image = self.processor.equalize_histogram(image)
        if self.scale or self._standard_params.var_average:
            image = self.processor.scale(image, self._standard_params.var_average, self._standard_params.var_per_channel)
        image = self.processor.transposed(image)
        return image

    def _get_image(self, i):
        image = Image.open(self.items[i][IMAGE])
        return image


class ImageDataReader(ImageDataReaderBase):
    def __init__(self, txt_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._read_from_txt(txt_path)
        if self.shuffle:
            random.shuffle(self.items)


class CifarArchive:
    CIFAR10 = 'CIFAR10'
    CIFAR100 = 'CIFAR100'

    @classmethod
    def read_from_archive(cls, archive_path, cifar_type,
                          coarse_labels, load_test: bool,
                          store: callable):
        """
        Reads cifar archive

        :param self:
        :param load_test:
        :param coarse_labels:
        :param store:
        :return:
        """
        data_type_t = 'test' if load_test else 'train'
        print("Loading {0} data from {1}".format(data_type_t, archive_path))
        tar = tarfile.open(archive_path, 'r')
        if cifar_type == cls.CIFAR100:
            label_name = 'coarse_labels' if coarse_labels else 'fine_labels'
        else:
            label_name = 'labels'
        data_key_names = cls._get_data_key_names(cifar_type, load_test)
        for member in tar.getmembers():
            if '/' in member.name:
                data_key = member.name.split('/')[1]
                if data_key not in data_key_names:
                    continue
                f = tar.extractfile(member)
                pick = pickle._Unpickler(f)
                pick.encoding = 'latin1'
                data = pick.load()
                store(data, label_name)

    @classmethod
    def _get_data_key_names(cls, cifar_type, load_test):
        if cifar_type == cls.CIFAR10:
            test_names = ['test_batch']
            train_names = ['data_batch_' + str(i) for i in range(1, 6)]
        elif cifar_type == cls.CIFAR100:
            test_names = ['test']
            train_names = ['train']
        else:
            raise NotImplementedError("Unexpected cifar type: {0}".format(self.cifar_type))
        if load_test:
            return test_names
        return train_names


class CifarDataReader(ImageDataReaderBase):

    def __init__(self, archive_path, *args, load_test=False, coarse_labels=False, **kwargs):
        """
        Load cifar archive for test or train data

        :param archive_path: str
            path to cifar tar.gz archive
        :param args: tuple
            ImageDataReaderBase params
        :param test: bool
            load test dataset instead of train
        :param coarse: bool
            load coarse labels instead of fine
        :param kwargs: dict
            ImageDataReaderBase params
        """
        super().__init__(*args, **kwargs)
        self.archive_path = archive_path
        self.load_test = load_test
        self.coarse_labels = coarse_labels
        self._cifar_type = None
        self._images = []
        self._load()

    def _load(self):
        self._set_cifar_type()
        CifarArchive.read_from_archive(self.archive_path, self.cifar_type, self.coarse_labels,
                                       self.load_test, self.__store)
        self._size = len(self.items)
        if self.shuffle:
            random.shuffle(self.items)

    @property
    def cifar_type(self):
        assert self._cifar_type is not None
        return self._cifar_type

    @cifar_type.setter
    def cifar_type(self, value):
        self._cifar_type = value

    def _set_cifar_type(self):
        tar = tarfile.open(self.archive_path, 'r')
        members = tar.getmembers()
        if any('cifar-10-' in x.name for x in members):
            self.cifar_type = CifarArchive.CIFAR10
        elif any('cifar-100-' in x.name for x in members):
            self.cifar_type = CifarArchive.CIFAR100
        else:
            raise NotImplementedError('Only cifar-10 and cifar-100 archives are supported')

    def _reshape_to_image(self, array):
        return self.processor.retransposed(array.reshape((3, 32, 32)))

    def __store(self, data, label_name):
        new_items = [(i + len(self.items), label) for (i, label) in
                     enumerate(data[label_name])]
        self._images.extend(self._reshape_to_image(row) for row in data['data'])
        self.items.extend(new_items)

    def _get_image(self, i):
        return self._images[self.items[i][IMAGE]]
