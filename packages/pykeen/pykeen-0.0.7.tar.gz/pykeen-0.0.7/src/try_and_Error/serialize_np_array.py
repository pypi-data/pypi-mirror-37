
import numpy as np


if __name__ == '__main__':
    a = np.ones(shape=(2,2))
    outfile = '/Users/mehdi/PycharmProjects/kg_embeddings_pipeline/data/test_serialized_data/matrix.npy'
    np.save(outfile, a)

    print(np.load(outfile))