
from itertools import product
import numpy as np
import torch

a = [1,2,3]
c = list(product(a, a))

# print(np.array(c))

d = torch.tensor([100,20,50])

_, e = torch.sort(d)
e = e.cpu().numpy()

print(e)