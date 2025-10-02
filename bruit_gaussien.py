from random import random
import numpy as np
from math import sqrt
from math import cos
from math import sin
from math import log
from math import pi

def double_gauss():
    """
    Cette fonction retourne le bruit gaussien de variance 1
    """
    x0 :float
    x1: float
    nb_ready=0
    u: float
    v: float
    w: float
    z: float

    if nb_ready == 0 :
        u = np.random.uniform(0,1.1)
        v = np.random.uniform(0,1.1)
        while log(u)>0:
            u = np.random.uniform(0,1.1)
        w = sqrt(-2.0 * log(u))
        z = 2 * pi * v
        x0 = w * cos(z)
        x1 = w * sin(z)
       

        nb_ready = 1
        return x0
    
    else :
        nb_ready = 0
        return x1


if __name__ == "__main__":
    print(double_gauss())

    
