# -*- coding: utf-8 -*-
import numpy as np

if __name__ == '__main__':
    np.random.seed(1)
    ent = [10,2,20]

    for _ in range(3):
        print(np.random.permutation(ent))
