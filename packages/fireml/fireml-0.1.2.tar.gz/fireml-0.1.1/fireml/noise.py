import theano
import numpy
import theano.tensor as T
from theano.ifelse import ifelse


def iterative_mean(current, new, t):
    mean = current + 1.0/t * (new - current)
    return mean

def OUnoise(curr, tau, eps, dt):
    return curr * numpy.exp(-dt/tau) + (eps / tau * (1 - numpy.exp(-2 * dt / tau))) ** 0.5 * numpy.random.normal()

def Ornstein_Uhlenbeck_noise(tau, eps, gaussian_noise, dt):
    curr = theano.shared(numpy.zeros(gaussian_noise.shape.eval()))
    curr.name = 'Ornstein_Uhlenbeck_noise.curr'
    return curr, [(curr, curr * T.exp(-dt/tau) + (eps / tau * (1.0 - T.exp(-2.0 * dt / tau)))**0.5 * gaussian_noise), ]




def smooth(noise, window_param):
    smooth = theano.shared(noise.get_value())
    i = theano.shared(1.0, 'i')
    i.name = 'smooth.i'
    updates = [(smooth, iterative_mean(smooth, noise, i)), (i, ifelse(T.lt(i, window_param), i + 1, i))]
    return smooth, updates


def noise2(curr, noise_scale, theta, sigma ):
    return theta*( - curr) + sigma*numpy.random.normal() * noise_scale


def noise_t(noise, noise_scale, theta, sigma ):
    curr = theano.shared(noise.eval())
    return curr, [(curr, theta * ( - curr) + sigma * noise * noise_scale)]


if __name__ == '__main__':
    c = 0.0
    t = 1.0
    e = 8.88
    ns = 0
    smooth = 0
    x = []
    y = []
    dt = 1
    time = 0.0
    for i in range(1, 1000):
        #print(smooth)
        new_noise = OUnoise(ns, t, e, dt )
        #new_noise = noise2(ns, 2.1, 0.15, 4.5)
        smooth = iterative_mean(smooth, new_noise, i if i < 16 else 16)
        y.append(smooth)
        x.append(time)
        time += 1
        #print(ns)
        ns = new_noise
    import matplotlib.pyplot as plt
    plt.plot(x, y, 'b')
    plt.show()
