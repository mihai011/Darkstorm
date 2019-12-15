from socket import *
import time
startTime = time.time()

from multiprocessing import Process
from multiprocessing import Pool                                                
from functools import partial




def scan_target(port, target):

    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(5)
    try:
        conn = s.connect((target, port))
    except timeout:
        return 

    return port



if __name__ == "__main__":
    
    ports = 1000
    target = "8.8.8.8"

    ports = [i for i in range(1, ports)]

    scan_partial = partial(scan_target, target=target)
    pool = Pool(processes=len(ports))
    res = pool.map(scan_partial, ports)
    res  = list(filter(lambda x: x!=None, res))
    print(res)
