from utils import read_data_pgsql


df = read_data_pgsql(database="aux", tbl_name="ampl_markowitz")
excl_cols = ["run_timestamp", "total_run_time_min", "solve_time_min", "mean", "risk"]
select_cols = list(set(df.columns.tolist()) - set(excl_cols))

print(f"Soma dos pesos: {df[select_cols].sum().sum():.2f}")
print(f"Retorno médio: {df['mean'].unique()[0] * 100:.6f}%")
print(f"Risco médio: {df['risk'].unique()[0]:.6f}")
print(f"Tempo total do algoritmo: {df['total_run_time_min'].unique()[0]:.2f} minutos")
print(f"Quantidade de ativos selecionados: {len(select_cols)}")
