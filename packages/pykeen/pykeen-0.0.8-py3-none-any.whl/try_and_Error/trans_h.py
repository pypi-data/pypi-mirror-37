
import torch


def project():
    pass

if __name__ == '__main__':
    heads = torch.tensor([[1.,1.],[2.,2.]]).unsqueeze(1)
    normal_vecs = torch.tensor([[1., 1.], [2., 2.]]).unsqueeze(1)

    scaling_factors = torch.sum(normal_vecs*heads, dim=-1).unsqueeze(1)

    print(scaling_factors.shape)
    exit(0)

    heads_projected_on_normal_vecs = scaling_factors * normal_vecs
    projections = (heads - heads_projected_on_normal_vecs).view(-1,2)

    print(projections)
    print()

    energy_vecs = heads.view(-1,2) - projections

    print(energy_vecs)
    print()

    scores = torch.norm(energy_vecs, dim=1, p=2).view(size=(-1,))

    print(scores)
