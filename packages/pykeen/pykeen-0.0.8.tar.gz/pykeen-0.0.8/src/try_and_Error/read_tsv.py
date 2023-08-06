import numpy as np
if __name__ == '__main__':
    path = '/Users/mehdi/PycharmProjects/kg_embeddings_pipeline/corpora/fb15k/fb_15k_test.tsv'

    with open(path) as f:
        lines = f.readlines()

        for l in lines:
            p = l.split('\t')
            if len(p) >3:
                print(p)

        pos_triples = np.loadtxt(fname=path, dtype=str, comments='@Comment@ Subject Predicate Object')#, delimiter='\t')

        print(pos_triples)