
import numpy as np

if __name__ == '__main__':
    a = np.array([5,2,1], dtype=np.float)

    appended = np.append(arr=a, values=7)

    indice_of_pos = appended.size -1

    sorted = np.argsort(appended)

    rank = np.where(sorted == indice_of_pos)[0][0]

    print(a)
    print(appended)
    print(sorted)
    print(indice_of_pos)
    print(rank)