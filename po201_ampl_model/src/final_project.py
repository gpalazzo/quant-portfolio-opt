"""
TODO:
    - fazer um loop com umas 5 combinações de ativo para testar pegar o maior deles
    - gerar a combinação de todos os ativos e rodar no loop
"""

from amplpy import AMPL, Environment
import pandas as pd
import numpy as np
from utils import ampl_list_to_pandas_df, pandas_df_to_indexed_ampl_format
from itertools import chain, combinations
from datetime import datetime, timedelta
from functools import reduce
from sqlalchemy import create_engine
import os
import uuid
from time import sleep, time


def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(15, len(ss) + 1)))


def dump_data_pgsql(
    df: pd.DataFrame,
    database: str,
    tbl_name: str = None,
    append_data: bool = True,
) -> None:

    print(f"Dumping data to PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    try:
        if append_data:
            df.to_sql(tbl_name, engine, if_exists="append", index=False)

        else:
            df.to_sql(tbl_name, engine, if_exists="replace", index=False)

    except Exception as e:
        print("Erro")
        print(e.args)


def read_data_pgsql(
    database: str, tbl_name: str = None, query: str = None
) -> pd.DataFrame:

    print(f"Reading data from PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    if not query:
        df = pd.read_sql_query(
            f'select * from {database}.public."{tbl_name}"', con=engine
        )

    else:
        pass  # testar execução de query aqui

    return df


ampl = AMPL(Environment("/home/ampl/ampl_linux-intel64"))

session_uuid = uuid.uuid4()

base_path = "/home/ampl/src"

# read model files
ampl.read(f"{base_path}/projeto_final.mod")
ampl.readData(f"{base_path}/projeto_final.dat")

# get parameters needed for calculations
## list of assets
assets = ampl.getSet("A")
assets_list = assets.getValues().toList()
assets_comb_list = []

for subset in all_subsets(assets_list):
    assets_comb_list.append(list(subset))

start = time()

for i, assets_comb in enumerate(assets_comb_list, 1):

    # sleep somente para garantir que o dump de dados ocorrerá sem problemas no Postgres
    sleep(0.1)

    print(f"***** --> Rodando a {i}a combinação...")
    print(f"***** --> Total de combinações: {len(assets_comb_list)}")

    # reseta contexto antes de cada iteração para limpar memória
    ampl.reset()

    # read model files
    ampl.read(f"{base_path}/projeto_final.mod")
    ampl.readData(f"{base_path}/projeto_final.dat")

    ampl.set["A"] = np.array(assets_comb)

    ## prior
    bl_prior_covar = ampl.getParameter("prior_cov_ret")
    bl_prior = ampl.getParameter("prior")

    ## investors' view
    bl_investors_view_P = ampl.getParameter("P")
    bl_investors_view_tal = ampl.getParameter("tal")

    bl_investors_view_omega = ampl.getParameter("omega")
    bl_investors_view_Q = ampl.getParameter("Q")

    # parse parameters
    ## prior
    prior_cov_ret_list = bl_prior_covar.getValues().toList()
    df_prior_cov_ret = ampl_list_to_pandas_df(
        ampl_list=prior_cov_ret_list, cols_as_index=True, n_stocks=len(assets_comb)
    )

    prior_list = bl_prior.getValues().toList()
    df_prior = pd.DataFrame(prior_list, columns=["stock", "prior"]).set_index("stock")

    ## investors' view
    P_list = bl_investors_view_P.getValues().toList()
    df_P = ampl_list_to_pandas_df(ampl_list=P_list, n_stocks=len(assets_comb))

    scalar_tal = bl_investors_view_tal.getValues().toList()[0]

    omega_list = bl_investors_view_omega.getValues().toList()
    df_omega = ampl_list_to_pandas_df(ampl_list=omega_list, n_stocks=len(assets_comb))

    Q_list = bl_investors_view_Q.getValues().toList()
    df_Q = ampl_list_to_pandas_df(ampl_list=Q_list, n_stocks=len(assets_comb))

    # calculations
    ## (tal x covar)^-1
    tal_covar_inv = np.linalg.inv(df_prior_cov_ret.to_numpy() * scalar_tal)

    ## P^T x Omega^-1
    _np_omega = df_omega.to_numpy()
    if np.linalg.det(_np_omega) == 0:
        m = np.mean(_np_omega[_np_omega > 0])
        _np_omega[_np_omega != 0] = m
        PT_OmegaInv = np.matmul(df_P.to_numpy().transpose(), _np_omega)
    else:
        PT_OmegaInv = np.matmul(df_P.to_numpy().transpose(), np.linalg.inv(_np_omega))

    ## P^T x Omega^-1 x P
    PT_OmegaInv_P = np.matmul(PT_OmegaInv, df_P.to_numpy())

    ## covariância BL
    covar_bl = np.linalg.inv(tal_covar_inv + PT_OmegaInv_P)

    ## média BL
    _tmp = np.matmul(tal_covar_inv, df_prior.to_numpy())
    _tmp2 = np.matmul(PT_OmegaInv, df_Q.to_numpy().transpose())

    media_staging = _tmp + _tmp2
    media_bl = np.matmul(covar_bl, media_staging)

    # parse covariância BL
    covar_bl_df = pd.DataFrame(covar_bl)
    covar_bl_df.index = covar_bl_df.index + 1
    covar_bl_df.columns = [col + 1 for col in covar_bl_df.columns]

    covar_bl_indx = pandas_df_to_indexed_ampl_format(df=covar_bl_df)

    # cálculo final
    weight = np.matmul(np.linalg.inv(covar_bl_df), media_bl)
    df_weight = pd.DataFrame(weight.transpose())
    df_weight.columns = df_prior_cov_ret.columns.tolist()
    # weight's normalization
    _total_abs_weight = abs(df_weight.sum()).sum()
    df_weight = abs(df_weight / _total_abs_weight)

    data_values = {}

    for j, row in df_weight.iterrows():
        for k in range(0, len(row)):
            _key = (j + 1, row.index[k])
            data_values[_key] = row[k]

    weight = pd.DataFrame.from_dict(data_values, orient="index", columns=["value"])

    # seta valores AMPL
    # ampl.param["covar_bl"] = covar_bl_indx
    # ampl.param["mean_bl"] = media_bl
    ampl.param["w"] = weight

    ampl.setOption("solver", "cplex")

    ampl.solve()

    _session_uuid = pd.DataFrame({"uuid": session_uuid}, index=[0])

    _now = datetime.now() - timedelta(hours=3)
    _time_df = pd.DataFrame({"run_timestamp": _now}, index=[0])

    df_weight_aux = df_weight.copy()
    weight_cols = df_weight_aux.columns.tolist()
    assets_excl = list(set(assets_list) - set(weight_cols))
    df_weight_aux[assets_excl] = None

    _risk = ampl.getParameter("portfolio_stdev").getValues().toList()[0]
    _risk_df = pd.DataFrame({"risk": _risk}, index=[0])

    _return = ampl.getParameter("mean_ret").getValues().toList()
    _return_np = (
        pd.DataFrame(_return, columns=["stock", "return"]).set_index("stock").to_numpy()
    )
    _return = np.matmul(df_weight.to_numpy(), _return_np)[0][0]
    _return_df = pd.DataFrame({"return": _return}, index=[0])

    _sharpe_ratio = ampl.getParameter("Sharpe_Ratio").getValues().toList()[0]
    _sharpe_ratio_df = pd.DataFrame({"sharpe_ratio": _sharpe_ratio}, index=[0])

    dfs = [
        _session_uuid,
        _time_df,
        df_weight_aux,
        _risk_df,
        _return_df,
        _sharpe_ratio_df,
    ]

    final_df = reduce(
        lambda left, right: pd.merge(
            left, right, left_index=True, right_index=True, how="outer"
        ),
        dfs,
    )

    dump_data_pgsql(df=final_df, database="aux", tbl_name="ampl_report")

    # if i == 10:
    #     break

time_df = pd.DataFrame(
    {"uuid": session_uuid, "run_time_sec": time() - start}, index=[0]
)
dump_data_pgsql(df=time_df, database="aux", tbl_name="ampl_run_time")
