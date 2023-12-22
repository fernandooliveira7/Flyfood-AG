import random

# Função para ler a matriz de um arquivo
def read_matrix(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        matrix = [list(line.strip().split()) for line in lines]
    return matrix

# Define o arquivo de entrada
input_file = "matriz.txt"

# Lê a matriz do arquivo de entrada
matrix = read_matrix(input_file)

# Encontra os pontos de entrega (exceto R)
points = []
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] not in ['0', 'R']:
            points.append(matrix[i][j])

# Função para calcular o custo de uma ordem de entrega
def calculate_cost(order):
    cost = 0
    order = ['R'] + order + ['R']
    for i in range(len(order) - 1):
        x1, y1 = [index for index, row in enumerate(matrix) if order[i] in row][0], [row.index(order[i]) for row in matrix if order[i] in row][0]
        x2, y2 = [index for index, row in enumerate(matrix) if order[i+1] in row][0], [row.index(order[i+1]) for row in matrix if order[i+1] in row][0]
        cost += abs(x1 - x2) + abs(y1 - y2)
    return cost

# Função para criar uma população inicial de soluções
def generate_initial_population(size):
    population = [random.sample(points, len(points)) for _ in range(size)]
    return population

# Função para selecionar os melhores indivíduos com base no custo
def select_best_individuals(population, num_parents):
    costs = [calculate_cost(individual) for individual in population]
    sorted_population = [x for _, x in sorted(zip(costs, population))]
    return sorted_population[:num_parents]

# Função para cruzar dois indivíduos
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    return child

# Função para mutar um indivíduo
def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Parâmetros do algoritmo genético
population_size = 100
num_generations = 100
num_parents = 50
mutation_rate = 0.1

# Gera uma população inicial
population = generate_initial_population(population_size)

# Executa o algoritmo genético
for generation in range(num_generations):
    parents = select_best_individuals(population, num_parents)
    offspring = []

    while len(offspring) < population_size:
        parent1, parent2 = random.sample(parents, 2)
        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate)
        offspring.append(child)

    population = parents + offspring

# Encontra a melhor solução na última geração
best_solution = min(population, key=calculate_cost)

# Imprime a ordem de entrega com o menor custo
print(' '.join(best_solution))


