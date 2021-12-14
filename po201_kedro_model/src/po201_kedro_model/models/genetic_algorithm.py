import numpy as np
import pandas as pd
import uuid
from datetime import datetime, timedelta
from functools import reduce
import time
import pygad


global ret_covar


def model_run(
    initial_df,
    desired_output,
    num_generations,
    init_range_low,
    init_range_high,
    crossover_type,
    mutation_percent_genes,
    parent_selection_type,
    keep_parents,
    num_parents_mating,
    sol_per_pop,
):
    def fitness_func(solution, solution_idx):

        target_risk = 0

        calculated_risk = np.dot(solution.T, np.dot(ret_covar, solution))

        # return calculated_risk - target_risk

        return 1 / np.abs(calculated_risk - target_risk)

    def mutation_func(offspring, ga_instance):
        # This is random mutation that mutates a single gene.
        for chromosome_idx in range(offspring.shape[0]):
            # Make some random changes in 1 or more genes.
            random_gene_idx = np.random.choice(range(offspring.shape[0]))

            offspring[chromosome_idx, random_gene_idx] += np.random.random()

        return offspring

    global ret_covar
    ret_covar = initial_df.cov()
    cols_len = list(range(len(initial_df.columns.tolist())))
    ret_covar.columns = cols_len
    ret_covar.index = cols_len

    function_inputs = initial_df.to_numpy()

    fitness_function = fitness_func
    num_genes = len(function_inputs[0])

    ga_instance = pygad.GA(
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
        mutation_type=mutation_func,
        mutation_percent_genes=mutation_percent_genes,
    )

    start_run_time = time.time()

    ga_instance.run()

    end_run_time = time.time()

    print(f"Time to run in seconds: {end_run_time - start_run_time}")

    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    total = sum(solution)
    weights_norm = [_solution / total for _solution in solution]

    breakpoint()

    calculated_risk = np.dot(pd.Series(weights_norm).T, np.dot(ret_covar, weights_norm))

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
