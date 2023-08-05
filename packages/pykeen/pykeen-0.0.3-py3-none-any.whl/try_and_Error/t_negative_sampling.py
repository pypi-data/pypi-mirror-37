
import numpy as np
import torch

def split_list_in_batches(input_list, batch_size):
    return [input_list[i:i + batch_size] for i in range(0, len(input_list), batch_size)]

if __name__ == '__main__':
    batch_size = 2
    all_entities = np.array([0, 1, 2, 3], dtype=np.int)
    relations = [0, 1]
    pos_triples = np.array([[0, 0, 1], [0, 1, 2], [1, 0, 1]], dtype=np.int)

    num_pos_triples = pos_triples.shape[0]
    num_entities = all_entities.shape[0]


    for epoch in range(1):
        print("Before shuffling pos_triples: ", pos_triples)
        print()
        np.random.seed(seed=2)
        indices = np.arange(num_pos_triples)
        np.random.shuffle(indices)
        pos_triples = pos_triples[indices]
        print("After shuffling pos_triples: ", pos_triples)
        print()

        pos_batches = split_list_in_batches(input_list=pos_triples, batch_size=batch_size)

        print('pos_batches: ', pos_batches)
        print()

        for i in range(len(pos_batches)):
            pos_batch = pos_batches[i]

            print('pos_batch: ', pos_batch)

            current_batch_size = len(pos_batch)
            print('current_batch_size: ', current_batch_size)
            batch_subjs = pos_batch[:, 0:1]
            batch_relations = pos_batch[:, 1:2]
            batch_objs = pos_batch[:, 2:3]

            print("batch_subjs: ", batch_subjs)
            print('batch_relations: ', batch_relations)
            print('batch_objs: ', batch_objs)

            print()

            num_subj_corrupt = len(pos_batch) // 2
            num_obj_corrupt = len(pos_batch) - num_subj_corrupt
            pos_batch = torch.tensor(pos_batch, dtype=torch.long)

            print('num_subj_corrupt: ', num_subj_corrupt)
            print('num_obj_corrupt: ', num_obj_corrupt)
            print()

            corrupted_subj_indices = np.random.choice(np.arange(0, num_entities), size=num_subj_corrupt)
            print('corrupted_subj_indices: ', corrupted_subj_indices)

            corrupted_subjects = np.reshape(all_entities[corrupted_subj_indices], newshape=(-1, 1))

            print('corrupted_subjects: ', corrupted_subjects)

            subject_based_corrupted_triples = np.concatenate(
                [corrupted_subjects, batch_relations[:num_subj_corrupt], batch_objs[:num_subj_corrupt]], axis=1)

            print('subject_based_corrupted_triples: ', subject_based_corrupted_triples)

            corrupted_obj_indices = np.random.choice(np.arange(0, num_entities), size=num_obj_corrupt)
            print('corrupted_obj_indices: ', corrupted_obj_indices)

            corrupted_objects = np.reshape(all_entities[corrupted_obj_indices], newshape=(-1, 1))
            print('corrupted_objects: ', corrupted_objects)

            object_based_corrupted_triples = np.concatenate(
                [batch_subjs[num_subj_corrupt:], batch_relations[num_subj_corrupt:], corrupted_objects], axis=1)

            print('object_based_corrupted_triples: ', object_based_corrupted_triples)

            neg_batch = np.concatenate([subject_based_corrupted_triples, object_based_corrupted_triples], axis=0)

            neg_batch = torch.tensor(neg_batch, dtype=torch.long)

            print('neg_batch: ', neg_batch)

            print()

        print('###########')