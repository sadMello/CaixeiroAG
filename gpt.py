#%%
import random
import numpy as np

# Defina suas cidades como pontos com coordenadas (x, y)
cities = [(0, 0), (1, 2), (3, 2), (2, 4), (4, 4)]

# Função para calcular a distância total de uma rota
def total_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        city1 = route[i]
        city2 = route[i + 1]
        distance += np.linalg.norm(np.array(cities[city1]) - np.array(cities[city2]))
    return distance

# Função de adaptação (fitness) - inverso da distância total
def fitness(route):
    return 1 / total_distance(route)

# Geração de uma população inicial aleatória
def initialize_population(population_size):
    num_cities = len(cities)
    population = []
    for _ in range(population_size):
        route = list(range(num_cities))
        random.shuffle(route)
        population.append(route)
    return population

# Seleção de pais com base na roleta
def select_parents(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    return random.choices(population, probabilities, k=2)

# Cruzamento (crossover) usando o operador de ordem
def crossover(parent1, parent2):
    num_cities = len(parent1)
    start = random.randint(0, num_cities - 2)
    end = random.randint(start + 1, num_cities - 1)
    
    segment = parent1[start:end]
    child = [city for city in parent2 if city not in segment]
    child[start:start] = segment
    
    return child

# Mutação simples - troca de duas cidades
def mutate(individual):
    num_cities = len(individual)
    idx1, idx2 = random.sample(range(num_cities), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Algoritmo genético principal
def genetic_algorithm(population_size, generations):
    population = initialize_population(population_size)
    
    for _ in range(generations):
        fitness_values = [fitness(individual) for individual in population]
        new_population = []
        
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitness_values)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.extend([child, parent1])  # Substitui metade da população pelos filhos
        
        population = new_population
    
    best_individual = max(population, key=fitness)
    best_distance = total_distance(best_individual)
    
    return best_individual, best_distance

# Exemplo de uso
if __name__ == "__main__":
    population_size = 100
    generations = 1000
    
    best_route, best_distance = genetic_algorithm(population_size, generations)
    
    print("Melhor rota encontrada:", best_route)
    print("Melhor distância encontrada:", best_distance)

# %%
