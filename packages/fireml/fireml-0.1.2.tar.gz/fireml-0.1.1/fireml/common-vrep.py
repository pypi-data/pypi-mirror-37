import numpy
import scipy
import pylab
import theano
import os
import theano.tensor as T 
from scipy import interpolate
from const import DELTA_FLOAT


def png_to_data_by_names():
    '''convert image files to dataset
    
    if name starts with 'train' image goes to train set
    if name starts with 'valid' image goes to validation set
    if name starts with 'test' image goes to test set
    '''
    dataset_path = "/home/noskill/projects/python/DeepLearningTutorials/nn_application/dataset"  
    image_path = "/home/noskill/projects/python/DeepLearningTutorials/nn_application/m"

    dirs = os.listdir(image_path)
    targets = range(len(dirs))
    dataset = [None, None, None]
    for d in targets:
        frameList = [[],[],[]]
        dir = os.path.join(image_path, dirs[d])
        for f in os.listdir(dir):
            file = os.path.join(dir, f)
            r = numpy.random.randint(0,10, 1)
            if 'train' in f:
                frameList[0].append(pylab.imread(file)) # train
            else:
                if r <= 5:
                    frameList[1].append(pylab.imread(file)) # validation
                else:
                    frameList[2].append(pylab.imread(file)) # test
                

        if dataset[0]==None:     
            for i in range (0,3):
                dataset[i]= gendatasetfromlist(frameList[i], d, dtype=numpy.float16)
        else:
            for i in range (0,3):
                dataset[i]=numpy.concatenate([dataset[i],gendatasetfromlist(frameList[i], d, dtype=numpy.float16)])       

        save_dataset(dataset, dataset_path, 'exp')


def png_to_data():
    '''converts images to dataset
    
    takes images from folders and converts it to dataset
    one folder = one dataset
    '''
    
    dataset_path = "/home/noskill/projects/python/DeepLearningTutorials/nn_application/dataset"  
    image_path = "/home/noskill/projects/python/DeepLearningTutorials/nn_application/m"

    dirs = os.listdir(image_path)
    targets = range(len(dirs))
    dataset = [None, None, None]
    for d in targets:
        frameList = [[],[],[]]
        dir = os.path.join(image_path, dirs[d])
        for f in os.listdir(dir):
            file = os.path.join(dir, f)
            rand = numpy.random.randint(0,10, 1)
            if rand <= 2:
                frameList[1].append(pylab.imread(file)) # validation
            elif rand >= 9:
                frameList[2].append(pylab.imread(file)) # test
            else:
                frameList[0].append(pylab.imread(file)) # train

        if dataset[0]==None:     
            for i in range (0,3):
                dataset[i]= gendatasetfromlist(frameList[i], d, dtype=numpy.float16)
        else:
            for i in range (0,3):
                dataset[i]=numpy.concatenate([dataset[i],gendatasetfromlist(frameList[i], d, dtype=numpy.float16)])       
        save_dataset(dataset, dataset_path, 'onekey')


def gendatasetfromlist(frameList, target, dtype=numpy.float32):
    '''generates dataset from images in given list with given target

    brightness of pixels converted to [0; 1] range
    '''

    h,v = frameList[0].shape[0],frameList[0].shape[1]
    data_set = numpy.zeros([len(frameList), h*v*3 + 1], dtype)
    for y in range(len(frameList)):
        frame = frameList[y]
        if frame.max() > 1.0 + DELTA_FLOAT:
            data_set[y,:-1] = (frame / 255.).reshape(frame.size)
        else:
            data_set[y,:-1] = frame.reshape(frame.size)
        import pdb;pdb.set_trace()
        data_set[y,-1] = target
    return data_set


def resize_linearized(array, init_shape, target_shape):
    """
    resize array of 1d Data rows
    """
    result = numpy.zeros([array.shape[0], numpy.prod(target_shape)], dtype=array.dtype)
    for i in range(array.shape[0]):
        result[i] = scipy.misc.imresize(array[i].reshape(init_shape), target_shape, interp='bilinear').reshape(numpy.prod(target_shape))
    return result


def save_dataset(dataset, path, name):
    def save(full_path, data):
        if os.path.exists(full_path):
            f = open(full_path, "ab")
        else:
            f = open(full_path, "wb")
        f.write(data)
        f.close()

    names = map(lambda n: os.path.join(path, name + n), ['train_set', 'validation', 'test_set'])
    
    for p, d in zip(names, dataset):
        numpy.save(p, d)


