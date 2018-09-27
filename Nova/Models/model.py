from keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation

model = Sequential
model.add(Dense(16, input_dim=6, init='uniform'))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(8))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(4))
model.add(Activation('relu'))
model.add(Dropout(0.2))
