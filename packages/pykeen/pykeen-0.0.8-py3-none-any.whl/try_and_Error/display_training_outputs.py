
import pickle

if __name__ == '__main__':

    data_path = '/Users/mehdi/PycharmProjects/kg_embeddings_pipeline/data/corpora/out/25-09-2018_09:29:12/entities_to_embeddings.pkl'
    with open(data_path, 'rb') as f:
        data = pickle.load(f)


    print(data)