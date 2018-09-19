import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)
arrary = np.load('Nova/Examples/train_data/1537020881.npy')

for i in range(len(arrary)):
    print(arrary[i][0])
    plt.imshow(arrary[i][1])
    plt.show()