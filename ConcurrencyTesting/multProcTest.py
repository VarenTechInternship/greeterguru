import multiprocessing
manager = multiprocessing.Manger()
import time

count = 0

def func1():

    global count

    for i in range(10):
        print("AAAA--> "+str(count))
        count += 1
        time.sleep(.5)

def func2():

    global count

    while count < 10:
        print("BBBB--> "+str(count))
        count += 1
        time.sleep(2)


if __name__ == '__main__':

    proc1 = multiprocessing.Process(target=func1)
    proc2 = multiprocessing.Process(target=func2)

    proc1.start()
    proc2.start()
