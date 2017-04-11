from Subject import *
from random import choice, uniform


class GA:
	def __init__(self, Graphs, generation_size,  genotype_size):
		self.Graphs = Graphs
		self.subjects = []
		self.gen_size = generation_size
		self.genotype_size = genotype_size
		self.best_one = None
		self.Xfitness = 0
		self.gen_n = 0


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
		#print(path_dist, self.manhattan(subject.path[-1], subject.b), subject.a, subject.b)
		path_dist += 2 * self.manhattan(subject.path[-1], subject.b)

		subject.fitness = (best_dist / path_dist)



	def generate_subjects(self):
		self.subjects = []

		genotype_iter = range(self.genotype_size)
		generation_iter = range(self.gen_size)

		for i in generation_iter:
			new_gen = ""
			for i in genotype_iter:
				new_gen += choice(['N', 'S', 'L', 'W', 'U', 'D'])
			self.subjects.append(Subject(new_gen))


	def cross(self):
		self.new_subjects = []
		ordered_subj = sorted(self.subjects, key=lambda x: x.fitness, reverse=True)

		sum_fit = 0
		for i in ordered_subj:
			sum_fit += i.fitness

		for i in range(int(self.gen_size / 2)):
			a = uniform(0, sum_fit)

			inter = 0
			for i in ordered_subj:
				if a >= inter and a < inter + i.fitness:
					a = i
					break
				inter += i.fitness

			flag = True
			while flag:
				inter = 0
				b = uniform(0, sum_fit)
				for i in ordered_subj:
					if b >= inter and b < inter + i.fitness:
						if i.gen != a.gen:
							b = i
							flag = False
							break
					inter += i.fitness

			#	Aqui já tem sorteado dois indivíduos, em a e b
			#	Agora tem que sortear os atributos que vão ser misturados
			#	Somar as fitness e sortear de acordo com o quao bom são os pais
			#	wtc é a
			soma = a.fitness + b.fitness
			prob_a = a.fitness / soma
			new_a = ""
			new_b = ""

			for i in range(len(a.gen)):
				s = uniform(0, soma)
				if s < prob_a:
					new_a += a.gen[i]
					new_b += b.gen[i]
				else:
					new_a += b.gen[i]
					new_b += a.gen[i]
			self.new_subjects.append(Subject(new_a))
			self.new_subjects.append(Subject(new_b))

			#print(new_a)
			#print(new_b)

		self.subjects = self.new_subjects



	def run_subjects(self):
		self.Xfitness = 0
		summ = 0
		for i in self.subjects:
			sg = choice(self.Graphs)
			a = choice(sg.nodes())
			b = choice(sg.nodes())

			while b == a:
				b = choice(sg.nodes())

			i.run_forest_run(a, b, sg.size(), sg)
			self.fitness(i)
			if i.fitness > self.best_one.fitness:
				self.best_one = i
			summ += i.fitness
			#print(i.fitness)
		self.Xfitness = summ / self.gen_size


	def run(self, stop, more):
		self.generate_subjects()
		self.best_one = self.subjects[0]
		n = 1

		while self.best_one.fitness < stop:
			self.run_subjects()
			print("Generation: %d | Avarage fitness: %f" %(n, self.Xfitness))
			self.cross()
			n += 1
		print("Someone did it")
		for i in range(more):
			self.run_subjects()
			print("Generation: %d | Avarage fitness: %f" %(n, self.Xfitness))
			self.cross()
			n += 1

		print(self.best_one.fitness)
		print(self.best_one.a, self.best_one.b)
		print(self.best_one.path)
