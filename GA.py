from Subject import *
from random import choice


class GA:
	def __init__(self, Graphs, generation_size):
		self.Graphs = Graphs
		self.subjects = []
		self.gen_size = generation_size
		self.best_one = None


	def select_bests(self, n):
		bests = []
		ordered = sorted(self.subjects, key=lambda x: x.fitness, reverse=True)
		for i in ordered:
			if n < 1:
				break
			bests.append(i)
			n -= 1
		return bests


	def print_subjects(self):
		for i in self.subjects:
			print("%s | %f | %s" %(i.gen, i.fitness, i.didIt))
			print(i.path)

	def manhattan(self, a, b):
		(x1, y1, z1) = a
		(x2, y2, z2) = b
		return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


	def fitness(self, subject):
		#	Distância percorrida + distância de manhattan
		path_dist = 0

		path_size = len(subject.path)
		c1 = 0
		c2 = c1 + 1
		while c2 < path_size:
			path_dist += self.manhattan(subject.path[c1], subject.path[c2])
			c1 += 1
			c2 = c1 + 1

		best_dist = self.manhattan(subject.a, subject.b)

		#	Se não chegou no destino, adiciona a penalidade
		#	Soma a distancia do último nodo do caminho até o destino com a menor
		#	distância da origem até o destino (origem -> destino -> onde parou).
		path_dist += 2 * self.manhattan(subject.path[-1], subject.b)

		subject.fitness = (best_dist / path_dist)



	def generate_subjects(self):
		self.subjects = []

		genotype_iter = range(105)
		generation_iter = range(self.gen_size)

		for i in generation_iter:
			new_gen = ""
			for i in genotype_iter:
				new_gen += choice(['N', 'S', 'L', 'E', 'U', 'D'])
			self.subjects.append(Subject(new_gen))

	def run_subjects(self):
		for i in self.subjects:
			sg = choice(self.Graphs)
			i.run_forest_run(choice(sg.nodes()), choice(sg.nodes()), sg.size(), sg)
			self.fitness(i)

	def run(self, stop):
		self.generate_subjects()
		self.best_one = self.subjects[0]
			while self.best_one.fitness < stop:
				pass
