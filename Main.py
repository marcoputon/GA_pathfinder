from networkx import *
from GA import *

def dist(a, b):
	(x1, y1, z1) = a
	(x2, y2, z2) = b
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5



def main():
	G = nx.grid_graph(dim = [20, 20, 20])
	ga = GA([G], 64, 26)
	s = ga.run(0.9, True)

	for i in range(5):
		ga.cross()
		s = ga.run(0.9, False)

	print("\n", s.a, s.b)
	p = s.run_forest_run((0, 0, 0), (19, 19, 19), 8000, G)
	for i in p:
		print(i)

if __name__ == "__main__":
	main()
