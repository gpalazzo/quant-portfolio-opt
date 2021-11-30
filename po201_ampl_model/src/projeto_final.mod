#passos para a solução

# 1 -> setar parâmetros -- (OK)
#	1.1 -> lista de ativos -- (OK)
#	1.2 -> retorno esperado -- (OK)
#	1.3 -> risco esperado -- (OK)
#	1.4 -> taxa livre de risco -- (OK)

# 2 -> arquivos de dados -- (OK)
#	2.1 -> retorno histórico em diferentes janelas de tempo -- (OK)
#	2.2 -> capitalização de mercado -- (OK)
#	2.3 -> retorno de todos os ativos que compõem o índice -- (OK)

# 3 -> restrições -- (OK)
#	3.1 -> sum wi = 1 (todo capital disponível é investido) -- (OK)
#	3.2 -> 0 <= wi <= 1 (não alavancagem das operações) -- (OK)
#	3.3 -> sum ri * wi >= 0 (retorno positivo dos ativos) -- (OK)

# 4 -> calcular peso ótimo
#	4.1 -> prior -- (OK)
#	4.2 -> investors' view -- (OK)
#	4.3 -> posterior

# 5 -> função objetivo

# 6 -> cálculos matemáticos
#	6.1 -> retorno médio em todas as janelas de tempo -- (OK)
#	6.2 -> diferença entre as janelas de tempo e a média -- (OK)
#	6.3 -> covariância dos retornos -- (OK)
#	6.4 -> desvio padrão

reset;

# ********** SETUP BASE **********

# sets
set A; #lista de ativos
set ROWS := {1..19}; #total de linhas no dataset

# parâmetros
param rf_rate default 0.075; #taxa livre de risco
param min_expected_risk default 0.0005; # mínimo risco esperado
param max_expected_ret default 0.35; # máximo retorno esperado

param monthly_ret {ROWS, A}; #retorno dos ativos em diferentes janelas de tempo
param mktcap {1..1, A}; #capitalização de mercado dos ativos

#retorno médio considerando todas as janelas de tempo
# potencial problema aqui: estou fazendo média de uma janela rolante que já é uma média
param mean_ret {j in A} = (sum {i in ROWS} monthly_ret[i, j]) / card(ROWS);

param diff_monthly_mean {i in ROWS, j in A} = monthly_ret[i, j] - mean_ret[j];

# ********** BL - PRIOR **********
set IBXX;
param prior_cov_ret {i in A, j in A} = sum {k in ROWS} (diff_monthly_mean[k, i] * diff_monthly_mean[k, j]) / (card{ROWS}-1); #covariância dos retornos
param prior_peso_mktcap {a in A} = mktcap[1, a] / (sum {i in A} mktcap[1, i]); #peso inicial baseado em capitalização de mercado
param ibxx_stocks {ROWS, IBXX}; #retorno de todos os ativos do índice em diferentes janelas de tempo

param mean_ret_ibxx_asset {j in A} = (sum {i in ROWS} ibxx_stocks[i, j]) / card(ROWS);
param mean_global_ret = (sum {a in A} mean_ret_ibxx_asset[a]) / card(A);
param var_ret_ibxx = (sum {a in A} (mean_ret_ibxx_asset[a] - mean_global_ret)^2) / card(A);
param lambda_risk_aversion = (mean_global_ret - rf_rate) / var_ret_ibxx;

param prior_staging {i in A, j in A} = prior_cov_ret[i, j] * lambda_risk_aversion;
param prior {i in A} = sum {j in A} prior_staging[i, j] * prior_peso_mktcap[i];

# ********** BL - INVESTORS' VIEW **********
param Q {1..1, A};
param P {1..card(A), A};
param omega {1..card(A), A};

# ********** BL - POSTERIOR **********
param tal = 1 / (card(ROWS) - card(A));

# tal x matriz covariância (falta calcular inversa)
param tal_covar_inv {i in A, j in A} = (prior_cov_ret[i, j] * tal);
#param bl_covar = 

# ********** MODELO **********
# variável de decisão
var w{A} >= 0; #peso de cada ativo da carteira

# objetivo
#maximize Sharpe_Ratio {a in A}: (sum {i in ROWS} w[a] * monthly_ret[i, a] - rf_rate) / 

# restrições
subject to total_peso_um: sum {a in A} w[a] = 1;
subject to nao_alavancagem {a in A}: 0 <= w[a] <= 1;
subject to ret_positivo {a in A}: sum {i in ROWS} w[a] * monthly_ret[i, a] >= 0;

# ***** OBS: aparentemente o objetivo de maximização se dará por um while loop levando em conta o risco e o retorno *****

