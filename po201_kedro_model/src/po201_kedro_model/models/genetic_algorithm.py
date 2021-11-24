import time
import numpy as np
import pandas as pd


class GeneticAlgorithm:
    def __init__(self, initial_df, qty_genes, population_size, risk_free_rate):
        self.initial_df = initial_df
        self.qty_genes = qty_genes
        self.population_size = population_size
        self.risk_free_rate = risk_free_rate
        self.cov_hist_return = None
        self.mean_hist_return = None
        self.sd_hist_return = None
        self.calculate_statistics()

    def create_gene(self):
        pass

    def create_chromosome(self):
        ch = np.random.rand(self.qty_genes)
        return ch / sum(ch)

    def initial_population(self):
        return np.array([self.create_chromosome() for _ in range(self.population_size)])

    def fitness_func(self, child):
        return (self.mean_portfolio_return(child) - self.risk_free_rate) / np.sqrt(
            self.var_portfolio_return(child)
        )

    def var_portfolio_return(self, child):
        part_1 = np.sum(np.multiply(child, self.sd_hist_return) ** 2)
        temp_lst = []

        for i in range(6):
            for j in range(6):
                temp = self.cov_hist_return.iloc[i][j] * child[i] * child[j]
                temp_lst.append(temp)

        part_2 = np.sum(temp_lst)

        return part_1 + part_2

    def mean_portfolio_return(self, child):
        return np.sum(np.multiply(child, self.mean_hist_return))

    def calculate_statistics(self):
        cols = self.initial_df.columns
        self.initial_df[cols] = self.initial_df[cols].apply(
            pd.to_numeric, errors="coerce"
        )

        # covariance
        self.cov_hist_return = self.initial_df.cov()
        # mean
        self.mean_hist_return = self.initial_df.mean()
        # standard deviation
        self.sd_hist_return = self.initial_df.std()

    def Select_elite_population(self, population, frac=0.3):
        """Select elite population from the total population based on fitness function values.
        Input: Population and fraction of population to be considered as elite.
        Output: Elite population."""
        population = sorted(
            population, key=lambda x: self.fitness_func(x), reverse=True
        )
        percentage_elite_idx = int(np.floor(len(population) * frac))
        return population[:percentage_elite_idx]

    def mutation(self, parent):
        """Randomy choosen elements of a chromosome are swapped
        Input: Parent
        Output: Offspring (1D Array)"""
        child = parent.copy()
        n = np.random.choice(range(6), 2)
        while n[0] == n[1]:
            n = np.random.choice(range(6), 2)
        child[n[0]], child[n[1]] = child[n[1]], child[n[0]]
        return child

    def Arithmetic_crossover(self, parent1, parent2):
        """The oﬀsprings are created according to the equation:
            Off spring A = α ∗ Parent1 + (1 −α) ∗ Parent2
            Off spring B = (1 −α) ∗ Parent1 + α ∗ Parent2

                Where α is a random number between 0 and 1.
        Input: 2 Parents
        Output: 2 Children (1d Array)"""
        alpha = np.random.rand()
        child1 = alpha * parent1 + (1 - alpha) * parent2
        child2 = (1 - alpha) * parent1 + alpha * parent2
        return child1, child2

    def next_generation(self, pop_size, elite, crossover=Arithmetic_crossover):
        """Generates new population from elite population with mutation probability as 0.4 and crossover as 0.6.
        Over the final stages, mutation probability is decreased to 0.1.
        Input: Population Size and elite population.
        Output: Next generation population (2D Array)."""
        new_population = []
        elite_range = range(len(elite))
        #     print(elite_range)
        while len(new_population) < pop_size:
            if (
                len(new_population) > 2 * pop_size / 3
            ):  # In the final stages mutation frequency is decreased.
                mutate_or_crossover = np.random.choice([0, 1], p=[0.9, 0.1])
            else:
                mutate_or_crossover = np.random.choice([0, 1], p=[0.4, 0.6])
            #         print(mutate_or_crossover)
            if mutate_or_crossover:
                indx = np.random.choice(elite_range)
                new_population.append(self.mutation(elite[indx]))
            else:
                p1_idx, p2_idx = np.random.choice(elite_range, 2)
                c1, c2 = crossover(elite[p1_idx], elite[p2_idx])
                chk = 0
                for gene in range(6):
                    if c1[gene] < 0:
                        chk += 1
                    else:
                        chk += 0
                if sum(chk) > 0:
                    p1_idx, p2_idx = np.random.choice(elite_range, 2)
                    c1, c2 = crossover(elite[p1_idx], elite[p2_idx])
                new_population.extend([c1, c2])
        return new_population


n = 6  # Number of stocks = 6
pop_size = 100  # initial population = 100


# Initial population
population = np.array([chromosome(n) for _ in range(pop_size)])

# Get initial elite population
elite = Select_elite_population(population)

iteration = 0
Expected_returns = 0
Expected_risk = 1

while (Expected_returns < 0.30 and Expected_risk > 0.0005) or iteration <= 40:
    print("Iteration:", iteration)
    population = next_generation(100, elite, Arithmetic_crossover)
    elite = Select_elite_population(population)
    Expected_returns = mean_portfolio_return(elite[0])
    Expected_risk = var_portfolio_return(elite[0])
    print(
        "Expected returns of {} with risk of {}\n".format(
            Expected_returns, Expected_risk
        )
    )
    iteration += 1

print("Portfolio of stocks after all the iterations:\n")
[print(hist_stock_returns.columns[i], ":", elite[0][i]) for i in list(range(6))]

print(
    "\nExpected returns of {} with risk of {}\n".format(Expected_returns, Expected_risk)
)
