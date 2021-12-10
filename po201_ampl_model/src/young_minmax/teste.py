import numpy as np

if __name__ == "__main__":

    n = 10  # size
    array = np.random.random((n, n))

    for i, arr in enumerate(array):
        for j in list(range(len(arr))):
            multiplier = np.random.choice(np.arange(-1, 2), p=[0.34, 0.33, 0.33])
            array[i][j] = arr[j] * multiplier

    print(array)
