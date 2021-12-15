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
global counter


def model_run(
    initial_df,
    num_generations,
    crossover_type,
    mutation_type,
    mutation_percent_genes,
    parent_selection_type,
    keep_parents,
    num_parents_mating,
    sol_per_pop,
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

    def fitness_func(solution, solution_idx):
        print(f"Calculating fitness for solution {solution_idx}...")
        total_weight = sum(solution)
        solution = [solution_norm / total_weight for solution_norm in solution]

        stdev_portfolio_ret = np.sqrt(_calc_var_portfolio_ret(weights=solution))

        fitness = 1 / stdev_portfolio_ret

        print(f"Fitness value: {fitness}")

        return fitness

    def on_generation(ga_instance):

        global counter
        counter += 1

        if counter == 10:
            return "stop"
        else:
            pass

    global ret_covar
    global ret_mean
    global ret_stdev

    ret_mean = initial_df.mean()
    ret_covar = initial_df.cov()
    ret_stdev = initial_df.std()

    fitness_function = fitness_func

    inputs = initial_df.to_numpy()
    num_genes = len(inputs[0])

    ga_instance = pygad.GA(
        initial_population=inputs,
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_function,
        sol_per_pop=sol_per_pop,
        num_genes=num_genes,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes,
        # stop_criteria="saturate_5",
        on_generation=on_generation,
    )

    start_run_time = time.time()

    print("Start running...")
    ga_instance.run()

    end_run_time = time.time()

    print(f"Time to run in seconds: {end_run_time - start_run_time}")

    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    total = sum(solution)
    weights_norm = [_solution / total for _solution in solution]

    breakpoint()

    mean_portfolio_ret = np.sum(np.multiply(weights_norm * ret_mean))
    stdev_portfolio_ret = np.sqrt(_calc_var_portfolio_ret(weights=weights_norm))

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
