import sys
import copy
import math
import random
class Board:
	def __init__(self,board_size,goal):
		self.board_size = board_size
		self.goal = goal
		self.fitness=0
		self.queens=list(range(self.board_size))
		self.switch(self.board_size/2)
	def __del__(self):
		pass
	def switch(self,count):
		count = int(count)
		for i in range(count):
			j = random.randint(0,self.board_size-1)
			k = random.randint(0,self.board_size-1)
			self.queens[j],self.queens[k]=self.queens[k],self.queens[j]
		self.compute_fitness()
	def regenerate(self,prob):
		#self.switch(2)
		if random.random() < prob:
			if prob==0.50:
				self.switch(2)
			else:
				self.switch(1)
	def compute_fitness(self):
		self.fitness = self.goal
		for i in range(self.board_size):
			for j in range(i+1, self.board_size):
				if math.fabs(self.queens[i] - self.queens[j]) == j-i:
					self.fitness-=1
	def print_board(self):
		for row in range(self.board_size):
			print("",end="|")
			
			queen = self.queens.index(row)
			for col in range(self.board_size):
				if col == queen:
					print("Q",end="|")
				else:
					print("_",end="|")
			print("")
	
class GaQueens:
	def __init__(self,board_size,population_size,generation_size):
		self.board_size = board_size
		self.population_size = population_size
		self.generation_size = generation_size
		self.generation_count = 0
		self.goal = int((self.board_size * (self.board_size-1))/2)
		self.population = []
		self.first_generation()
		while True:
			if self.is_goal_reached() == True:
				break
			if -1 < self.generation_size <= self.generation_count:
				break
			self.next_generation()
		#print("===================================================================")
		if -1 < self.generation_size <= self.generation_count:
			print("Couldn't find result in %d Generations" % self.generation_count)
		elif self.is_goal_reached():
			#print("Correct answer found in %d Genrations" % self.generation_count)
			print (self.board_size, self.population_size, self.generation_count)			
			for population in self.population:
				if population.fitness == self.goal:
					#print(population.queens)
					#population.print_board()
					break
	def __del__(self):
		pass
	def is_goal_reached(self):
		for population in self.population:
			if population.fitness == self.goal:
				return True
		return False
	def random_selection(self):
		population_list = []
		for i in range(len(self.population)):
			population_list.append((i,self.population[i].fitness))
		population_list.sort(key=lambda pop_item:pop_item[1], reverse=True)
		return population_list[:int(len(population_list)/3)]
	def first_generation(self):
		for i in range(self.population_size):
			self.population.append(Board(self.board_size, self.goal))
		self.print_population()
	def cxPartialyMatched(self,ind1, ind2):
		size = min(len(ind1), len(ind2))
		p1, p2 = [0]*size, [0]*size

    # Initialize the position of each indices in the individuals
		for i in range(size):
			p1[ind1[i]] = i
			p2[ind2[i]] = i
    # Choose crossover points
		cxpoint1 = random.randint(0, size)
		cxpoint2 = random.randint(0, size - 1)
		if cxpoint2 >= cxpoint1:
			cxpoint2 += 1
		else: # Swap the two cx points
			cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    
    # Apply crossover between cx points
		for i in range(cxpoint1, cxpoint2):
        # Keep track of the selected values
			temp1 = ind1[i]
			temp2 = ind2[i]
        # Swap the matched value
			ind1[i], ind1[p1[temp2]] = temp2, temp1
			ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
			p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
			p2[temp1], p2[temp2] = p2[temp2], p2[temp1]
		return ind1, ind2
	def onePointX(self,child1,child2):
		crossover_point = random.randint(2,self.board_size-2)
		var = crossover_point
		while len(child1) < self.board_size:
			if parent2.queens[var % self.board_size] not in child1:
				child1.append(parent2.queens[var % self.board_size])
			var +=1
		var = crossover_point
		while len(child2) < self.board_size:
			if parent1.queens[var % self.board_size] not in child2:
				child2.append(parent1.queens[var % self.board_size])
			var +=1
		return child1,child2
	def next_generation(self):
		self.generation_count+=1
		selections = self.random_selection()
		new_population = []
		select_list = []
		for select in selections:
			if len(select)==2:
				#new_population.append(self.population[select[0]])
				select_list.append(select[0])
		maxFitness = self.population[select_list[0]].fitness
		goal = self.goal
		while len(new_population) < self.population_size:
			#sel = random.sample(select_list,2)
			'''#sel2 = random.randint(0,self.population_size-1)
			#print(sel[0],sel[1])
			parent1 = self.population[sel[0]]
			parent2 = self.population[sel[1]]
			child1=[]
			child2=[]
			for i in range(0,crossover_point):
				child1.append(parent1.queens[i])
				child2.append(parent2.queens[i])
			self.onePointX(p,child2)
			self.cxPartialyMatched(child1,child2)
			parent1.queens = child1
			parent2.queens = child2 
			new_population.append(parent1)
			new_population.append(parent2)'''
			sel = random.choice(selections)[0]
			new_population.append(copy.deepcopy(self.population[sel]))
		i=0
		while i<len(new_population):
			sel=random.sample(range(0,self.population_size),2)
			parent1=new_population[sel[0]]
			parent2=new_population[sel[1]]
			if maxFitness < 0.97*goal:
				#self.cxPartialyMatched(parent1.queens,parent2.queens)
				self.onePointX(parent1.queens,parent2.queens)
			i+=1
		self.population = new_population
		for population in self.population:
			if maxFitness < 0.97*goal:
				population.regenerate(0.25)
			else:
				population.regenerate(0.50)
		self.print_population(selections)
	def print_population(self,selections=None):
		#print("Population #%d " % self.generation_count)
		if selections == None:
			selections = []
		#print("		Using:%s" % str([sel[0] for sel in selections]))
		count=0
		for population in self.population:
			#print("%8d : (%d) %s" % (count,population.fitness,str(population.queens)))
			count+=1
if __name__ == '__main__':
    # default values
    # size of board also shows how many queens are in game
    board_size = 8
    # size of each generation
    population_size = 10
    # how many generations should I check
    # -1 for no generation limit. (search to find a result)
    generation_size = -1

    # if there is arguments use them instead of default values
    if len(sys.argv) == 4:
        board_size = int(sys.argv[1])
        population_size = int(sys.argv[2])
        generation_size = int(sys.argv[3])

    # print some information about current quest!
    #print ("Starting:")
    #print ("    board size      : ", board_size)
    #print ("    population size : ", population_size)
    #print ("    generation size : ", generation_size)
    #print (board_size, population_size, generation_size)
    #print ("==================================================================")

    # Run!
    GaQueens(board_size, population_size, generation_size)
