
import torch
import torch.nn as nn

if __name__ == '__main__':
    emb = torch.nn.Embedding(4, 2)
    print(emb.weight.data)
    norms = torch.norm(emb.weight, p=2, dim=1).data
    emb.weight.data = emb.weight.data.div(norms.view(4, 1).expand_as(emb.weight))

    print()
    print(emb.weight.data)

    print()

    nn.init.uniform_(emb.weight.data, a=-5, b=-3)

    print(emb.weight.data)