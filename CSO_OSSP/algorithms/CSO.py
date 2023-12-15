from solution import solution
from ossp import ossp
import numpy as np
from itertools import permutations
import random

class CSO:
    def __init__(self, max_efos: int, max_local: int, size:int,mr:float, spc:False, problem=ossp):
        self.max_efos = max_efos
        self.max_local = max_local
        self.size = size #Cantidad de gatos que se crearán
        self.poblation = [] #Arreglo de N gatos
        self.mr = mr #Taza para definir gatos en búsqueda y rastreo
        self.spc = spc
        self.efo = 0
    def evolve(self, seed: int, problem: ossp):
        self.problem = problem
        self.best = solution(self.problem)
        np.random.seed(seed)
        best_fitness_history = []
        best_cat_solution_history = []
        for cat in range(self.size):
                S = solution(problem)
                S.cells = cat
                self.poblation.append(S.Initialization())
                self.efo+=1
        # Se asigna una bandera para establer Cuales son los gatos busqueda y segui.
        best_cat = min(self.poblation, key=lambda x: x[1])
        best_fitness_history.append(best_cat[1])
        best_cat_solution_history.append(best_cat[0])
        self.distribute_cats()
        stop = False
        while self.efo < self.max_efos:
            for c in self.poblation:
            #Se evalua si el gato está en modo búsqueda o seguimiento
                if c[2]==True:
                    self.tracing_mode(c,best_cat)
                else:
                    self.seeking_mode(c)
            best_cat = min(self.poblation, key=lambda x: x[1])
            if best_cat[1] < best_fitness_history[-1]:
                best_fitness_history.append(best_cat[1])
                best_cat_solution_history.append(best_cat[0])
            else:
                best_fitness_history.append(best_fitness_history[-1])
                best_cat_solution_history.append(best_cat_solution_history[-1])
            self.redistribute_cats()
            stop_optimal = 0
        best_fitness_history = np.array(best_fitness_history)
        self.best.cells = best_fitness_history
        self.best.fitness = best_fitness_history[-1]
        self.efo = 0
        return best_fitness_history, stop

    def redistribute_cats(self):
        for cat in self.poblation:
            cat[2] = not cat[2]
    
    def seeking_mode(self,cat):
        new_cat = self.tweak_cat(cat)
        cat[0] = new_cat[0] #Actualiza las posiciones del gato
        cat[1] = new_cat[1] # Fitness del nuevo gato
     
    def tracing_mode(self,cat,best_cat):
        n_updates = np.random.randint(0, int(len(cat[0])/2))
        self.update_position_cat(n_updates,cat,best_cat) 
        self.generate_permutations(cat)
        fitness = self.problem.evaluate(cat[0])
        self.efo+=1
        cat[1] = fitness
        
    def generate_permutations(self,cat):
        for permutation in cat[3]:
            A = cat[0]
            B = A.copy()
            position1 = A.index(permutation[0])
            position2 = A.index(permutation[1])
            B[position1] = permutation[1]
            B[position2] = permutation[0]
            cat[0]=B

    def update_position_cat(self,n_updates,cat,best_cat):
        #Toma algunas posiciones del mejor gato y se acoplan
        #al gato actual
        A=best_cat[0]
        n_updates = int(self.problem.size*0.25)
        for i in range(n_updates-1):
            B=cat[0]
            ran_pos = np.random.randint(0, len(cat[0])-1)
            value_A = A[ran_pos]
            value_B = B[ran_pos]
            pos_value_B = A.index(value_A)
            C = B.copy()
            C[ran_pos]=value_A
            pos_value_C = B.index(value_A)
            C[pos_value_C] = value_B
            cat[0]=C

    def tweak_cat(self,cat):
        n_cats = self.max_local
        cats_to_evaluate = self.create_cats_to_evaluate(n_cats,cat)
        new_cat = self.select_new_cat(cats_to_evaluate) #Corregir la seleccion
        return new_cat

    def select_new_cat(self,cats_to_evaluate):
        # En esa funcion se elige el gato según su peso de probabilidad
        # Convierte solo los segundos elementos a float64
        weights = 1 / np.array([cat[1] for cat in cats_to_evaluate], dtype=np.float64)
        weights /= weights.sum()

        selected_index = np.random.choice(len(cats_to_evaluate), p=weights)
        selected_dict = cats_to_evaluate[selected_index]

        return selected_dict

    def create_cats_to_evaluate(self,n_cats,cat):
        cats_to_evaluate = []
        if self.spc == True:
            n_cats = n_cats - 1
            cats_to_evaluate.append([cat[0],cat[1],cat[2]])
        for i in range(n_cats):
            cdc = np.random.randint(2, self.problem.size-1)
            srd = np.random.randint(1, self.problem.size-1)
            cat_rotate = self.rotate_solution(cat[0], n=srd)
            new_cat = []
            slices = cat_rotate[:cdc]
            slices.reverse()
            new_cat += slices
            item = len(slices)
            for i in cat_rotate:
                new_cat.append(cat_rotate[item])
                item+=1
                if len(new_cat) == len(cat_rotate):
                    break

            new_cat = self.rotate_solution(new_cat, n=-srd)
            fitness = self.problem.evaluate(new_cat)
            self.efo += 1
            
            cats_to_evaluate.append([new_cat,fitness,False])
        
        for c in cats_to_evaluate:
            pi = self.calculate_pi(cats_to_evaluate,c)
            c += [pi]
        
        return cats_to_evaluate
    
    def calculate_pi(self,cats_to_evaluate,c):
        max_fitness = max(x[1] for x in cats_to_evaluate)
        min_fitness = min(x[1] for x in cats_to_evaluate)
        try:
            pi = (abs(c[1] - max_fitness)) / (max_fitness - min_fitness)
        except ZeroDivisionError:
            pi = 0
        return pi
    
    def rotate_solution(self, cat, n):
        length = len(cat)
        n = n % length  # Manejar casos donde n es mayor que la longitud del vector
        cat_rotate = cat[n:] + cat[:n]

        return cat_rotate

    def create_cats(self, d):
        number_cats = self.size
        initial_cat= list(range(1, d + 1))
        # Generar todas las permutaciones de longitud m
        all_combinations = list(permutations(initial_cat, d))

        # Seleccionar n permutaciones aleatorias sin repetición
        n_combinations = random.sample(all_combinations, number_cats)

        # Convertir las permutaciones en arreglos
        cats = [list(combination) for combination in n_combinations]

        return cats

    def distribute_cats(self):
        cats_tracing  = int(self.mr*self.size)
        index_cats = np.random.choice(np.arange(0, self.size), cats_tracing, replace=False)
        for index in index_cats:
            self.poblation[index][2] = True

    def __str__(self):
        result = "CSO-Gatos_locales:" + str(self.max_local)
        return result