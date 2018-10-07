import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
import csv
import numpy as np
import matplotlib.pyplot as plt


file = open('./SUPPLYDEPOT.csv', 'r', encoding='utf-8')
csv_reader = csv.reader(file)

x_train = np.zeros((495, 14))
y_train = np.zeros((495, 2))

cnt = -1
for row in csv_reader:
    cnt += 1
    for i in range(len(row)):
        if i == 0:
            for j in range(2):
                x_train[cnt][i * 2 + j] = [float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')][j]
        elif i == 1:
            for j in range(2):
                x_train[cnt][i * 2 + j] = [float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')][j]
        elif i == 2:
            for j in range(2):
                x_train[cnt][i * 2 + j] = [float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')][j]
        elif i == 3:
            for j in range(2):
                x_train[cnt][i * 2 + j] = [float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')][j]
        elif i == 4:
            for j in range(2):
                x_train[cnt][i * 2 + j] = [float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')][j]
        elif i == 5:
            for j in range(2):
                x_train[cnt][i * 2 + j] = [float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')][j]
        elif i == 6:
            for j in range(2):
                y_train[cnt][j] = [float(i) for i in row[i].split('"')[0].replace('(', '').replace(')', '').split(', ')][j]

print("x_train shape: ", x_train.shape)
print("y_train shape: ", y_train.shape)
file.close()


model = Sequential()
model.add(Dense(64, input_dim=14, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(8, activation='relu'))
model.add((Dense(2, activation='softmax')))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
model.save('build_supply_location_model.h5')
hist = model.fit(x_train, y_train, epochs=200, batch_size=32)


fig, loss_ax = plt.subplots()

acc_ax = loss_ax.twinx()

loss_ax.set_ylim([0.0, 3.0])
acc_ax.set_ylim([0.0, 1.0])

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
acc_ax.plot(hist.history['acc'], 'b', label='train acc')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuracy')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()