
import torch
import numpy as np
if __name__ == '__main__':
    # a = torch.tensor(np.array([1,1,1],dtype=np.float32))
    # b = torch.transpose(torch.tensor(np.ones(shape=(3,4),dtype=np.float32)),0,1)

    # c = a*b

    a = torch.tensor([[3,3,3],[2,2,2]], dtype=torch.float)
    b = torch.tensor([[1,1,1],[1,1,1]], dtype=torch.float)
    c = torch.tensor([[1,1],[2,2]], dtype=torch.long)

    print(a-b)

    s = torch.sum(a-b,1)
    square= torch.mul(s,s)
    rt = torch.sqrt(square)
    dist = -rt
    print(s)
    print(square)
    print(rt)
    print(dist)

    print(torch.abs(s))

    # print(a-b)


    # print(torch.dist(a+b,c))
    # print(torch.norm(a-b,1))
    # a = np.array([1,5,0],dtype=np.int)
    # print(np.sort(a))
    # print(c)

