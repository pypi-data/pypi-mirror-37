import matplotlib
matplotlib.matplotlib_fname()
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    losses = [1, 0.5, 0.25, 0.3, 1]
    epochs = np.arange(start=1, stop=len(losses) + 1)
    plt.title(r'Loss Per Epoch')
    plt.xlabel('epoch')
    plt.ylabel('loss')

    plt.plot(epochs, losses)
    plt.savefig('/Users/mehdi/PycharmProjects/kg_embeddings_pipeline/data/corpora/out/losses.png')