def trajectory_iterator(data, n_items=20, datafields=4, dtype=theano.config.floatX):
    current = 0
    assert(all(map(lambda x: x < 10e-10, data[current][1:])))
    next_chunk = int(data[current][0]) + datafields
    item_size = int(data[1][0]) - 1
    current += datafields
    target_size = int(data[2][0])
    target = data[3][:target_size]

    while True:
        if current >= data.shape[0]:
            raise StopIteration
        chunk = data[current:next_chunk][:, 1:item_size + 1]
        trajectory = interp3d(chunk, numpy.linspace(0,10, chunk.shape[0]), numpy.linspace(0,10, n_items))

        yield trajectory.astype(dtype)

        current = next_chunk + 2
        if current >= data.shape[0]:
            raise StopIteration
        target = data[next_chunk + 1][:-1]
        next_chunk += int(data[next_chunk][0]) + 2


def joint_interp_iterator(data, datafields=4, n_items=20, dtype=theano.config.floatX, return_target=False):
    current = 0
    assert(all(map(lambda x: x < 10e-10, data[current][1:])))
    next_chunk = int(data[current][0]) + datafields
    item_size = int(data[1][0]) - 1
    current += datafields
    target_size = int(data[2][0])
    target = data[3]

    while True:
        if current >= data.shape[0]:
            raise StopIteration
        chunk = data[current:next_chunk][:, 1:item_size + 1]
        joints = interpnd(chunk, numpy.linspace(0,10, chunk.shape[0]), numpy.linspace(0,10, n_items))
	if return_target:
	  yield joints.astype(dtype), target
        else:
	  yield joints.astype(dtype)

        current = next_chunk + 2
        if current >= data.shape[0]:
            raise StopIteration
        target = data[next_chunk + 1][:-1]

        next_chunk += int(data[next_chunk][0]) + 2


def joint_iterator(data, n_items=5, datafields=4):
    current = 0
    assert(all(map(lambda x: x < 10e-10, data[current][1:])))
    next_chunk = int(data[current][0]) + datafields
    item_size = int(data[1][0]) - 1
    current += datafields
    target_size = int(data[2][0])
    target = data[3]

    while True:
        if current >= data.shape[0]:
            raise StopIteration
        if current >= next_chunk:
            current = next_chunk + 2
            target = data[next_chunk + 1]
            next_chunk += int(data[next_chunk][0]) + 2
        result = numpy.zeros([n_items, item_size], dtype=data.dtype)
        for i in range(n_items):
            if current + i < next_chunk:
                result[i] = data[current + i][1: item_size + 1]
            else:
                result[i] = data[next_chunk - 1][1: item_size + 1]
        result = numpy.vstack((target[:item_size], result))
        yield result

        current += 1

def target_iterator(joint_chunk, datafields=4):
    """
    iterates over target (x, y, z) vectors in joint data dump
    """
    
    current = 0
    assert(all(map(lambda x: x < 10e-10, joint_chunk[current][1:])))
    next_chunk = int(joint_chunk[current][0]) + datafields
    current += datafields
    target_size = int(joint_chunk[2][0])
    target = joint_chunk[3][:target_size]

    while True:
        if current >= joint_chunk.shape[0]:
            raise StopIteration
        yield target
        current = next_chunk + 2
	target = joint_chunk[next_chunk + 1][:target_size]
	next_chunk += int(joint_chunk[next_chunk][0]) + 2

      

def tip_joint_iterator(tip_chunk, joint_chunk, n_items=None):
    """
    returns x,y pair.
    x = [current_joint_position, desired_tip_position]
        numpy.array of len 5 + 3 = 8
    y = desired_j_position
      numpy.array of len  5
    """
    
    if not n_items:
        for i in range(tip_chunk.shape[0]):
                if i == 0:
                    result_x = numpy.hstack([joint_chunk[i], tip_chunk[i + 1]])
                    result_y = joint_chunk[i + 1]
                elif i == tip_chunk.shape[0] - 1:
                    yield result_x, result_y
                else:
                    raw = numpy.hstack([joint_chunk[i], tip_chunk[i + 1]])
                    result_x = numpy.vstack([result_x, raw])
                    result_y = numpy.vstack([result_y, joint_chunk[i + 1]])
        raise StopIteration       
    else:
        for i in range(tip_chunk.shape[0]):
            if i != tip_chunk.shape[0] - 1:
                result_x = numpy.hstack([joint_chunk[i], tip_chunk[i + 1]])
                result_y = joint_chunk[i + 1]
                yield result_x, result_y
            else:
                raise StopIteration


