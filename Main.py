from networkx import *
from GA import *



def dist(a, b):
	(x1, y1, z1) = a
	(x2, y2, z2) = b
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5


def main():
	G = nx.grid_graph(dim = [10, 10, 5])
	ga = GA([G], 500, 27)
	ga.generate_subjects()
	ga.run(0.97, 200, 200)

	'''
	i = Subject(ga.best_one.gen)
	i.run_forest_run((0, 0, 0), (5, 7, 3), 449, G)
	print("\n", i.a, i.b, "\n", i.path)

	i.run_forest_run((0, 7, 0), (5, 7, 3), 449, G)
	print("\n", i.a, i.b, "\n", i.path)

	i.run_forest_run((0, 9, 0), (5, 7, 3), 449, G)
	print("\n", i.a, i.b, "\n", i.path)

	i.run_forest_run((9, 9, 3), (2, 1, 2), 449, G)
	print("\n", i.a, i.b, "\n", i.path)
	'''

if __name__ == "__main__":
	main()
