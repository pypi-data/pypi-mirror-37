
import torch
import numpy as np
import torch.nn as nn

if __name__ == '__main__':
    # a = torch.randn(2, 3)
    # b = torch.randn(2, 3, 7)
    # c = torch.randn(2, 7)
    # torch.einsum('ik,ikl->il', [a, b])
    # exit(0)

    pos_heads = torch.tensor([0,1])
    pos_rels = torch.tensor([0, 0])
    pos_tails = torch.tensor([0, 0])

    num_entities = 2
    num_relations = 2
    relation_embedding_dim = 3
    entity_embedding_dim = 2

    entity_embeddings = nn.Embedding(num_entities, entity_embedding_dim)
    relation_embeddings = nn.Embedding(num_relations, relation_embedding_dim)
    projection_matrix_embs = nn.Embedding(num_relations, entity_embedding_dim * relation_embedding_dim)

    print("projection_matrix_embs shape: ", projection_matrix_embs.weight.shape)
    print("projection_matrix_embs: ", projection_matrix_embs.weight.data)
    print()

    proj_matrix_embs = projection_matrix_embs(pos_rels).view(-1,  entity_embedding_dim, relation_embedding_dim)
    print("proj_matrix_embs shape: ", proj_matrix_embs.shape)
    print(proj_matrix_embs)
    print()

    pos_h_embs = entity_embeddings(pos_heads)
    pos_r_embs = relation_embeddings(pos_rels)
    pos_t_embs = entity_embeddings(pos_tails)

    print("pos_h_embs shape: ", pos_h_embs.shape)
    print("pos_h_embs: ", pos_h_embs)
    print()

    # proj_pos_heads_embs = torch.mm(pos_h_embs, projection_matrix_embs.weight)
    proj_pos_heads_embs = torch.einsum('ik,ikl->il',[pos_h_embs,proj_matrix_embs])
    print("proj_pos_heads_embs shape: ", proj_pos_heads_embs.shape)
    print("proj_pos_heads_embs: ", proj_pos_heads_embs)
    print()


