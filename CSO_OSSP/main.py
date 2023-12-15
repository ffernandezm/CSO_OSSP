import numpy as np
import pandas as pd
import time
from ossp import ossp
from algorithms.CSO import CSO
from plot_convergence_curve import plot_convergence_curve

# Ruta de paquete de problemas
myPath = "CSO_OSSP/problems/txt/"
max_efos = 50000
repetitions = 10

## Afinamiento de parametros
max_local = 5 #Este parámetro representa la cantidad de gatos que se 
              #copiarán en el modo de búsqueda para así sacar con probabilidades al mejor 
spc = False # Este parámetro si está en True toma al gato original para también evaluarlo
           # lo que significa que el max_local = valor - 1
size = 10 # Cantidad de gatos que se crearán
mr = 0.3333 #Porcentaje de distribución que se hará para los tipos de gatos en seguimiento


## Path de problemas
taill2 = ossp(myPath + "taill2_4x4.txt")
taill3 = ossp(myPath + "taill3_4x4.txt")
taill4 = ossp(myPath + "taill4_4x4.txt")
taill5 = ossp(myPath + "taill1_5x5.txt")
taill6 = ossp(myPath + "taill2_5x5.txt")
taill7 = ossp(myPath + "taill3_5x5.txt")
taill8 = ossp(myPath + "taill1_7x7.txt")
taill9 = ossp(myPath + "taill2_7x7.txt")
taill10 = ossp(myPath + "taill3_7x7.txt")
taill11 = ossp(myPath + "taill1_10x10.txt")
taill12 = ossp(myPath + "taill2_10x10.txt")
taill13 = ossp(myPath + "taill3_10x10.txt")
taill14 = ossp(myPath + "taill1_15x15.txt")
taill15 = ossp(myPath + "taill2_15x15.txt")
taill16 = ossp(myPath + "taill3_15x15.txt")
taill17 = ossp(myPath + "taill1_20x20.txt")
taill18 = ossp(myPath + "taill2_20x20.txt")
taill19 = ossp(myPath + "taill3_20x20.txt")


# Se crea una cadena para iterar con cada problema
problems = [
            taill2,
            taill3,
            taill4,    
            taill5, 
            taill6, 
            taill7, 
            taill8,
            taill9, 
            taill10, 
            taill11,
            taill12, 
            taill13, 
            taill14, 
            taill15,
            taill16, 
            taill17, 
            taill18, 
            taill19, 
            ]

df = pd.DataFrame({'Problem': pd.Series(dtype='str'),
                   'Average Fitness': pd.Series(dtype='float'),
                   'Standard Deviation': pd.Series(dtype='float'),
                   'Best Fitness': pd.Series(dtype='float'),
                   'Worst Fitness': pd.Series(dtype='float'),
                   'Execution Time': pd.Series(dtype='float')})
num_p = 0


name_problem = [
                    "taill2_4x4",
                    "taill3_4x4",
                    "taill4_4x4",
                    "taill1_5x5",
                    "taill2_5x5",
                    "taill3_5x5",
                    "taill1_7x7",
                    "taill2_7x7",
                    "taill3_7x7",
                    "taill1_10x10",
                    "taill2_10x10",
                    "taill3_10x10",
                    "taill1_15x15",
                    "taill2_15x15",
                    "taill3_15x15",
                    "taill1_20x20",
                    "taill2_20x20",
                    "taill3_20x20",
                    ]

for p in problems:
    ## Instanciamos el algoritmo
    cso = CSO(max_efos=max_efos, max_local=max_local, size=size, mr=mr, spc=spc)
    start_timer_p = time.time()
    names_alg = []
    avg_curve_alg = []
    best_avg_fitness_alg = []
    best_std_fitness_alg = []
    best_fitness_along_seeds = []
    worst_fitness_along_seeds = []
    alg_avg_time = []
    best_fitnes = np.zeros(repetitions, float)
    time_by_repetition = np.zeros(repetitions, float)

    for s in range(0, repetitions):
        start_timer = time.time()
        curve_data, stop = cso.evolve(seed=s, problem=p)
        end_timer = time.time()
        avg_curve = np.zeros(len(curve_data), float)
        time_spend = end_timer - start_timer
        avg_curve = avg_curve + curve_data
        time_by_repetition[s] = time_spend
        best_fitnes[s] = cso.best.fitness

    avg_curve = avg_curve / repetitions
    avg_best_fitnes = np.average(best_fitnes)
    std_best_fitnes = np.std(best_fitnes)
    avg_time = np.average(time_by_repetition)
    names_alg.append(str(cso))
    avg_curve_alg.append(avg_curve)
    best_avg_fitness_alg.append(avg_best_fitnes)
    best_std_fitness_alg.append(std_best_fitnes)
    best_fitness_along_seeds.append(min(best_fitnes))
    worst_fitness_along_seeds.append(max(best_fitnes))
    alg_avg_time.append(avg_time)

    plot_convergence_curve.plot_convergence_curve_comparison(
        avg_curve_alg, p, names_alg, name_problem[num_p], max_local)  

    end_timer_p = time.time()
    time_p = end_timer_p - start_timer_p
    print("Tiempo de ejecucion " + str(name_problem[num_p]) + " : "+ str(time_p))
    num_p = num_p + 1
    
    new_row = pd.DataFrame({'Problem': str(p),
                            'Average Fitness': str(best_avg_fitness_alg[0]),
                            'Standard Deviation': str(best_std_fitness_alg[0]),
                            'Best Fitness': str(best_fitness_along_seeds[0]),
                            'Worst Fitness': str(worst_fitness_along_seeds[0]),
                            'Execution Time': str(alg_avg_time[0])}, index=[0])
    
    df = pd.concat([df.loc[:], new_row]).reset_index(drop=True)
    df.to_csv("CSO_OSSP/result/CSO" +
            "-max_local-" + str(max_local) + ".csv", index=False)