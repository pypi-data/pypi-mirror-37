
import torch

if __name__ == '__main__':
    heads = torch.tensor([1,3,5,1])
    tails = torch.tensor([2,4,4])

    ent = torch.cat([heads,tails],)
    ent_unique = torch.unique(ent)

    print(ent)
    print(ent_unique)