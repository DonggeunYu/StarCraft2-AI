import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
import csv


file = open('./SUPPLYDEPOT.csv', 'r', encoding='utf-8')
csv_reader = csv.reader(file)

commandcenter = []
mineral_1 = []
mineral_2 = []
mineral_3 = []
vespen_1 = []
vespen_2 = []

for row in csv_reader:
    for i in range(len(row)):
        if i == 0:
            commandcenter.append([float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')])
        elif i == 1:
            mineral_1.append([float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')])
        elif i == 2:
            mineral_2.append([float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')])
        elif i == 3:
            mineral_3.append([float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')])
        elif i == 4:
            vespen_1.append([float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')])
        elif i == 5:
            vespen_2.append([float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')])

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