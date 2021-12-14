import numpy as np
import pandas as pd
import uuid
from datetime import datetime, timedelta
from functools import reduce
import time
import pygad
import os
import multiprocessing


os.environ["NUMEXPR_MAX_THREADS"] = f"{multiprocessing.cpu_count() - 1}"

global ret_covar
global ret_mean
global ret_stdev


def model_run(
    initial_df,
    num_generations,
    init_range_low,
    init_range_high,
    crossover_type,
    mutation_type,
    mutation_percent_genes,
    parent_selection_type,
    keep_parents,
    num_parents_mating,
    sol_per_pop,
    min_expected_risk,
):
    def _calc_var_portfolio_ret(weights):

        part_1 = np.sum(np.multiply(weights, ret_stdev) ** 2)
        temp_lst = []

        for i in range(len(weights)):
            for j in range(len(weights)):
                temp = ret_covar.iloc[i][j] * weights[i] * weights[j]
                temp_lst.append(temp)

        part_2 = np.sum(temp_lst)

        return part_1 + part_2

    def _calculate_fit_stats(weights):

        mean_portfolio_ret = np.sum(np.multiply(weights, ret_mean))
        stdev_portfolio_ret = np.sqrt(_calc_var_portfolio_ret(weights=weights))

        return mean_portfolio_ret, stdev_portfolio_ret

    def fitness_func(solution, solution_idx):

        print(f"Calculating fitness for solution {solution_idx}...")
        total_weight = sum(solution)
        weights_norm = pd.Series(
            [solution_norm / total_weight for solution_norm in solution]
        )

        _risk = np.dot(weights_norm, np.dot(ret_covar, weights_norm))

        fitness = (1 / (_risk - min_expected_risk)) * -1

        # breakpoint()

        print(f"Fitness value: {fitness}")

        return fitness

    global ret_covar
    global ret_mean
    global ret_stdev

    ret_mean = initial_df.mean()
    ret_covar = initial_df.cov()
    ret_stdev = initial_df.std()

    # cols_len = list(range(len(initial_df.columns.tolist())))
    # ret_covar.columns = cols_len
    # ret_covar.index = cols_len

    fitness_function = fitness_func
    num_genes = len(initial_df.to_numpy()[0])

    ga_instance = pygad.GA(
        # initial_population=function_inputs, #VERIFICAR ESSE PARAMETRO
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_function,
        sol_per_pop=sol_per_pop,
        num_genes=num_genes,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes,
        stop_criteria=f"saturate_{sol_per_pop}",
    )

    start_run_time = time.time()

    print("Start running...")
    ga_instance.run()

    end_run_time = time.time()

    print(f"Time to run in seconds: {end_run_time - start_run_time}")

    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    total = sum(solution)
    weights_norm = [_solution / total for _solution in solution]

    mean_portfolio_ret = np.sum(weights_norm * ret_mean)
    stdev_portfolio_ret = np.dot(weights_norm, np.dot(ret_covar, weights_norm))

    # TESTES

    cols = initial_df.columns.tolist()
    w = {"stock": cols, "peso": weights_norm}
    wdf = pd.DataFrame.from_dict(w)
    rdf = (
        pd.DataFrame(ret_mean, columns=["retorno"])
        .reset_index()
        .rename(columns={"index": "stock"})
    )
    df = pd.merge(left=wdf, right=rdf, on=["stock"])

    breakpoint()

    # TESTES

    breakpoint()

    print(f"Risco: {stdev_portfolio_ret}")
    print(f"Retorno: {mean_portfolio_ret}")
    print(f"Soma dos pesos: {sum(weights_norm)}")

    breakpoint()


def build_report(
    _initial_df,
    qty_genes,
    _elite,
    _expected_returns,
    _expected_risk,
    _rf_rate,
    start_time,
):

    end = time.time()
    uuid_session = uuid.uuid4()
    info_df = pd.DataFrame(
        {"uuid": uuid_session, "run_timestamp": datetime.now() - timedelta(hours=3)},
        index=[0],
    )

    run_time_df = pd.DataFrame(
        {"uuid": uuid_session, "run_time_sec": end - start_time},
        index=[0],
    )

    weights = {}

    print("Portfolio of stocks after all the iterations:\n")
    for i in list(range(qty_genes)):
        weights[_initial_df.columns[i]] = _elite[0][i]
    print(f"Sum of total weights: {sum(weights.values())}")

    weights_df = pd.DataFrame(weights, index=[0])

    print(
        "\nExpected returns of {} with risk of {}\n".format(
            _expected_returns, _expected_risk
        )
    )

    _sharpe = (_expected_returns - _rf_rate) / _expected_risk

    _df_aux = pd.DataFrame(
        {"risk": _expected_risk, "return": _expected_returns, "sharpe_ratio": _sharpe},
        index=[0],
    )

    dfs = [info_df, weights_df, _df_aux]

    final_df = reduce(
        lambda left, right: pd.merge(
            left, right, left_index=True, right_index=True, how="outer"
        ),
        dfs,
    )

    return final_df, run_time_df
