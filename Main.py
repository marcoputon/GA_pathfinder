from networkx import *
from GA import *

def dist(a, b):
	(x1, y1, z1) = a
	(x2, y2, z2) = b
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5



def main():
	G = nx.grid_graph(dim = [10, 10, 10])
	ga = GA([G], 64)
	ga.generate_subjects()
	ga.run_subjects()
	ga.print_subjects()
	for i in ga.subjects[0].path:
		print(i)



if __name__ == "__main__":
	main()
