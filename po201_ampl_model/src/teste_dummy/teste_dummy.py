from amplpy import AMPL, Environment
import pandas as pd


ampl = AMPL(Environment("/home/ampl/ampl_linux-intel64"))

base_path = "/home/ampl/src/teste_dummy"

ampl.read(f"{base_path}/diet.mod")
ampl.readData(f"{base_path}/diet.dat")

ampl.setOption("solver", "cplex")

x_values = {
    (1, 1): 3,
    (6, 3): -1,
    (99, 5): 15,
}

df = pd.DataFrame.from_dict(x_values, orient="index", columns=["value"])
print("df:", df)

ampl.param["x"] = df

breakpoint()

x = ampl.getParameter("x")

breakpoint()


# ampl.solve()

# obj = ampl.getObjective("Total_Cost")
#
# print(f"Cost: {obj.value()}")
#
# cost = ampl.getParameter("cost")
#
# breakpoint()
#
# cost.setValues({"BEEF": 5.01, "HAM": 4.55})
#
# # cost.getValues().toList()
