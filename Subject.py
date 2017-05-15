class Subject:
	def __init__(self, genotype):
		self.gen = genotype			#	Gen do indivíduo
		self.path = []				#	O caminho que o individuo encontrou
		self.a = None				#	Vértice inicial
		self.b = None				#	Vértice final
		self.fitness = 0			#	Fitness
		self.G = None				#	O grafo onde o indivíduo é testado
		self.didIt = False			#	Se chegou até b


	#	Função que roda o indivíduo
	def run_forest_run(self, a, b, max_steps, graph):
		#	Seta valores iniciais
		self.G = graph
		self.a = a
		self.b = b
		self.path.append(a)
		next_a = a

		#	Variável para controlar o numero máximo de passos
		step = 0

		#	Executa enquando não chegar no vértice final ou não atingir o
		#	número máximo de passos.
		while step < max_steps:
			
			#	De acordo com o gen, diz qual o próximo vértice do caminho.
			next_a = self.next_node(next_a, b)

			#	Se ficou parado, termina.
			if next_a is None:
				break

			#	Adiciona o vértice no caminho.
			self.path.append(next_a)

			if next_a == b:
				break

			step += 1

		#	Se terminou e chegou no destino, seta que conseguiu.
		if next_a == b:
			self.didIt = True

	#	Coloca valores nas coordenadas para saber se está a cima, a baixo, ou igual
	#	igual:		0
	#	a cima:		1
	#	a baixo:   -1
	def test_pos(self, a, b):
		r = [0, 0, 0]

		for i in range(3):
			if a[i] == b[i]:
				r[i] = 0
			elif b[i] > a[i]:
				r[i] = 1
			else:
				r[i] = -1

		return tuple(r)


	def sub_decide(self, a, b, pos, sub_gen):
		if pos[0] > 0 and pos[1] > 0 and pos[2] > 0:
			return sub_gen[0]

		if pos[0] > 0 and pos[1] > 0 and pos[2] < 0:
			return sub_gen[1]

		if pos[0] > 0 and pos[1] > 0 and pos[2] == 0:
			return sub_gen[2]

		if pos[0] > 0 and pos[1] < 0 and pos[2] > 0:
			return sub_gen[3]

		if pos[0] > 0 and pos[1] == 0 and pos[2] > 0:
			return sub_gen[4]

		if pos[0] > 0 and pos[1] < 0 and pos[2] < 0:
			return sub_gen[5]

		if pos[0] > 0 and pos[1] < 0 and pos[2] == 0:
			return sub_gen[6]

		if pos[0] > 0 and pos[1] == 0 and pos[2] < 0:
			return sub_gen[7]

		if pos[0] > 0 and pos[1] == 0 and pos[2] == 0:
			return sub_gen[8]

		if pos[0] < 0 and pos[1] > 0 and pos[2] > 0:
			return sub_gen[9]

		if pos[0] == 0 and pos[1] > 0 and pos[2] > 0:
			return sub_gen[10]

		if pos[0] < 0 and pos[1] > 0 and pos[2] < 0:
			return sub_gen[11]

		if pos[0] < 0 and pos[1] > 0 and pos[2] == 0:
			return sub_gen[12]

		if pos[0] == 0 and pos[1] > 0 and pos[2] < 0:
			return sub_gen[13]

		if pos[0] == 0 and pos[1] > 0 and pos[2] == 0:
			return sub_gen[14]

		if pos[0] < 0 and pos[1] < 0 and pos[2] > 0:
			return sub_gen[15]

		if pos[0] < 0 and pos[1] == 0 and pos[2] > 0:
			return sub_gen[16]

		if pos[0] == 0 and pos[1] < 0 and pos[2] > 0:
			return sub_gen[17]

		if pos[0] == 0 and pos[1] == 0 and pos[2] > 0:
			return sub_gen[18]

		if pos[0] < 0 and pos[1] < 0 and pos[2] < 0:
			return sub_gen[19]

		if pos[0] < 0 and pos[1] < 0 and pos[2] == 0:
			return sub_gen[20]

		if pos[0] < 0 and pos[1] == 0 and pos[2] < 0:
			return sub_gen[21]

		if pos[0] < 0 and pos[1] == 0 and pos[2] == 0:
			return sub_gen[22]

		if pos[0] == 0 and pos[1] < 0 and pos[2] < 0:
			return sub_gen[23]

		if pos[0] == 0 and pos[1] < 0 and pos[2] == 0:
			return sub_gen[24]

		if pos[0] == 0 and pos[1] == 0 and pos[2] < 0:
			return sub_gen[25]

		if pos[0] == 0 and pos[1] == 0 and pos[2] == 0:
			return sub_gen[26]


	def where_to(self, a, n, wt):
		for i in n:
			if i[0] - a[0] > 0:		#	Lest
				if wt == 'L':
					return i
			elif i[0] - a[0] < 0:	#	West
				if wt == 'W':
					return i
			elif i[1] - a[1] > 0:	#	North
				if wt == 'N':
					return i
			elif i[1] - a[1] < 0:	#	South
				if wt == 'S':
					return i
			elif i[2] - a[2] > 0:	#	Up
				if wt == 'U':
					return i
			elif i[2] - a[2] < 0:	#	Down
				if wt == 'D':
					return i
		return None


	#	Decide qual é o próximo vértice de acordo com o gen e com o estado atual
	def next_node(self, a, b):
		n = self.G.neighbors(a)
		pos = self.test_pos(a, b)
		wt = self.sub_decide(a, b, pos, self.gen)
		where = self.where_to(a, n, wt)

		return where
