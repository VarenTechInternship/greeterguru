from multiprocessing import Pool, Value
from time import sleep

counter = None

def init(args):
    ''' store the counter for later use '''
    global counter
    counter = args

def analyze_data(args):
    ''' increment the global counter, do something with the input '''
    global counter
    # += operation is not atomic, so we need to get a lock:
    with counter.get_lock():
        counter.value += 1
        sleep(1)
    print counter.value
    return args * 10

if __name__ == '__main__':
    #inputs = os.listdir(some_directory)

    #
    # initialize a cross-process counter and the input lists
    #
    counter = Value('i', 0)
    inputs = [1, 2, 3, 4]

    #
    # create the pool of workers, ensuring each one receives the counter 
    # as it starts. 
    #
    p = Pool(initializer = init, initargs = (counter, ))
    i = p.map_async(analyze_data, inputs, chunksize = 1)
    i.wait()
    print i.get()
