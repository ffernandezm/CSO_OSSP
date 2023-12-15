import numpy as np
from pathlib import Path

# Download problems at https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html
# Download problems at TSPLIb -> http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/

class ossp:
    size: int

    def __init__(self, filename):
        file1 = open(filename, 'r')
        lines = file1.readlines()
        self.file_name = Path(filename).stem
        self.size_jobs = int(lines[0])
        self.size_machines = int(lines[1])
        self.bestFitness = int(lines[5])
        self.size = self.size_jobs * self.size_machines
        self.lookup_table = self.create_matrix_solution(lines)
        self.sequence = None
        self._makespan = None

    def evaluate(self, cells):
        schedule = [[0 for j in self.lookup_table[0]] for i in self.lookup_table]
        self.sequence = cells
        for operation in self.sequence:
            job = self.id_to_job_index(operation)
            machine = self.id_to_machine_index(operation)
            op_cost = self.id_to_lookup(operation)

            column = [row[machine] for row in schedule]
            next_time = max(column)

            if max(schedule[job]) > next_time:
                next_time = max(schedule[job])

            schedule[job][machine]  = next_time + op_cost

        columns = zip(*schedule)
        makespan = 0
        for column in columns:
            cand = max(column)
            if cand > makespan:
                makespan = cand
        return makespan

    def create_matrix_solution(self,lines):
        #Create matrix solution
        matrix_solution = []
        j = 6
        o = 1
        total_operations = self.size_jobs*self.size_machines
        for i in range(total_operations):
            times = lines[j].split()
            machines = lines[j+self.size_jobs].split()
            for m in range(self.size_jobs):
                job = j-5
                col = [o,job,int(machines[m]),float(times[m])]
                matrix_solution.append(col)
                o+=1

            j+=1
            
            if len(matrix_solution) == total_operations:
                break
        
        c_m = self.size_machines
        m_order = []
        if len(matrix_solution):
            for m in matrix_solution:
                if len(m_order) == 0:
                    slices_m = matrix_solution[:c_m]
                    order_slices = sorted(slices_m, key=lambda x: x[2])
                    line = []
                    for s in order_slices:
                        line.append(s[3])
                    m_order.append(line)
                else:
                    slices_m = matrix_solution[c_m:c_m+self.size_machines]
                    order_slices = sorted(slices_m, key=lambda x: x[2])
                    line = []
                    for s in order_slices:
                        line.append(s[3])
                    m_order.append(line)
                    c_m +=self.size_machines
                
                if len(m_order) == self.size_machines:
                    break
        return m_order
    
    
    def id_to_machine_index(self, id):
        transposed_id = id - 1
        return transposed_id % len(self.lookup_table)

    def id_to_job_index(self, id):
        transposed_id = id - 1
        return transposed_id // len(self.lookup_table[0])

    def id_to_lookup(self, id):
        transposed_id = id - 1
        return self.lookup_table[transposed_id//len(self.lookup_table)][transposed_id%len(self.lookup_table[0])]
    
    
    def __str__(self):
        return self.file_name + ' ' + str(self.bestFitness)