import argparse
from collections import deque
import math

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adj_list = [[] for _ in range(nodes)]
        self.adj_matrix = [[0] * nodes for _ in range(nodes)]
        self.edge_list = []

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_matrix[u][v] = 1
        #self.adj_matrix[v][u] = -1
        self.edge_list.append((u, v))

    def print_matrix(self,n):
        print("  |", end="")
        for i in range(1,n+1):
            print(i, end=" ")
        print("",end=" \n")
        i=1
        for row in self.adj_matrix:
            print(i,end=" |")
            print(" ".join(map(str, row)),end="\n")
            i+=1

    def print_list(self):
        for i, neighbors in enumerate(self.adj_list):
            print(f"{i+1}: {' '.join(map(str, neighbors))}")

    def print_table(self):
        for u, v in self.edge_list:
            print(f"({u+1}, {v+1})")

    def edge_exists(self, u, v):
        return self.adj_matrix[u][v] == 1

    def start(self):
        if self.nodes == 0:
            raise RuntimeError("Cannot perform BFS on empty graph")
        stopien = [0] * self.nodes
        for u in range(self.nodes):
            for v in self.adj_list[u]:
                stopien[v] += 1
        liczby = [i for i in range(self.nodes) if stopien[i] == 0]
        return liczby

    def bfs(self):
        poczatek=min(self.start())
        wizyty = [False] * self.nodes
        queue = deque([poczatek])
        wizyty[poczatek] = True
        order = []

        while queue:
            u = queue.popleft()
            order.append(u+1)
            for v in self.adj_list[u]:
                if not wizyty[v]:
                    wizyty[v] = True
                    queue.append(v)
        return order

    def dfs_pomoc(self, u, wizyty, order):
        wizyty[u] = True
        order.append(u+1)
        for v in self.adj_list[u]:
            if not wizyty[v]:
                self.dfs_pomoc(v, wizyty, order)

    def dfs(self):
        poczatek=min(self.start())
        wizyty = [False] * self.nodes
        order = []
        self.dfs_pomoc(poczatek, wizyty, order)
        return order

    def to_tikz(self):
        print("Podaj nazwę pliku:")
        filename=input()
        tikz_code = """\\documentclass[border=5pt]{standalone}
    \\usepackage{tikz}
    \\usetikzlibrary{arrows.meta}
    \\begin{document}
    \\begin{tikzpicture}[->, >=Stealth, auto, node distance=2.5cm, thick,
        main node/.style={circle, draw, font=\\sffamily\\Large\\bfseries}]

    """

        tikz_code += "    % Wierzchołki\n"
        for i in range(self.nodes):
            angle = 2 * math.pi * i / self.nodes
            x = 5 * math.cos(angle)
            y = 5 * math.sin(angle)
            tikz_code += f"    \\node[main node] ({i + 1}) at ({x:.2f},{y:.2f}) {{{i + 1}}};\n"

        tikz_code += "\n    % Krawędzie\n"
        for u, v in self.edge_list:
            bend = "" if (v, u) not in self.edge_list else "bend left=15"
            tikz_code += f"    \\path ({u + 1}) edge[{bend}] ({v + 1});\n"

        tikz_code += """\\end{tikzpicture}
    \\end{document}"""

        with open(filename, 'w') as f:
            f.write(tikz_code)

        print(f"Graf został wyeksportowany do {filename}")

    def kahn_sort(self):
        stopien = [0] * self.nodes
        for u in range(self.nodes):
            for v in self.adj_list[u]:
                stopien[v] += 1

        queue = deque(self.start())
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u+1)
            for v in self.adj_list[u]:
                stopien[v] -= 1
                if stopien[v] == 0:
                    queue.append(v)

        if len(topo_order) != self.nodes:
            print("Graf ma co najmniej jeden cykl")
        else:
            print("Sortowanie topologiczne (Kahn):", " ".join(map(str, topo_order)))

    def tarjan_sort(self):
        marks = [0] * self.nodes
        result = []
        cykle = False

        def visit(n):
            nonlocal cykle
            if marks[n] == 2:
                return
            if marks[n] == 1:
                cykle = True
                return
            marks[n] = 1
            for neighbor in self.adj_list[n]:
                visit(neighbor)
                if cykle:
                    return
            marks[n] = 2
            result.append(n)

        for node in range(self.nodes):
            if marks[node] == 0:
                visit(node)
                if cykle:
                    break

        if cykle:
            print("Graf ma co najmniej jeden cykl")
        else:
            result.reverse()
            print("Sortowanie topologiczne (Tarjan):", " ".join(str(x + 1) for x in result))
def get_help():
    print("\nOperacje na grafach:")
    print("  Print - wypisanie grafu w wybranej reprezentacji")
    print("  Find - szukanie krawędzi")
    print("  BFS - przechodzenie wszerz grafu")
    print("  DFS - przechodzenie w głąb grafu")
    print("  Export - generowanie kodu do latex")
    print("  Kahn - sortowanie topologiczne gradu algorytmem Kahna")
    print("  Tarjan - sortowanie topologiczne gradu algorytmem Trajana")
    print("  Help - opis menu")
    print("  Exit - wyjście z propgramu\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--user-provided', action='store_true')
    args = parser.parse_args()

    if args.generate:
        nodes = int(input("nodes > "))
        saturation = float(input("saturation (0-100) > "))
        from random import sample

        graph = Graph(nodes)
        max_edge = (nodes * (nodes - 1)) // 2
        count_edge = int((saturation * max_edge)/100)
        possi_edge = [(i, j) for i in range(nodes) for j in range(i + 1, nodes)]
        sel_edge = sample(possi_edge, count_edge)

        for u, v in sel_edge:
            graph.add_edge(u, v)

    elif args.user_provided:
        nodes = int(input("nodes > "))
        graph = Graph(nodes)
        for u in range(1,nodes+1):
            raw = input(f"{u} > ").strip()
            if raw:
                neighbors = list(map(int, raw.split()))
                for v in neighbors:
                    graph.add_edge(u-1, v-1)
    else:
        print("Provide either --generate or --user-provided")
        return

    print("\nOperacje na grafach:")
    print("  Print")
    print("  Find")
    print("  BFS")
    print("  DFS")
    print("  Export")
    print("  Kahn")
    print("  Tarjan")
    print("  Help")
    print("  Exit\n")

    while True:
        try:
            action = input("action> ").strip().lower()

            match action:
                case "print":
                    rep = input("representation? matrix/list/table > ").strip().lower()
                    match rep:
                        case "matrix":
                            graph.print_matrix(nodes)
                        case "list":
                            graph.print_list()
                        case "table":
                            graph.print_table()
                        case _:
                            print("Invalid representation type")

                case "find":
                    w = int(input("from> "))
                    v = int(input("to> "))
                    print("True" if graph.edge_exists(w, v) else "False")

                case "bfs":
                    print("inline:", " ".join(map(str, graph.bfs())))

                case "dfs":
                    print("inline:", " ".join(map(str, graph.dfs())))
                case "export":
                    graph.to_tikz()
                case "help":
                    print(get_help())
                case "kahn":
                    graph.kahn_sort()
                case "tarjan":
                    graph.tarjan_sort()
                case "exit":
                    break
                case _:
                    print("Nie ma takiej opcji!")
        except ValueError:
            print("Invalid input - please enter numbers where required")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()