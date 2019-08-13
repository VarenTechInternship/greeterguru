# multiprocess server and faceID

import multiprocessing
import time
import os

def faceRecog():
    os.system("cd $GGPATH/FaceID && python3 -c 'from faceID import *; main()'")

def server():
    os.system("cd $GGPATH/GGProject && python3 $GGPATH/GGProject/manage.py runserver")

if __name__ == '__main__':

    proc1 = multiprocessing.Process(target=server)
    proc2 = multiprocessing.Process(target=faceRecog)

    proc1.start()
    time.sleep(5)
    proc2.start()

