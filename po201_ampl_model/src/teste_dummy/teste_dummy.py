from amplpy import AMPL, Environment

ampl = AMPL(Environment("/home/ampl/ampl_linux-intel64"))

base_path = "/home/ampl/src/teste_dummy"

ampl.read(f"{base_path}/markowitz_example.mod")
ampl.readData(f"{base_path}/markowitz_example.dat")

ampl.solve()

obj = ampl.getObjective("Risk")

print(f"Risco: {obj.value()}")
