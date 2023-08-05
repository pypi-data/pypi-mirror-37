
import torch

if __name__ == '__main__':
        h_embs = torch.tensor([[1,2],[3,4]])
        r_embs = torch.tensor([[2,1],[0,1]])
        t_embs = torch.tensor([[1, 2], [3, 4]])

        intermediates = torch.mul(h_embs, r_embs)
        scores = torch.einsum('nd,nd->n', [intermediates, t_embs])

        print(scores)
