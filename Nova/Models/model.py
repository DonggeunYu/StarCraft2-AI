import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
import csv
import sys


file = open('./SUPPLYDEPOT.csv', 'r', encoding='utf-8')
csv_reader = csv.reader(file)

for row in csv_reader:
    print(row[0].split('"', "("))
file.close()
'''
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
model.add(Dense(2))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit_generator(
        train_generator,
        steps_per_epoch=15,
        epochs=50,
        validation_data=test_generator,
        validation_steps=5)

model.fit()
'''