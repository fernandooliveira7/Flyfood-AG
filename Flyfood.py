import random
import matplotlib.pyplot as plt
import time
random.seed(328315)
class Pontos:

    def __init__(self, numero, coord_x, coord_y):
        self.numero = numero
        self.coord_x = coord_x
        self.coord_y = coord_y

    def __repr__(self):
        return f'{int(self.numero)}'

    def distancia(self, Pontos):
        xDistancia = (self.coord_x - Pontos.coord_x)**2
        yDistancia = (self.coord_y - Pontos.coord_y)**2
        distancia = (xDistancia + yDistancia)**(1/2)
        return distancia

class Route:
    def __init__(self, rota, fitness=None):
        self.rota = rota
        self.fitness = fitness

class Population:

    def __init__(self):
        self.individuals = []

    def add(self, solution):
        self.individuals.append(solution.rota)

    def addfrente(self, solution):
        self.individuals.insert(0, solution)

    def sort_individuals(self):
        self.individuals.sort(key=lambda x: (route_distance(x)))

    def size(self):
        return len(self.individuals)


def route_distance(sequence):
    distancia_total = 0
    for i in range(len(sequence) - 1):
        ponto_atual = sequence[i]
        proximo_ponto = sequence[i + 1]
        distancia_total += (ponto_atual.distancia(proximo_ponto))
    return distancia_total

def newroutes(locais):
    rota = random.sample(locais, len(locais))
    return rota

def initial_population(locais, len_pop):
    population = Population()
    while population.size() < len_pop:
        lista_temporaria = newroutes(locais)
        lista_temporaria.insert(0, ponto_inicial)
        lista_temporaria.append(ponto_inicial)
        if lista_temporaria not in population.individuals:
            population.add(Route(lista_temporaria, route_distance(lista_temporaria)))
    return population

def torneio(population):
    choices = random.choices(population.individuals, k=2)
    best_ind = None
    best_fit = float('inf')

    for i in choices:
        distance = route_distance(i)
        if distance < best_fit:
            best_fit = distance
            best_ind = i
    return best_ind

def crossover(pai1, pai2, crossover_tax):

    if random.random() <= crossover_tax:

        partition = random.randint(1, len(pai1))
        filho1, filho2 = pai1, pai2
        pai1, pai2 = tuple(pai1), tuple(pai2)

        for i in range(len(pai1)):
            if i <= partition:
                if filho1[i] != pai2[i]:
                    substituir = filho1[i]
                    encontrar = pai2[i]
                    j = i
                    while j < len(filho1):
                        if filho1[j] == encontrar:
                            filho1[j] = substituir
                            j = len(filho1)
                        j += 1
                    filho1[i] = encontrar
            else:
                if filho2[i] != pai1[i]:
                    substituir = filho2[i]
                    encontrar = pai1[i]
                    j = 0
                    while j < len(filho2):
                        if filho2[j] == encontrar:
                            filho2[j] = substituir
                            j = len(filho1)
                        j += 1
                    filho2[i] = encontrar
    else:
        return list(pai1).copy(), list(pai2).copy()
    return filho1, filho2


def mutation(individuo, taxaDeMutacao):
    for i in range(1, len(individuo)-1):
        if (random.random() < taxaDeMutacao):

            trocarCom = random.randrange(1, len(individuo))

            while trocarCom == 0 or trocarCom == len(individuo)-1:
                trocarCom = random.randrange(1, len(individuo))

            ponto1 = individuo[i]
            ponto2 = individuo[trocarCom]

            individuo[i] = ponto2
            individuo[trocarCom] = ponto1
    return individuo

def new_population(curr_population, elitism, crossover_tax, mutation_tax):
    new_pop = Population()
    curr_population.sort_individuals()
    melhor_ind = []
    for i in range(0, elitism):
        melhor_ind.append(tuple(curr_population.individuals[i]))
    while len(new_pop.individuals) < len(curr_population.individuals)-elitism:
        dad1 = torneio(curr_population)
        dad2 = torneio(curr_population)
        f1, f2 = crossover(dad1, dad2, crossover_tax)
        f1 = mutation(f1, mutation_tax)
        f2 = mutation(f2, mutation_tax)
        if f1 not in new_pop.individuals:
            new_pop.individuals.append(f1)
        if f2 not in new_pop.individuals and len(new_pop.individuals) < len(curr_population.individuals)-elitism:
            new_pop.individuals.append(f2)
    for i in range(len(melhor_ind)-1, -1, -1):
        new_pop.addfrente(list(melhor_ind[i]))
    return new_pop


def algoritmoGenetico(locais, tamanhoDaPopulacaoInicial, taxadecrossover, taxaDeMutacao, numeroDeGeracoes):
    pop = initial_population(locais, tamanhoDaPopulacaoInicial)
    pop.sort_individuals()
    bestrota = pop.individuals[0]
    '''''
    print(route_distance(bestrota))
    X = []
    y = []
    for i in range(len(bestrota)):
        X.append(bestrota[i].coord_x)
        y.append(bestrota[i].coord_y)
    plt.plot(X, y, 'b--o')
    plt.title('Melhor rota | Geração 1')
    plt.plot(color='green', marker='o', linestyle='-', linewidth=2)
    plt.show()
    '''
    short_distance = []
    #n = 2000
    for i in range(1, numeroDeGeracoes + 1):
        pop = new_population(pop, tamanhoElitismo, taxadecrossover, taxaDeMutacao)

        pop.sort_individuals()
        bestrota = pop.individuals[0]
        menor_distancia = route_distance(bestrota)
        print(menor_distancia)
        short_distance.append(menor_distancia)
        '''''
        if i == n:
            X = []
            y = []
            for i in range(len(bestrota)):
                X.append(bestrota[i].coord_x)
                y.append(bestrota[i].coord_y)
            plt.plot(X, y, 'b--o')
            plt.title('Melhor rota | Geração {}'.format(n))
            plt.plot(color='green', marker='o', linestyle='-', linewidth=2)
            plt.show()
            n += 2000
        
    X = []
    y = []
    for i in range(len(bestrota)):
        X.append(bestrota[i].coord_x)
        y.append(bestrota[i].coord_y)
    plt.plot(X, y, 'b--o')
    plt.title('Melhor rota | Geração {}'.format(numeroDeGeracoes))
    plt.plot(color='green', marker='o', linestyle='-', linewidth=2)
    plt.show()
'''
    plt.plot(short_distance)
    plt.ylabel('Menor distancia')
    plt.xlabel('Geração')
    plt.title('Menor distância vs Geração')
    plt.tight_layout()
    plt.show()
    return bestrota


#Main
ini = time.time()
locais = []
arquivo = open('a280.tsp', 'r')
for linha in arquivo.readlines():
    linhasplit = linha.split()
    coordenadas = []
    coordenadas.append(linhasplit[0])
    coordenadas.append(linhasplit[1])
    coordenadas.append(linhasplit[2])
    if linhasplit[0] != '1':
        locais.append(Pontos(int(linhasplit[0]), int(linhasplit[1]), int(linhasplit[2])))
    else:
        ponto_inicial = (Pontos(int(linhasplit[0]), int(linhasplit[1]), int(linhasplit[2])))

tamanhoDaPopulacaoInicial = 30
tamanhoElitismo = 2
taxaDeMutacao = 0.01
taxadecrossover = 0.6
numeroDeGeracoes = 10000
melhorrota = algoritmoGenetico(locais, tamanhoDaPopulacaoInicial, taxadecrossover, taxaDeMutacao, numeroDeGeracoes)
#print(melhorrota)
fim = time.time()
print("tempo de execução:", fim-ini)