def dist(x,y):   
    return numpy.sqrt(numpy.sum((x-y)**2))


def get_nearest_next(points, point, threshold=None):
    _dist = [dist(p, point) for p in points]
    n_points = len(_dist)
    for i in range(n_points):
        if _dist[i] >= threshold:
            if (i != n_points - 1) and i:
                assert_point_on_line(points[i], points[i-1], points[i+1], threshold/20.0)
            return points[i]
    return points[-1]


def assert_point_on_line(point, a, b, threshold=None):
    x, y, z = [(point[i] - a[i])/(b[i] - a[i]) for i in range(3)]
    assert(numpy.abs(z - x) + numpy.abs(y - x) < threshold)
    return True
    

def interpnd(array, x, points, kind='cubic'):
    inter = [interpolate.interp1d(x, array[:,i], kind=kind) for i in range(array.shape[1])]
    return reduce(lambda one, two: numpy.vstack([one(points) if callable(one) else one, two(points)]), inter).transpose()


def interp3d(array, x, points, kind='cubic'):
    """array - array of shape (n_points, 3)
       x - range of datapoints indexes 
       points - array of points to interpolate at"""
    s_x, s_y, s_z = [interpolate.interp1d(x, array[:,i], kind=kind) for i in range(3)]
    result = numpy.vstack([s_x(points), s_y(points)])
    result = numpy.vstack([result, s_z(points)])
    return result.transpose()


def gen_dataset_from_tip_dump(dtype=numpy.float32):
    """
    generates file with following structure:
    series_size
    target
    data_point
    data_point
    .
    ..
    ..
    series_size
    target
    and so on
    """

    data_file = "/home/noskill/tipdump.txt"
    dataset_path = "/home/noskill/projects/python/DeepLearningTutorials/nn_application/dataset"  
    target_size = 3
    import pdb; pdb.set_trace()
    dataset = [None, None, None]
    lines = []
    max_series_size = 0
    with open(data_file, 'rt') as dump:
        count = 0
        for line in dump.readlines():
            line = line.replace('\n', '')
            if line:
                line = line.replace(' ', ''). replace(',','.').split(';')
                lines.append(line)

            else:
                if lines:
                    series = lines[0]
                    
                    item_size = 3 + 1  #  +1 for timestamp
                    series_size = len(series)/item_size # 
                    if series_size > max_series_size:
                        max_series_size = series_size
                    target = lines[1]
                    assert(len(target) == 3)
                    
                    dataline = numpy.asarray(series, dtype=dtype)
                    dataline = dataline.reshape((series_size, item_size))
                    if count < 2900:
		        number = 0
		    else:
		        number = 2
                    if dataset[number] == None:
                        for data in map(lambda x:numpy.asarray(x, dtype=dtype), reversed((series_size, item_size, target_size, target))):
                            placeholder = numpy.zeros(item_size, dtype=dtype)
                            placeholder[0:data.size] = data
                            dataline = numpy.vstack([placeholder, dataline])
                        dataset[number] = dataline
                    else:
                        for data in map(lambda x:numpy.asarray(x, dtype=dtype), reversed((series_size, target))):
                            placeholder = numpy.zeros(item_size, dtype=dtype)
                            placeholder[0:data.size] = data
                            dataline = numpy.vstack([placeholder, dataline])
                        dataset[number] = numpy.vstack((dataset[number], dataline))
                    lines = []
                else:
                    lines = []
            count += 1
    print max_series_size
    import pdb;pdb.set_trace()
    save_dataset(dataset, dataset_path, 'tip')


