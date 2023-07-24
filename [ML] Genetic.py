import random
import statistics

# Genetic Algorithm Parameters
population_size = 100
num_genes = 10
mutation_rate = 0.01
num_generations = 100

# Generate the initial population
population = []
for _ in range(population_size):
    individual = [random.randint(0, 100) for _ in range(num_genes)]
    # print(statistics.stdev(individual))
    population.append(individual)

# Define the fitness function
def fitness(individual):
    return 50 - statistics.stdev(individual)

# Main Genetic Algorithm Loop
for generation in range(num_generations):
    # Evaluate the fitness of each individual in the population
    fitness_scores = [fitness(individual) for individual in population]

    # Select parents for mating
    mating_pool = []
    for _ in range(population_size):
        parent1 = random.choices(population, weights=fitness_scores)[0]
        parent2 = random.choices(population, weights=fitness_scores)[0]
        mating_pool.append((parent1, parent2))

    # Create the next generation
    population = []
    for parents in mating_pool:
        parent1, parent2 = parents
        child = []
        for gene_index in range(num_genes):
            if random.random() < mutation_rate:
                # Mutation: randomly change the gene value
                child.append(random.randint(0, 100))
            else:
                # Crossover: inherit gene from parents
                if random.random() < 0.5:
                    child.append(parent1[gene_index])
                else:
                    child.append(parent2[gene_index])
        population.append(child)

# Find the best individual in the final population
best_individual = max(population, key=fitness)
best_fitness = fitness(best_individual)

print("Best Individual:", best_individual)
print("Best Fitness:", best_fitness)
