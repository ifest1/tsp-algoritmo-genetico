import random
# classe que representa o indivíduo/cromossomo
class Route:
  def __init__(self, path, length):
    self.path = path
    self.length = length
    self.fitness = 0

  def __repr__(self):
    return self.path
  
  def __str__(self):
    return self.path

  def get_path(self):
    return self.path

  def get_length(self):
    return self.length

  def get_fitness(self):
    return self.fitness

  def set_fitness(self, position):
    route, length = self.path, self.length
    s_route = i = 0

    while i + 1 < length:
      s_route += self.get_distance(position[route[i]], position[route[i + 1]])
      i += 1

    self.fitness = (1 / s_route)

  def get_distance(self, position1, position2):
    return (abs(position1[0] - position2[0]) + abs(position1[1] - position2[1]))


class GeneticAlgorithm:
  def __init__(self, 
              source,
              p_mutate=0.4, 
              p_crossover=0.4, 
              generation_limit=100,
              initial_pop_size=100):

    # parâmetros do algoritmo
    self.p_mutate = p_mutate
    self.p_crossover = p_crossover
    self.initial_pop_size = initial_pop_size
    self.generation_limit = generation_limit

    # rotas, cidades e posição de cada cidade
    self.source = source
    self.cities = []
    self.position = {}
    self.routes = []


  # nesse método acontece a seleção dos indivíduos, crossover e mutação  
  def do_ga(self):
    self.generate_random_population()
    
    temp_population = self.routes

    self.routes = []

    for generation in range(self.generation_limit):
      route1 = self.get_random_route(temp_population)
      route2 = self.get_random_route(temp_population)
    
      for _ in range(self.initial_pop_size // 2):
        
        children = self.crossover(
          route1.get_path(),
          route2.get_path())

        if children is not None:
          ch1, ch2 = children

          self.routes.append(self.mutate(ch1))
          self.routes.append(self.mutate(ch2))

    print(self.get_best_route())

  # retorna a rota com maior fitness
  def get_best_route(self):
    return max(self.routes, key=lambda route: route.fitness)

  # retorna uma rota aleatória levando em consideração seu fitness
  def get_random_route(self, routes):
    total_fitness = sum([x.get_fitness() for x in routes])

    n = random.uniform(0, total_fitness)

    for route in routes:
      if n < route.fitness:
        return route
        
      n = n - route.fitness

  # gera a população inicial random
  def generate_random_population(self):
    for _ in range(self.initial_pop_size):
      temp = self.cities
      random.shuffle(temp)

      temp = ''.join(temp)
      temp = self.source + temp + self.source

      route = Route(temp, len(temp))
      route.set_fitness(self.position)

      self.routes.append(route)

  # mutação do cromossomo
  def mutate(self, route):
    if random.random() < self.p_mutate:
      path = route.get_path()
      len_path = len(path)
      new_path = list(path)

      i = random.randint(1, len_path - 2)
      j = random.randint(1, len_path - 2)
      
      if i != j: 
        new_path[i], new_path[j] = path[j], path[i]
        new_path = ''.join(new_path)
        new_route = Route(new_path, len_path)
        new_route.set_fitness(self.position)
    
    return route

  # faz o crossover (retorna dois descendentes)
  def crossover(self, path1, path2):
    placeholder = 'x'
    if random.random() < self.p_crossover:
      path1 = path1[1:-1]
      path2 = path2[1:-1]
      length = len(path1)
      random_int = random.randint(0, length - 3)
      f_cut, s_cut = random_int, random_int + 3
  
      o1 = placeholder * (f_cut) + path2[f_cut: s_cut] + placeholder * (length - s_cut)
      o2 = placeholder * (f_cut) + path1[f_cut: s_cut] + placeholder * (length - s_cut)
      
      l_o1, l_o2 =  list(o1), list(o2)
      remaining1 = remaining2 = ''

      for i in range(length):
        if path1[i] not in o1: remaining1 += path1[i]
        if path2[i] not in o2: remaining2 += path2[i]
      
      for i in range(length):
        if l_o1[i] == placeholder:
          l_o1[i] = remaining1[0]
          remaining1 = remaining1[1:]

        if l_o2[i] == placeholder:
          l_o2[i] = remaining2[0]
          remaining2 = remaining2[1:]
      
      o1 = ''.join(l_o1)
      o2 = ''.join(l_o2)
      
      o1 = self.source + o1 + self.source
      o2 = self.source + o2 + self.source

      route1 = Route(o1, len(o1))
      route2 = Route(o2, len(o2))
      
      route1.set_fitness(self.position)
      route2.set_fitness(self.position)

      return route1, route2

    return None

  def set_city(self, city):
    self.cities += city

  def set_distance(self, city, position):
    self.position[city] = (position)

def main():
    source = 'R'
    not_city = '0'
    g_algo = GeneticAlgorithm(source, )

    l, c = [int(x) for x in input().split()]
    
    for i in range(l):
        for j, c in enumerate(input().split()):
            if c != not_city:
                g_algo.set_distance(c, (i, j))
                if c != source: g_algo.set_city(c)
    g_algo.do_ga()

main()
