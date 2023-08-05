import numpy
from skimage import exposure
from fireml import common
from PIL import Image
np = numpy

epsilon = 0.0000001

class Preprocessor:
    def __init__(self, new_size=None, mean_values=None, scale=0.0):
        """
        Substract mean value and/or resize

        :param new_size: (width, height)
        :param mean_values: (r, g, b) or (intensity) for 1 channel image
        """
        self.new_size = new_size
        self._mean = mean_values
        self._scale = scale
        self._ave_mean_per_channel = None
        self._mean_idx = 1
        self._ave_std_per_channel = None
        self._std_idx = 1

    def resize(self, image):
        tmp = image
        if self.new_size is not None:
            w, h = self.new_size
            tmp = np.asarray(common.scale(tmp, w, h))
        return tmp

    @staticmethod
    def std_per_channel(image):
        return numpy.array([image[:, :, i].std() for i in range(image.shape[-1])])

    @staticmethod
    def mean_per_channel(image):
        return numpy.array([image[:, :, i].mean() for i in range(image.shape[-1])])

    def scale(self, image, average: int, per_channel: bool):
        if self._scale:
            return image * self._scale
        if average == 0:
            return image
        if self._ave_std_per_channel is None:
            self._ave_std_per_channel = self.std_per_channel(image)
        # update average
        self._ave_std_per_channel = common.iterative_mean(self._ave_std_per_channel, self.std_per_channel(image), self._std_idx)
        if self._std_idx < average:
            self._std_idx += 1
        if per_channel:
            return image / [max(x, epsilon) for x in self._ave_std_per_channel]
        mean = self._ave_mean_per_channel.mean()
        std_sq = numpy.mean(self._ave_mean_per_channel ** 2 + self._ave_std_per_channel ** 2) - mean ** 2
        return image / max(std_sq ** 0.5, epsilon)

    def substract(self, image, average: int, per_channel: bool):
        if self._mean:
            return image - self._mean
        if average == 0:
            return image
        if self._ave_mean_per_channel is None:
            self._ave_mean_per_channel = self.mean_per_channel(image)
        # update average
        self._ave_mean_per_channel = common.iterative_mean(self._ave_mean_per_channel, self.mean_per_channel(image), self._mean_idx)
        if self._mean_idx < average:
            self._mean_idx += 1
        # actual computation
        if per_channel:
            return image - self._ave_mean_per_channel
        return image - self._ave_mean_per_channel.mean()

    def restore_substraction(self, image):
        if self.mean is not None:
            return image + self.mean
        return image

    def mirror(self, image):
        tmp = image
        if 0.5 < np.random.random():
            # lucky!
            transposed = tmp.shape[0] < tmp.shape[-1]
            tmp = numpy.fliplr(self.retransposed(tmp))
            if transposed:
                tmp = self.transposed(tmp)
        return tmp

    @staticmethod
    def transposed(image):
        transposed = image.shape[0] < image.shape[-1]
        if not transposed:
            return common.transpose(image)
        return image

    @staticmethod
    def retransposed(image):
        transposed = image.shape[0] < image.shape[-1]
        if transposed:
            return common.reverse_transpose(image)
        return image

    def equalize_histogram(self, image):
        img_eq = numpy.zeros_like(image, dtype=numpy.float32)
        n_channels = len(image.shape)
        if n_channels == 3:
            for i in range(image.shape[-1]):
                img_eq[:,:,i] = exposure.equalize_hist(image[:,:,i])
        else:
            img_eq = exposure.equalize_hist(image)
        return (img_eq - 0.5) * 100

    @staticmethod
    def grayscale(self, image):
        return common.rgb2gray(image)

    @staticmethod
    def array_to_pil(array):
        return Image.fromarray(Preprocessor.retransposed(array), 'RGB')

