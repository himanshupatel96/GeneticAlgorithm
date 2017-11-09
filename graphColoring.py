import sys
import copy
import math
import random
class Vertices:
	def __init__(self,no_of_vertices,adjacency_list,goal,max_colors):
		self.no_of_vertices = no_of_vertices
		self.goal = goal
		self.adjacency_list=adjacency_list
		self.fitness=0
		self.max_colors=max_colors
		self.pM=1.1/float(self.no_of_vertices)
		self.chromosome=[random.randint(0,self.max_colors-1) for _ in range(self.no_of_vertices)]
		self.switch(self.no_of_vertices/2)
	def __del__(self):
		pass
	def switch(self,count):
		count = int(count)
		for i in range(count):
			j = random.randint(0,self.no_of_vertices-1)
			k = random.randint(0,self.no_of_vertices-1)
			self.chromosome[j],self.chromosome[k]=self.chromosome[k],self.chromosome[j]
		self.compute_fitness()
	def mutation(self,prob):
		if random.random() <= self.pM:
			ind=random.randint(0,self.no_of_vertices-1)
			self.chromosome[ind]=random.randint(0,self.max_colors-1)
		self.compute_fitness()
	def compute_fitness(self):
		self.fitness = self.goal
		for ind, node in enumerate(self.adjacency_list):
			#print(ind," ",node)
			for vertex in node:
				if self.chromosome[int(vertex)] == self.chromosome[int(ind)]:
					self.fitness-=1
class GAgraphColoring:
	def __init__(self,no_of_vertices,no_of_edges,adjacency_list,population_size,generation_size):
		self.no_of_vertices = no_of_vertices
		self.no_of_edges=no_of_edges
		self.adjacency_list=adjacency_list
		self.population_size = population_size
		self.generation_size = generation_size
		self.generation_count = 0
		self.pM=1.1/float(self.no_of_vertices)
		self.goal = int(2*self.no_of_edges)
		max=0
		for node in adjacency_list:
			if max<len(node):
				max=len(node)
		self.max_colors=max
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
			print (self.population_size, self.generation_count)
			for population in self.population:
				if population.fitness == self.goal:
					#print("{{",population.fitness,"}}  ",population.chromosome)
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
			self.population.append(Vertices(self.no_of_vertices,self.adjacency_list,self.goal,self.max_colors))
		#self.print_population()
	def unifXover(self,parentA, parentB):
		childA = parentA[:]
		childB = parentB[:]
		for i in range(self.no_of_vertices):
			if 0.5 > random.random():
				childA[i] = parentB[i]
				childB[i] = parentA[i]
		return [childA, childB]
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
			sel = random.choice(selections)[0]
			new_population.append(copy.deepcopy(self.population[sel]))
		i=0
		while i<len(new_population):
			sel=random.sample(range(0,self.population_size),2)
			parent1=new_population[sel[0]]
			parent2=new_population[sel[1]]
			if maxFitness < 0.98*goal:
				childAB=self.unifXover(parent1.chromosome,parent2.chromosome)
				parent1.chromosome=childAB[0]
				parent2.chromosome=childAB[1]
			i+=1
		self.population = new_population
		for population in self.population:
			if maxFitness < 0.98*goal:
				population.mutation(self.pM)
			else:
				for _ in range(int(self.no_of_vertices/5)):
					population.mutation(0.50)
				
		#self.print_population(selections)
	def print_population(self,selections=None):
		print("Population #%d " % self.generation_count)
		if selections == None:
			selections = []
		print("		Using:%s" % str([sel[0] for sel in selections]))
		count=0
		for population in self.population:
			print("%8d : (%d) %s" % (count,population.fitness,str(population.chromosome)))
			count+=1
if __name__ == '__main__':
	knapfile = 'input_file1.txt'
	with open(knapfile, 'rU') as kfile:
		lines = kfile.readlines()
	edges=[]
	for line in lines:
		edge=line.split()
		edges.append([edge[0],edge[1]])
	no_of_vertices = int(edges[0][0]) 
	no_of_edges = int(edges[0][1]) 
	adjacency_list=[[] for _ in range(no_of_vertices)]
	for i in range(1,no_of_edges+1):
		adjacency_list[int(edges[i][0])].append(edges[i][1])
		adjacency_list[int(edges[i][1])].append(edges[i][0])
	#print(adjacency_list)
	population_size=8
	generation_size=10
	if len(sys.argv) == 3:
		population_size = int(sys.argv[1])
		generation_size = int(sys.argv[2])
    # print some information about current quest!
	#print ("Starting:")
	#print ("    No of Vertices  : ", no_of_vertices)
	#print ("    population size : ", population_size)
	#print ("    generation size : ", generation_size)
	#print ("==================================================================")
    # Run!
	GAgraphColoring(no_of_vertices,no_of_edges,adjacency_list, population_size, generation_size)
