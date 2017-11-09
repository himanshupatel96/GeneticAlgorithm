""" Use GA to find the optimal solution for a + 4b + 2c + 3d = 40 """
import random
from itertools import chain
import sys

mrate = 0.12
crate = 0.70

population = []
"""Generating Initial Population Randomly """
if len(sys.argv) == 2:
        pop_size = int(sys.argv[1])
for i in range(1, pop_size):
    x = []
    for j in  range(1, 5):
        x.append(random.randint(0, 40))
    population.append(x)    

"""

#print("initial Population")
#print(population)
#print()
"""


""" Fitness Function """ 
def fitness(chromosome):
    return abs((1*chromosome[0] + 4*chromosome[1] + 2*chromosome[2] + 3*chromosome[3]) - 40)    





"""Crossover Operator """
def crossover(parent1, parent2):
    global population
    point = random.randint(0, len(parent1)-1)
        
    t1 = [parent1[:point], parent2[point:]]
    t2 = [parent1[point:], parent2[:point]]
        
    population.append(list(chain.from_iterable(t1)))
    population.append(list(chain.from_iterable(t2)))
    



""" Mutation Operator """
def mutation():
        global population
        total_gene = len(population) * 4 
        n = total_gene * mrate
        """ How much mutation should be applied """
        n = int(n) 
        while ( n ):
            rindex = random.randint(0, len(population) - 1)
            rval = random.randint(0, 40)
            population[int(rindex/4)][rindex%4] = rval
            n = n - 1



""" Tournament Selection """
def tournamentSelection(p):
    global population
    k = len(population) * 0.90
    """ 70 % individuals are selected randomly """
    k = int(k)
    temp = [0] * k
    for i in range(0, k):
        """ Select k individual candidates to choose from """
        r = random.randint(0, len(population) - 1)
        temp[i] = r
        
    best = None
    for i in range(0, k):
        if best == None or fitness(population[temp[i]]) > fitness(population[best]) :
            best = temp[i]
            
    second = None
    for i in range(0, k):
        A = fitness(population[temp[i]])
        if second != None :
            B = fitness(population[second])
        if  second == None or (A * (1 - A)) > (B * (1 - B)) :
            second = temp[i]

                   
    return [best, second]





""" Elitism --- Removing worst 20 % candidate solutions at each generation """
def removeWorstPerformers():
    global population
    f = []
    for i in range(0, len(population)):
        """Calculate the fitness of each individual """
        f.append((fitness(population[i]), i))

    f.sort()
    #print(f)
    d = len(population) * 0.2
    d = int(d)
    delete = f[len(population) - d:]
    for i in range(0, len(delete)):
        if delete[i][1] >= len(population):
            continue
        population.pop(delete[i][1])


""" Driver Function Which will do everything in this program """                                                          
def calculateFitnessAndOperations():
    global population
    iteration = 1000
    flag = False
    cnt = 1
    while ( iteration ):
        #print()
        #print("Iteration",cnt)
        #print()
        cnt += 1
        f = []
        for i in range(0, len(population)):
            x = fitness(population[i])
            if ( x == 0 ):
                #print("--------------------------------------------------------------------------------")
                #print("Solution ")
                #print(population[i])
                #print("-------------------------------------------------------------------------------")
                flag = True
                break
            f.append(x)
            
        if flag == True :
            break


        total = 0
        for i in range(0 , len(f)):
            f[i] = (1 / (1 + f[i]))
            total = total + f[i]

        #print()    
        #print("Error" , total)
        #print()
        p = []
        
        for i in  range(0, len(f)):
            p.append(f[i] / total)

        
        pair = tournamentSelection(p)
        crossover(population[pair[0]], population[pair[1]])
        
        mutation()
        if len(population) > 5 :
            removeWorstPerformers()

        #print("After Applying Mutation and Crossover Operations")
        #print()
        #print(len(population))
        #print()
        """for i in range(0, len(population)):
            if fitness(population[i]) >= 0 and fitness(population[i]) <= 1:
                #print(population[i])
                break
        """
        iteration -= 1
    print (pop_size, cnt)



        
calculateFitnessAndOperations()




