
import torch
import numpy as np

if __name__ == '__main__':
    training_triples = torch.tensor(([[1, 1, 1], [2, 2, 2], [3, 3, 3]]))
    test_triples = torch.tensor(([[3, 3, 3], [5, 5, 5],[1,1,1]]))

    t = torch.eq(test_triples,training_triples)

    print(t)

