# -*- coding: utf-8 -*-
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    ent = [1,20,2,3,30,4]
    train, test = train_test_split(ent,test_size = 0.33, random_state = 42)

    print(train)
    print(test)