
import numpy as np
import torch

if __name__ == '__main__':
    entities = np.array([0,1,2,3],dtype=np.int)
    relations = [0,1]
    test_triples = np.array([[0,0,1], [0,1,2], [1,0,1]],dtype=np.int)

    for row_nmbr, row in enumerate(test_triples):
        candidate_entities_subject_based = np.delete(arr=entities, obj=row[0:1])
        candidate_entities_subject_based = np.reshape(candidate_entities_subject_based, newshape=(-1, 1))
        candidate_entities_object_based = np.delete(arr=entities, obj=row[2:3])
        candidate_entities_object_based = np.reshape(candidate_entities_object_based, newshape=(-1, 1))

        print("candidate_entities_subject_based.T : ", candidate_entities_subject_based.T)
        print("candidate_entities_object_based.T: ", candidate_entities_object_based.T)
        print()

        tuple_subject_based = np.reshape(a=test_triples[row_nmbr, 1:3], newshape=(1, 2))
        tuple_object_based = np.reshape(a=test_triples[row_nmbr, 0:2], newshape=(1, 2))

        print("tuple_subject_based: ", tuple_subject_based)
        print("tuple_object_based: ", tuple_object_based)
        print()

        tuples_subject_based = np.repeat(a=tuple_subject_based, repeats=candidate_entities_subject_based.shape[0],
                                         axis=0)
        tuples_object_based = np.repeat(a=tuple_object_based, repeats=candidate_entities_object_based.shape[0], axis=0)

        print("tuples_subject_based: ", tuples_subject_based)
        print("tuples_object_based: ", tuples_object_based)
        print()

        corrupted_subject_based = np.concatenate([candidate_entities_subject_based, tuples_subject_based], axis=1)
        corrupted_subject_based = torch.tensor(corrupted_subject_based, dtype=torch.long)

        corrupted_object_based = np.concatenate([tuples_object_based, candidate_entities_object_based], axis=1)
        corrupted_object_based = torch.tensor(corrupted_object_based, dtype=torch.long)

        print("corrupted_subject_based: ", corrupted_subject_based)
        print("corrupted_object_based: ", corrupted_object_based)
        print()

        pos_triple = np.array(row)
        pos_triple = np.expand_dims(a=pos_triple, axis=0)
        pos_triple = torch.tensor(pos_triple, dtype=torch.long)
        score_of_positive = 3.2

        print("pos_triple: ", pos_triple)

        scores_of_corrupted_subjects = [2.5, 0.5, 10.]
        scores_object_based = [2.5, 0.5, 10.]

        scores_subject_based = np.append(arr=scores_of_corrupted_subjects, values=score_of_positive)
        indice_of_pos_subject_based = scores_subject_based.size - 1

        print("scores_subject_based: ", scores_subject_based)
        print("indice_of_pos_subject_based: ", indice_of_pos_subject_based)
        print()

        _, sorted_score_indices_subject_based = torch.sort(torch.tensor(scores_subject_based, dtype=torch.float),
                                                           descending=False)
        sorted_score_indices_subject_based = sorted_score_indices_subject_based.cpu().numpy()

        print("sorted_score_indices_subject_based: ", sorted_score_indices_subject_based)
        print()

        rank_of_positive_subject_based = np.where(sorted_score_indices_subject_based == indice_of_pos_subject_based)[0][
            0]

        print("rank_of_positive_subject_based: ", rank_of_positive_subject_based)

        exit(0)