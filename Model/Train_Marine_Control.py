from  keras.models import Sequential
from keras.layers import Dense

import numpy as np

if __name__ == "__main__":
    epsilon = .1
    num_actions = 3
    epoch = 1000
    max_memory = 1000
    hidden_size = 100
    batch_size = 50
    grid_size = 64

    model = Sequential()
    model.add(Dense(hidden_size, input_shape=(grid_size**2, ), activation='relu'))
    model.add(Dense(hidden_size, activation='relu'))
    model.add(Dense(num_actions))
    model.compile(sgd(lr=.2), "mse")

    env = Catch(grid_size)

    for e in range(epoch):
        loss = 0.
        env