def gen_dataset_from_joint_dump(dtype=numpy.float16):
    """
    generates file with following structure:
    target_pos
    joints
    ..
    ...
    joints
    target_pos
    joint
    and so on
    """

    data_file = "/home/noskill/jointdump.txt"
    dataset_path = "/home/noskill/projects/python/DeepLearningTutorials/nn_application/dataset"  

    dataset = [None, None, None]
    lines = []
    with open(data_file, 'rt') as dump:
        count = 0
        for line in dump.readlines():
            line = line.replace('\n', '')
            if line:
                line = line.replace(' ', ''). replace(',','.').split(';')
                lines.append(line)
            else:
                if lines:
                    series = lines[0]
                    item_size = int(series[0]) + 1  #  +1 for timestamp
                    series_size = (len(series) - 1)/item_size # -1 for items_size
                    dataline = numpy.asarray(series[1:], dtype=dtype)  
                    dataline = dataline.reshape((series_size, item_size))
                    target_size = len(lines[1][3:])

                    assert(target_size == 3)
                    assert(target_size <= dataline.shape[1])

                    target = lines[1][3:]

                    if count < 2900:
		        number = 0
		    else:
		        number = 2

                    if dataset[number] == None:
                        for data in map(lambda x:numpy.asarray(x, dtype=dtype), reversed((series_size, item_size, target_size, target))):
                            placeholder = numpy.zeros(item_size, dtype=dtype)
                            placeholder[0:data.size] = data
                            dataline = numpy.vstack([placeholder, dataline])
                        dataset[number] = dataline
                    else:
                        for data in map(lambda x:numpy.asarray(x, dtype=dtype), reversed((series_size, target))):
                            placeholder = numpy.zeros(item_size, dtype=dtype)
                            placeholder[0:data.size] = data
                            dataline = numpy.vstack([placeholder, dataline])
                        dataset[number] = numpy.vstack((dataset[number], dataline))
                    lines = []
                else:
                    lines = []
            count += 1
    import pdb;pdb.set_trace()
    save_dataset(dataset, dataset_path, 'joint')


def load_files(path,name):
    dataset = []
    for postfix in ('train_set.npy' , 'test_set.npy'): #'validation.npy'
        f = os.path.join(path, name + postfix)
        if os.path.exists(f):
	    try:
	      dataset.append(numpy.load(f, 'r'))
	    except ValueError as e:
	      print f + "  error loading: "
	      print e
	      dataset.append(None)
    return dataset


def load_dataset(path, name=''):
    tmp = load_files(path, name)
    dataset = [] 
    for i in range(len(tmp)):
        item = []
        data = tmp[i][:,:-1]
        targets = tmp[i][:,-1]
        item.append(data)
        item.append(targets)
        dataset.append(item)
    return dataset


def get_xy_trajectory(data, target_size=3, dtype=theano.config.floatX, do_reshape=False):
    sample_x = data[0][:target_size]
    sample_x = numpy.hstack([sample_x, data[-1][:target_size]]).astype(dtype)
    sample_y = data.astype(dtype)
    if do_reshape:
        sample_x = sample_x.reshape([1, sample_x.size])
        sample_y = sample_y.reshape([1, sample_y.size])
    return sample_x, sample_y


def get_xy(data, target_size=3, dtype=theano.config.floatX, do_reshape=False):
    # all data except last one
    sample_x = data[:-1].astype(dtype)

    #target position
    target  = sample_x[0][:target_size]

    sample_x = numpy.hstack((target, sample_x[1:].reshape(sample_x[1:].size)))
    sample_y = data[-1].astype(dtype)
    if do_reshape:
        sample_x = sample_x.reshape([1, sample_x.size])
        sample_y = sample_y.reshape([1, sample_y.size])
    return sample_x, sample_y


def get_batch(iter, count=1):
    d1 = next(iter)
    x1,y1 = get_xy(d1)
    count -= 1
    for i in range(count):
        x, y = get_xy(next(iter))
        x1 = numpy.vstack([x1, x])
        y1 = numpy.vstack([y1, y])
    if count == 0:
        x1 = x1.reshape([1, x1.size])
        y1 = y1.reshape([1, y1.size])
    return x1, y1


if __name__ == '__main__':
    gen_dataset_from_tip_dump()
    gen_dataset_from_joint_dump()
    
    #test
    datasets = load_files("/home/leron/projects/python/DeepLearningTutorials/code/dataset", "tip")
    train_set = datasets[0]
    datasets_joint = load_files("/home/leron/projects/python/DeepLearningTutorials/code/dataset", "joint")
    train_set_joint = datasets_joint[0]

    iter = trajectory_iterator(train_set)
    iter_joint = joint_interp_iterator(train_set_joint, return_target=True)

    count=0
    while(True):
      traj = next(iter)
      joints, joints_target = next(iter_joint)
      diff = numpy.sum(numpy.abs(numpy.abs(traj[-1]) - numpy.abs(joints_target[:3])))
      if diff > 0.0003:
	assert(diff < 0.0003)
      count += 1
    
