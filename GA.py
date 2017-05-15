from Subject import *
from random import choice, uniform
from math import sqrt


class GA:
	def __init__(self, Graphs, generation_size,  genotype_size):
		self.Graphs = Graphs
		self.subjects = []
		self.gen_size = generation_size
		self.genotype_size = genotype_size
		self.best_one = None
		self.Xfitness = 0
		self.gen_n = 0

	#	Não está sendo usado
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
		'''
		#	Distância percorrida + distância de manhattan
		path_dist = 0
		path_size = len(subject.path)

		c1 = 0
		c2 = c1 + 1
		while c2 < path_size:
			path_dist += self.manhattan(subject.path[c1], subject.path[c2])
			c1 += 1
			c2 = c1 + 1

		subject.fitness = (1 - ((path_dist + self.max_dist(subject.path[-1], subject.b)) / (self.max_dist((0, 0, 0), (9,  9,  4)))))
		'''


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
		path_dist += self.manhattan(subject.path[-1], subject.b) ** 2

		subject.fitness = (best_dist / path_dist)









	def max_dist(self, a, b):
		return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1) * (abs(b[2] - a[2]) + 1) - 1



	def generate_subjects(self):
		self.subjects = []

		#	O tamanho da pupolação e do genótipo é setado na instanciação do GA
		genotype_iter = range(self.genotype_size)
		generation_iter = range(self.gen_size)

		#	Cria indivíduos com genótipos aleatórios
		for i in generation_iter:

			new_gen = ""
			for i in genotype_iter:

				#	Sorteia um dos valores para colocar no índice
				new_gen += choice(['N', 'S', 'L', 'W', 'U', 'D'])

			self.subjects.append(Subject(new_gen))



	def cross(self):
		#	Nova lista de indivíduos
		self.new_subjects = []

		#	Lista de indivíduos ordenada por fitness na maior para a menor
		ordered_subj = sorted(self.subjects, key=lambda x: x.fitness, reverse=True)

		#	Soma das fitness
		sum_fit = 0
		for i in ordered_subj:
			sum_fit += i.fitness

		#	Aqui serão gerados os novos indivíduos. Como gera 2 indivíduos por
		#	vez, percorre a metade do tamanho da geração
		for i in range(int(self.gen_size / 2)):

			#	sorteia um float entre 0 e a soma das fitness
			a = uniform(0, sum_fit)

			#	Busca o indivíduo sorteado
			inter = 0
			for i in ordered_subj:
				if a >= inter and a < inter + i.fitness:
					a = i
					break
				inter += i.fitness
			#	Nesse ponto, a é o indivíduo sorteado

			#	Faz o mesmo para o segundo indivíduo que será sorteado. Caso
			#	seja o mesmo indivíduo, sorteia outro
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
			soma = a.fitness + b.fitness
			prob_a = a.fitness / soma
			new_a = ""
			new_b = ""

			#	Mistura os gens
			for i in range(len(a.gen)):
				#	Sorteia um numero para decidir se mistura o índice ou não
				s = uniform(0, soma)

				#	Aqui não mistura
				if s < prob_a:
					new_a += a.gen[i]
					new_b += b.gen[i]

				#	Aqui mistura
				else:
					new_a += b.gen[i]
					new_b += a.gen[i]

			#	Adiciona os novos indivíduos na lista nova
			self.new_subjects.append(Subject(new_a))
			self.new_subjects.append(Subject(new_b))

		#	Troca a lista velha de indivíduos pela nova
		self.subjects = self.new_subjects


	#	Função para rodar todos os indivíduos
	def run_subjects(self):

		#	Coloca a média e a soma das fitness com valor 0
		self.Xfitness = 0
		summ = 0

		for i in self.subjects:
			#	Sorteia um grafo e dois nodos
			sg = choice(self.Graphs)
			a = choice(sg.nodes())
			b = choice(sg.nodes())

			#	Se os dois nodos forem iguais, sorteia um novo
			while b == a:
				b = choice(sg.nodes())

			#	Roda o indivíduo
			i.run_forest_run(a, b, len(sg.nodes()) - 1, sg)
			#i.run_forest_run((0, 0, 0), (9, 9, 4), len(sg.nodes()) - 1, sg)

			#	Calcula a fitness
			self.fitness(i)

			#	Guarda a maior fitnes
			if i.fitness > self.best_one.fitness:
				self.best_one = i

			#	Soma as fitness
			summ += i.fitness

			#print("gen: %s | fitness: %f" %(i.gen, i.fitness))

		#	Calcula a média das fitness
		self.Xfitness = summ / self.gen_size


	#	Executar o algoritmo genético
	def run(self, stop, more,  only):

		#	Gera a primeira geração de indivíduos
		self.generate_subjects()

		#	O melhor é o primeiro para ter um valor, depois os indivíduos são
		#	executados e o melhor é atualizado.
		self.best_one = self.subjects[0]

		n = 1

		#	Executa até o critério de parada
		while self.best_one.fitness < stop:

			#	Executa os indivíduos
			self.run_subjects()
			print("Generation: %d | Avarage fitness: %f | Best fitness: %f" %(n, self.Xfitness, self.best_one.fitness))

			#	Faz o cruzamento
			self.cross()
			if only and n >= only:
				break
			n += 1


		#	Executa as iterações a mais
		for i in range(more):
			self.run_subjects()
			print("Generation: %d | Avarage fitness: %f" %(n, self.Xfitness))
			self.cross()
			n += 1

		#	Mostra os resultados
		print("best one's fitness:", self.best_one.fitness)
		print("best one's gen:", self.best_one.gen)
		print("Path:")
		print(self.best_one.a, self.best_one.b)
		print(self.best_one.path)
