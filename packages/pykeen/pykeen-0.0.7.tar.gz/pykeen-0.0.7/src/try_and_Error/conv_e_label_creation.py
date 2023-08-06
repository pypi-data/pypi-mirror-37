
import numpy as np
import torch

if __name__ == '__main__':
    scores = np.array([10, 1, 4, 2])
    sorted_score_indices= np.argsort(scores)
    indice_of_pos = 3
    print(sorted_score_indices)
    rank_of_positive = np.where(sorted_score_indices == indice_of_pos)[0][0]
    print(rank_of_positive)
    print(sorted_score_indices[:2])

    print("####torch based sorting#######")
    sorted_scores, sorted_score_indices = torch.sort(torch.tensor(scores,dtype=torch.float),descending=False)
    print(sorted_score_indices)
    print(sorted_scores)
    exit(0)


    pos_triples = np.array([[0,1,2],[0,3,0],[0,1,5]])
    subj_rels = pos_triples[:,0:2]
    labels = []
    entities = np.arange(0,5)
    entities = np.expand_dims(entities,axis=-1)

    y1 = np.array([[1, 2,2], [1, 3,2], [1, 2,2], [2, 2,2]])
    z = np.array([1, 2,2])
    # print((y1 == z))
    # print((y1 == z).all(axis=1)*1.)

    for subj_rel in subj_rels:
        subj_rel = np.expand_dims(subj_rel,axis=0)
        subj_rel_rep = np.repeat(subj_rel,axis=0,repeats=entities.size)
        candidates = np.concatenate([subj_rel_rep,entities],axis=-1)
        label_for_t= []
        for candi in candidates:
            label = (candi == pos_triples).all(axis=1).any()* 1.
            label_for_t.append(label)

        print(label_for_t)
        labels.append(label_for_t)

    labels = np.array(labels)
    print(labels.shape)
    print(labels)
