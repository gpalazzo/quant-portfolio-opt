from amplpy import AMPL, Environment
from time import time
import numpy as np
import pandas as pd


def _generate_random_matrix(nrows: int, ncols: int) -> np.ndarray:

    array = np.random.random((nrows, ncols))

    for i, arr in enumerate(array):
        for j in list(range(len(arr))):
            multiplier = np.random.choice(np.arange(-1, 2), p=[0.34, 0.33, 0.33])
            array[i][j] = arr[j] * multiplier

    return array


start = time()

ampl = AMPL(Environment("/home/ampl/ampl_linux-intel64"))

# reseta contexto antes de cada iteração para limpar memória
ampl.reset()

base_path = "/home/ampl/src"

# read model files
ampl.read(f"{base_path}/young_minmax/young_minmax.mod")
ampl.readData(f"{base_path}/young_minmax/young_minmax.dat")

assets = ampl.getSet("A")
assets_list = assets.getValues().toList()
assets_list = ["I" if isinstance(col, float) else col for col in assets_list]

# numpy matrix
matrix = _generate_random_matrix(nrows=100000, ncols=len(assets_list))
df = pd.DataFrame(matrix, columns=assets_list)

data_values = {}

for j, row in df.iterrows():
    for k in range(0, len(row)):
        _key = (j + 1, row.index[k])
        data_values[_key] = row[k]

return_df_ampl = pd.DataFrame.from_dict(data_values, orient="index", columns=["value"])

ampl.param["RetMat"] = return_df_ampl

ampl.setOption("solver", "cplex")

ampl.solve()


print(f"Demorou {(time() - start) / 60} min para rodar.")
