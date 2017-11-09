from __future__ import division
import sys
import random
import time

weights = [70,60,50,33,33,33,11,7,3]
gains = [1,2,3,2,3,4,1,1,1]
W = 200

mut_prob = 0.01
pop_size = int(sys.argv[1])

def fitness(member):
	we = 0
	ga = 0
	for i in range(0,len(member)):
		if(member[i]=='1'):
			we += weights[i]
			ga += gains[i]
	if(we<=W):
		return ga
	return 0

def new_population():
	new_pop = []
	for no in range(0,pop_size):
		temp = ""
		for i in range(0,len(gains)):
			temp += str(random.randint(0,1))
		new_pop.append(temp)
	return new_pop

def roulette_wheel(prob):
	r = random.uniform(0,1)
	for i in range(0,len(prob)):
		if(r<=prob[i]):
			return i
	return len(prob)-1

def crossover(par1,par2):
	child = []
	for i in range(0,len(par1)//2):
		child.append(par1[i])
	for i in range(len(par2)//2,len(par2)):
		child.append(par2[i])
		
	"""for i in range(0,len(par1)):
		if(i%2==0):
			child.append(par1[i])
		else:
			child.append(par2[i])"""
	return child

def mutate(member):
	child = ""
	for i in range(0,len(member)):
		r = random.uniform(0,1)
		if(r<=mut_prob):
			child += str(random.randint(0,1))
		else:
			child += str(member[i])
	return child
	
def solve():
	new_pop = new_population()
	iteration = 0
	while(True):
		print("Generation#:",iteration)
		iteration = iteration + 1
		pop = new_pop
		new_pop = []
		fit = []
		prob = []
		prev = 0.0
		for i in range(0,len(pop)):
			fit.append(fitness(pop[i]))
		
		Sum = sum(fit)
		
		for i in range(0,len(fit)):
			prev+=fit[i]/Sum
			prob.append(prev)
			
		for i in range(0,len(pop)):
			parent1 = roulette_wheel(prob)
			parent2 = roulette_wheel(prob)
			child = crossover(pop[parent1],pop[parent2])
			child = mutate(child)
			new_pop.append(child)
			print( child,fitness(child))
		D = {}
		mx = 0
		for i in range(0,len(new_pop)):
			val = fitness(new_pop[i]) 
			#print val
			if val in D:
				D[val] = D[val] + 1
				#print "at",val,D[val]
				mx = max(D[val],mx)
			else:
				#print "at",val,1
				D[val] = 1
		#print "Hiiiiiiiii",mx
		#time.sleep(1)
		for key in D:
			if( (D[key]/len(new_pop))*100 >= 96):
				for i in range(0,len(new_pop)):
					if(fitness(new_pop[i])==key): 
						return new_pop[i]
		#time.sleep(1)
		
if __name__=='__main__':
	start = time.time()
	solution = solve()
	end = time.time()
	print (solution,fitness(solution),end-start)

