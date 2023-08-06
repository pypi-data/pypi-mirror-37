
import torch
if __name__ == '__main__':
    PATH = '/Users/mehdi/PycharmProjects/PyKEEN/data/corpora/out/2018-10-28_13:53:34/trained_model.pkl'
    the_model = torch.load(PATH)

    print(the_model)