from amplpy import AMPL, Environment

ampl = AMPL(Environment("/Users/guilhermepalazzo/Desktop/ampl_macos64"))

base_path = "/Users/guilhermepalazzo/Google Drive/academico/MSc_ITA_UNIFESP/disciplinas/introdução_PO/projeto_final/exemplos_testados/markowitz_dummy"

ampl.read(f"{base_path}/markowitz_example.mod")
ampl.readData(f"{base_path}/markowitz_example.dat")

ampl.solve()

obj = ampl.getObjective("Risk")

print(f"Risco: {obj.value()}")
