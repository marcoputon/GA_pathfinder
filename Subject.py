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
		while step < max_steps or next_a == b:

			#	De acordo com o gen, diz qual o próximo vértice do caminho.
			next_a = self.next_node(next_a, b)

			#	Se ficou parado, termina.
			if next_a is None:
				break

			#	Adiciona o vértice no caminho.
			self.path.append(next_a)

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
		if pos[0] == 0 and pos[1] == 0:		#	XY=
			#	Case 0
			if b[2] - a[2] > 0:	#	Pela direita
				return sub_gen[0]

			#	Case 1
			else:	#	Pela esquerda
				return sub_gen[1]

		elif pos[0] == 0 and pos[2] == 0:	#	XZ=
			#	Case 2
			if b[1] - a[1] > 0:	#	Pela direita
				return sub_gen[2]

			#	Case 3
			else:	#	Pela esquerda
				return sub_gen[3]

		#	YZ=
		elif pos[1] == 0 and pos[2] == 0:
			#	Case 4
			if b[0] - a[0] > 0:	#	Pela direita
				return sub_gen[4]

			#	Case 5
			else:	#	Pela esquerda
				return sub_gen[5]

		#	X=
		elif pos[0] == 0:
			#	Esta mais perto por Y
			if abs(b[1] - a[1]) < abs(b[2] - a[2]):
				#	Pela direita
				if pos[1] > 0:
					#	case 6
					return sub_gen[6]

				#	Pela esquerda
				else:
					#	Case 7
					return sub_gen[7]

			#	Está mais perto por Z
			else:
				#	Pela direita
				if pos[2] > 0:
					#	case 8
					return sub_gen[8]

				#	Pela esquerda
				else:
					#	Case 9
					return sub_gen[9]

		#	Y=
		elif pos[1] == 0:
			#	Está mais perto por X
			if abs(b[0] - a[0]) < abs(b[2] - a[2]):
				#	Pela direita
				if pos[0] > 0:
					#	case 10
					return sub_gen[10]

				#	Pela esquerda
				else:
					#	Case 11
					return sub_gen[11]

			#	Está mais perto por Z
			else:
				#	Pela direita
				if pos[2] > 0:
					#	case 12
					return sub_gen[12]

				#	Pela esquerda
				else:
					#	Case 13
					return sub_gen[13]

		#	Z=
		elif pos[2] == 0:
			#	Esta mais perto por Y
			if abs(b[1] - a[1]) < abs(b[0] - a[0]):
				#	Pela direita
				if pos[1] > 0:
					#	case 14
					return sub_gen[14]

				#	Pela esquerda
				else:
					#	Case 15
					return sub_gen[15]

			#	Está mais perto por X
			else:
				#	Pela direita
				if pos[0] > 0:
					#	case 16
					return sub_gen[16]

				#	Pela esquerda
				else:
					#	Case 17
					return sub_gen[17]

		#	XYZ!=
		else:
			d1 = b[0] - a[0]
			d2 = b[1] - a[1]
			d3 = b[2] - a[2]

			#	d1 é o menor
			if abs(d1) < abs(d2) and abs(d1) < abs(d3):
				#	Case 18
				return sub_gen[18]

			#	d2 é o menor
			elif abs(d2) < abs(d3):
				#	Case 19
				return sub_gen[19]

			#	d3 é o menor
			else:
				#	Case 20
				return sub_gen[20]


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

		#	Vizinhos de do vértice atual
		n = self.G.neighbors(a)

		#
		pos = self.test_pos(a, b)

		wt = self.sub_decide(a, b, pos, self.gen)

		where = self.where_to(a, n, wt)

		return where
