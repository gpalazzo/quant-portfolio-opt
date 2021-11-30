from amplpy import AMPL, Environment, DataFrame
import pandas as pd
import numpy as np
from utils import ampl_list_to_df


ampl = AMPL(Environment("/home/ampl/ampl_linux-intel64"))

base_path = "/home/ampl/src"

ampl.read(f"{base_path}/projeto_final.mod")
ampl.readData(f"{base_path}/projeto_final.dat")

bl_investors_view_P = ampl.getParameter("P")
P_list = bl_investors_view_P.getValues().toList()

bl_prior_covar = ampl.getParameter("prior_cov_ret")

breakpoint()

P_pdf = ampl_list_to_df(ampl_list=P_list)

breakpoint()
