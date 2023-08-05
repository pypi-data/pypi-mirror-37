
import numpy as np

def my_func(r):
    return  hash(tuple(r))
if __name__ == '__main__':
    training_triples = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    test_triples = np.array([[3,3,3], [5, 5, 5], [5, 5, 4]])


    t = np.isin(element=test_triples,test_elements=training_triples) * 1.
    t = np.sum(t,axis=1)/3
    r = np.where(t==1.)
    print(test_triples[r])
    print(t)
    print(r)
    exit(0)
    all_triples = np.concatenate([training_triples,test_triples],axis=0)
    all_triples_hashed = np.apply_along_axis(my_func, 1, all_triples)
    corrupted = np.array([[1,1,1], [1,1,1]])
    corrupted_hashed = np.apply_along_axis(my_func,1,corrupted)

    mask = np.in1d(corrupted_hashed, all_triples_hashed, invert=True)
    mask2 = np.where(mask)[0]

    print(mask2.size)

    if not mask2:
        print("no")

    print(corrupted_hashed[mask])
    print(corrupted_hashed)
    print(corrupted[mask2])
