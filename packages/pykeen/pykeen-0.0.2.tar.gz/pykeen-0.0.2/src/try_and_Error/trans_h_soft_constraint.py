
import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim

if __name__ == '__main__':
    entities_embs = torch.nn.Embedding(3, 2)
    normal_vector_embs = torch.nn.Embedding(3, 2)
    projected_relation_embs = torch.nn.Embedding(3, 2)
    num_entities = 3
    num_relations = 3
    epislon = 1
    c = 0.5
    criterion = nn.MarginRankingLoss(margin=1, size_average=False)

    norm_of_entities = torch.norm(entities_embs.weight, p=2, dim=1)

    print("norm_of_entities shape: ", norm_of_entities.shape)
    print("norm_of_entities: ", norm_of_entities)
    print()


    square_norms_entities = torch.mul(norm_of_entities, norm_of_entities)

    print("square_norms_entities.shape: ", square_norms_entities.shape)
    print("square_norms_entities: ", square_norms_entities)
    print()


    entity_constraint = square_norms_entities - num_entities * 1.
    print("entity_constraint shape: ", entity_constraint.shape)
    print("entity_constraint: ", entity_constraint)
    print()

    entity_constraint = torch.sum(entity_constraint,dim=0)

    print("sum entity_constraint shape: ", entity_constraint.shape)
    print("sum entity_constraint: ", entity_constraint)
    print()

    print("normal_vector_embs shape: ", normal_vector_embs.weight.shape)
    print("normal_vector_embs: ", normal_vector_embs.weight.data)
    print()

    print("projected_relation_embs.weight shape: ", projected_relation_embs.weight.data.shape)
    print("projected_relation_embs.weight: ", projected_relation_embs.weight.data)
    print()

    orthogonalty_constraint_numerator = torch.mul(normal_vector_embs.weight,projected_relation_embs.weight)

    orthogonalty_constraint_numerator = torch.sum(orthogonalty_constraint_numerator,dim=1)


    orthogonalty_constraint_numerator = torch.mul(orthogonalty_constraint_numerator,
                                                  orthogonalty_constraint_numerator)

    print("shape orthogonalty_constraint_numerator: ", orthogonalty_constraint_numerator.shape)
    print("orthogonalty_constraint_numerator: ", orthogonalty_constraint_numerator)
    print()

    orthogonalty_constraint_denominator = torch.norm(projected_relation_embs.weight, p=2, dim=1)


    orthogonalty_constraint_denominator = torch.mul(orthogonalty_constraint_denominator,
                                                    orthogonalty_constraint_denominator)
    print("orthogonalty_constraint_denominator shape: ", orthogonalty_constraint_denominator.shape)
    print("orthogonalty_constraint_denominator: ", orthogonalty_constraint_denominator)
    print()


    relation_constraint = orthogonalty_constraint_numerator / orthogonalty_constraint_denominator
    print("relation_constraint shape: ", relation_constraint.shape)
    print("relation_constraint :", relation_constraint)
    print()

    relation_constraint = torch.sum(relation_constraint)

    relation_constraint = relation_constraint - num_relations * epislon
    soft_constraints = c * (entity_constraint + relation_constraint)

    print( soft_constraints)

    # loss = margin_ranking_loss + soft_constraints