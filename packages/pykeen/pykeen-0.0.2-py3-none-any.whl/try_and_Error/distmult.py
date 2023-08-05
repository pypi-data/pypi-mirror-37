import torch
import numpy as np
import torch.nn as nn

if __name__ == '__main__':
    pos_heads = torch.tensor([0, 1])
    pos_rels = torch.tensor([0, 0])
    pos_tails = torch.tensor([0, 0])

    num_entities = 2
    num_relations = 2
    relation_embedding_dim = 3
    entity_embedding_dim = 2

    entity_embeddings = nn.Embedding(num_entities, entity_embedding_dim)
    relation_embeddings = nn.Embedding(num_relations, relation_embedding_dim)

    heads = np.array([[1.,1.,1.],[2.,2.,2.]])
    relations = np.array([[2., 2., 2.], [2., 2., 2.]])
    tails = np.array([[3., 3., 3.], [2., 2., 2.]])

    heads = torch.tensor(heads,dtype=torch.float)
    relations = torch.tensor(relations,dtype=torch.float)
    tails = torch.tensor(tails,dtype=torch.float)

    scores = torch.mul(heads,relations)

    s = torch.sum(heads * relations * tails,dim=1)

    intermediates = torch.mul(heads, relations)
    s2 = torch.einsum('nd,nd->n', [intermediates, tails])

    print(scores)
    print()
    print(s)
    print()
    print(s2)