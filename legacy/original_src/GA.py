import random
import numpy as np
from TSP import generate_random_route, compute_route_distance

def elitism_selection(population, fitness_scores):
    selected_routes = []
    population_size = len(population)
    for i in range(population_size // 2):
        max_fitness_index = fitness_scores.index(min(fitness_scores))  # Minimize distance
        selected_routes.append(population[max_fitness_index])
        fitness_scores[max_fitness_index] = 0  
    return selected_routes

def tournament_selection(population, fitness_scores, tournament_size=3):
    selected_routes = []
    population_size = len(population)
    for _ in range(population_size // 2):  
        # Chọn ngẫu nhiên tournament_size cá thể
        tournament_indices = random.sample(range(population_size), tournament_size)
        tournament_participants = [population[i] for i in tournament_indices]
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        
        # Chọn cá thể có điểm fitness (distance) thấp nhất
        winner_index = tournament_fitness.index(min(tournament_fitness))
        selected_routes.append(tournament_participants[winner_index])

    return selected_routes

def rank_selection(population, fitness_scores):
    sorted_population = [ind for _, ind in sorted(zip(fitness_scores, population))] #sort with fitness
    ranks = np.arange(1, len(population) + 1) #add rank

    probabilities = 1 / ranks
    probabilities /= probabilities.sum()    
    cumulative_probabilities = np.cumsum(probabilities) #mảng cộng dồn

    selected_individuals = []
    population_size = len(population)
    for i in range(population_size // 2):
        r = np.random.rand() 
        for i, cum_prob in enumerate(cumulative_probabilities):
            if r <= cum_prob:
                selected_individuals.append(sorted_population[i])
                break
    return selected_individuals

def roulette_wheel_selection(population, fitness_scores):
    # Chuyển đổi fitness scores thành các giá trị dương (để tối thiểu hóa khoảng cách)
    max_fitness = max(fitness_scores)
    adjusted_fitness = [max_fitness - score for score in fitness_scores]
    
    total_fitness = sum(adjusted_fitness)

    selected_routes = []
    selection_size = max(2,len(population)) // 2  # Đảm bảo ít nhất 2 cá thể được chọn
    for _ in range(selection_size):
        pick = random.uniform(0, total_fitness)
        current = 0
        for i, fitness in enumerate(adjusted_fitness):
            current += fitness
            if current >= pick:  
                selected_routes.append(population[i])
                break
    return selected_routes


def selection (population, fitness_scores,algorithm = 'elitism'):
    if algorithm == 'elitism':
        return elitism_selection(population, fitness_scores)
    if algorithm == 'rank':
        return rank_selection(population, fitness_scores)
    if algorithm == 'tournament':
        return tournament_selection(population, fitness_scores, tournament_size = 3)
    if algorithm == 'roulette_wheel':
        return roulette_wheel_selection(population, fitness_scores)
    return []
    
def order_crossover(parent1, parent2):
    split_index = random.randint(1, len(parent1) - 1)
    child1_part1 = parent1[:split_index]
    child1_part2 = [city for city in parent2 if city not in child1_part1]
    child1 = child1_part1 + child1_part2
    
    child2_part1 = parent2[:split_index]
    child2_part2 = [city for city in parent1 if city not in child2_part1]
    child2 = child2_part1 + child2_part2
    
    return child1, child2

def single_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    # Tạo child1: lấy phần đầu từ parent1 và phần còn lại từ parent2
    child1 = parent1[:crossover_point]
    child1 += [city for city in parent2 if city not in child1]
    # Tạo child2: lấy phần đầu từ parent2 và phần còn lại từ parent1
    child2 = parent2[:crossover_point]
    child2 += [city for city in parent1 if city not in child2]
    return child1, child2

def two_point_crossover(parent1, parent2):
    point1, point2 = sorted(random.sample(range(1, len(parent1)), 2))

    # Crossover for child1
    child1_part1 = parent1[:point1]
    child1_middle = [city for city in parent2[point1:point2] if city not in child1_part1]
    child1_part3 = [city for city in parent1[point2:] if city not in child1_part1 + child1_middle]
    
    # Fill missing cities from parent2
    missing_cities1 = [city for city in parent2 if city not in child1_part1 + child1_middle + child1_part3]
    child1 = child1_part1 + child1_middle + child1_part3 + missing_cities1

    # Crossover for child2 (similar to child1)
    child2_part1 = parent2[:point1]
    child2_middle = [city for city in parent1[point1:point2] if city not in child2_part1]
    child2_part3 = [city for city in parent2[point2:] if city not in child2_part1 + child2_middle]
    
    # Fill missing cities from parent1
    missing_cities2 = [city for city in parent1 if city not in child2_part1 + child2_middle + child2_part3]
    child2 = child2_part1 + child2_middle + child2_part3 + missing_cities2

    return child1, child2

def uniform_crossover(parent1, parent2):
    child1 = [0] * len(parent1)
    child2 = [0] * len(parent1)
    child1[0] = child2[0] = 0  

    for i in range(1, len(parent1)):
        if random.random() < 1:
            child1[i] = parent1[i]
            child2[i] = parent2[i]
        else:
            child1[i] = parent2[i]
            child2[i] = parent1[i]
    
    for child in [child1, child2]:
        used_cities = set([0])
        for i in range(1, len(child)):
            if child[i] in used_cities:
                unused_cities = set(range(1, len(child))) - used_cities
                child[i] = random.choice(list(unused_cities))
            used_cities.add(child[i])
    
    return child1, child2

def crossover(parent1, parent2, algorithm='order'):
    if algorithm == 'order':
        return order_crossover(parent1, parent2)
    if algorithm == 'two_point':
        return two_point_crossover(parent1,parent2)
    if algorithm == 'single_point':
        return single_point_crossover(parent1, parent2)
    if algorithm == 'uniform':
        return uniform_crossover(parent1, parent2)
    return [],[]

def inversion_mutate(route, mutation_rate):
    
    if random.uniform(0, 1) < mutation_rate:
        
        start, end = sorted(random.sample(range(1, len(route)), 2)) 
        
        route[start:end] = reversed(route[start:end])
    return route


def scramble_mutate(route, mutation_rate):
    if random.random() < mutation_rate:
        point1 = random.randint(1, len(route) - 2) 
        point2 = random.randint(point1 + 1, len(route) - 1)

        # Scramble the segment between point1 and point2
        scrambled_segment = route[point1:point2]
        random.shuffle(scrambled_segment)

        mutated_route = route[:point1] + scrambled_segment + route[point2:]
        return mutated_route
    return route

def swap_mutate(route, mutation_rate):
    for i in range(1,len(route)):  
        if random.uniform(0, 1) < mutation_rate:
            j = random.randint(1, len(route) - 1)  
            route[i], route[j] = route[j], route[i] 
    return route

def insertion_mutate(route, mutation_rate):
    if random.random() < mutation_rate:
        
        idx1, idx2 = random.sample(range(1, len(route)), 2)
        if idx1 > idx2:
            idx1, idx2 = idx2, idx1
        
        # Lấy thành phố tại idx2 và chèn nó vào vị trí idx1
        city = route.pop(idx2)
        route.insert(idx1, city)
    
    return route

def mutate(route, mutation_rate, algorithm='swap'):
    if algorithm == 'swap':
        return swap_mutate(route, mutation_rate)
    if algorithm == 'scramble':
        return scramble_mutate(route,mutation_rate)
    if algorithm == 'inversion':
        return inversion_mutate(route, mutation_rate)
    if algorithm == 'insertion':
        return insertion_mutate(route, mutation_rate)
    return []

def fitness(population, distances):
    fitness_scores = []
    for route in population:
        distance = compute_route_distance(route + [route[0]], distances)
        fitness_scores.append(distance)
    return fitness_scores

def genetic_algorithm(n_cities, distances, population_size=100, generations=100, mutation_rate=0.01, 
                      mutation_algorithm='swap', selection_algorithm='elitism', crossover_algorithm='order'):
    # Tạo quần thể ban đầu 
    population = [generate_random_route(n_cities) for _ in range(population_size)]
    fitness_history = []
    for generation in range(generations):
        # Tính điểm fitness
        fitness_scores = fitness(population, distances)
        fitness_history.append(min(fitness_scores))

        # Chọn những tuyến đường tốt nhất
        selected_routes = selection(population, fitness_scores, selection_algorithm)

        # Thực hiện crossover
        offspring = []
        for i in range(population_size // 2):
            parent1, parent2 = random.sample(selected_routes, 2)  # Chọn ngẫu nhiên hai bố mẹ 
            child1, child2 = crossover(parent1, parent2, crossover_algorithm) 
            offspring.extend([child1, child2])

        # Đột biến các cá thể con
        for i in range(len(offspring)):
            offspring[i] = mutate(offspring[i], mutation_rate, mutation_algorithm)

        # Thay thế quần thể cũ bằng quần thể mới
        population = offspring

    # Tìm đường tốt nhất trong quần thể cuối cùng
    best_route = population[0]
    best_distance = compute_route_distance(best_route, distances)
    for route in population:
        route_distance = compute_route_distance(route, distances)
        if route_distance < best_distance:
            best_route = route
            best_distance = route_distance
    best_route = best_route + [best_route[0]]
    best_route = [city + 1 for city in best_route] 
    # Trả về kết quả
    solution = {
        'route': best_route,
        'distance': best_distance,
        'fitness': fitness_history
    }
    return solution
