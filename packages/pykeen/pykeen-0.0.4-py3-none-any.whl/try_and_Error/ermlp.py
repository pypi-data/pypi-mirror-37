
import torch
import torch.autograd
import torch.nn as nn

if __name__ == '__main__':
    mlp = nn.Linear(3,5)
    embedding_dim = 3

    a = torch.tensor([[1,2,3],[2,4,6]],dtype=torch.float)

    print(mlp(a).shape)

    b = torch.cat([a,a],dim=1)

    print(b)

    mlp = nn.Sequential(
        nn.Linear(2 * embedding_dim, embedding_dim),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(embedding_dim, 1),
    )

    print()
    print(mlp(b).shape)
    print(mlp(b))