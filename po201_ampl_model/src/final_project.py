from amplpy import AMPL, Environment
import pandas as pd
import numpy as np
from time import time
from functools import reduce
from datetime import datetime, timedelta
from typing import List
from utils import (
    ampl_list_to_pandas_df,
    pandas_df_to_indexed_ampl_format,
    dump_data_pgsql,
    read_data_pgsql,
)


def _generate_random_matrix(nrows: int, ncols: int) -> np.ndarray:

    array = np.random.random((nrows, ncols))

    for i, arr in enumerate(array):
        for j in list(range(len(arr))):
            multiplier = np.random.choice(np.arange(-1, 2), p=[0.45, 0.10, 0.45])
            array[i][j] = arr[j] * multiplier

    return array


def _build_report_dfs_list(total_run_time, solve_time) -> List[pd.DataFrame]:

    _now = datetime.now() - timedelta(hours=3)
    _time_df = pd.DataFrame({"run_timestamp": _now}, index=[0])

    _solve_time_df = pd.DataFrame({"solve_time_min": solve_time}, index=[0])
    _total_runtime_df = pd.DataFrame({"total_run_time_min": total_run_time}, index=[0])

    mean = ampl.getVariable("media_portfolio").getValues().toList()[0]
    mean_df = pd.DataFrame({"mean": mean}, index=[0])

    weights = ampl.getVariable("pesos").getValues().toList()
    weights_df = ampl_list_to_pandas_df(ampl_list=weights, n_stocks=len(weights))

    risk = ampl.getObjective("risco_portfolio").value()
    risk_df = pd.DataFrame({"risk": risk}, index=[0])

    return [_time_df, _total_runtime_df, _solve_time_df, mean_df, risk_df, weights_df]


start_total_runtime = time()

ampl = AMPL(Environment("/home/ampl/ampl_linux-intel64"))

# reseta contexto antes de cada iteração para limpar memória
ampl.reset()

base_path = "/home/ampl/src"

print("Reading mod and dat files...")
ampl.read(f"{base_path}/markowitz.mod")

print("Reading data from Kedro features...")
df_fte = read_data_pgsql(database="mi", tbl_name="master_table")

print("Parsing assets list...")
assets_fte_list = df_fte.columns.tolist()
index_fte_list = [index + 1 for index in df_fte.index.tolist()]

print("Generating numpy matrix and pandas df...")
# numpy matrix
# matrix = _generate_random_matrix(nrows=len(index_fte_list), ncols=len(assets_fte_list))
# df = pd.DataFrame(matrix, columns=[f"{col}_fake" for col in assets_fte_list])
df = pd.DataFrame()

final_df = pd.concat([df_fte, df], axis=1)

print("Parsing pandas df to ampl param format...")
return_df_ampl = pandas_df_to_indexed_ampl_format(df=final_df)

ampl.set["A"] = np.array(final_df.columns.tolist())
ampl.set["T"] = np.array(index_fte_list)
ampl.param["retorno_ativos"] = return_df_ampl

ampl.setOption("solver", "cplex")

start_solve_time = time()

print("Starting solver...")
ampl.solve()

end_solve_time = time()

end_total_runtime = time()


print(f"Demorou {(end_total_runtime - start_total_runtime) / 60} min para rodar E2E.")
print(f"Demorou {(end_solve_time - start_solve_time) / 60} min para rodar o solver.")

final_df = reduce(
    lambda left, right: pd.merge(
        left, right, left_index=True, right_index=True, how="outer"
    ),
    _build_report_dfs_list(
        total_run_time=(end_total_runtime - start_total_runtime) / 60,
        solve_time=(end_solve_time - start_solve_time) / 60,
    ),
)

dump_data_pgsql(
    df=final_df, database="aux", tbl_name="ampl_markowitz", append_data=False
)
