import argparse
from collections import deque, defaultdict

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adj_list = [[] for _ in range(nodes)]
        self.adj_matrix = [[0]*nodes for _ in range(nodes)]
        self.edge_list = []

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_matrix[u][v] = 1
        self.edge_list.append((u, v))

    def print_matrix(self):
        for row in self.adj_matrix:
            print(" ".join(map(str, row)))

    def print_list(self):
        for i, neighbors in enumerate(self.adj_list):
            print(f"{i}: {' '.join(map(str, neighbors))}")

    def print_table(self):
        for u, v in self.edge_list:
            print(f"({u}, {v})")

    def edge_exists(self, u, v):
        return self.adj_matrix[u][v] == 1

    def bfs(self, start):
        visited = [False] * self.nodes
        queue = deque([start])
        visited[start] = True
        order = []
        while queue:
            u = queue.popleft()
            order.append(u)
            for v in self.adj_list[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
        return order

    def dfs_util(self, u, visited, order):
        visited[u] = True
        order.append(u)
        for v in self.adj_list[u]:
            if not visited[v]:
                self.dfs_util(v, visited, order)

    def dfs(self, start):
        visited = [False] * self.nodes
        order = []
        self.dfs_util(start, visited, order)
        return order

    def to_tikz(self):
        tikz_lines = [
            "\\documentclass{article}",
            "\\usepackage{tikz}",
            "\\usetikzlibrary{graphs, graphdrawing, arrows.meta}",
            "\\usegdlibrary{layered} % Automatyczne rozmieszczanie w DAGu",
            "",
            "\\begin{document}",
            "",
            "\\begin{center}",
            "\\begin{tikzpicture}[>=Stealth, every node/.style={circle, draw, minimum size=1cm}]",
            "  \\graph [layered layout, sibling distance=2cm, level distance=2cm] {"
        ]

        for i in range(self.nodes):
            tikz_lines.append(f"    {i};")

        for u, v in self.edge_list:
            tikz_lines.append(f"    {u} -> {v};")

        tikz_lines.append("  };")
        tikz_lines.append("\\end{tikzpicture}")
        tikz_lines.append("\\end{center}")
        tikz_lines.append("")
        tikz_lines.append("\\end{document}")

        with open("graph.tex", "w") as f:
            f.write("\n".join(tikz_lines))

    def kahn_topological_sort(self):
        in_degree = [0] * self.nodes
        for u in range(self.nodes):
            for v in self.adj_list[u]:
                in_degree[v] += 1

        queue = deque([u for u in range(self.nodes) if in_degree[u] == 0])
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u)
            for v in self.adj_list[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(topo_order) != self.nodes:
            print("Graph has at least one cycle")
        else:
            print("Topological order (Kahn):", " ".join(map(str, topo_order)))

    def tarjan_topological_sort(self):
        visited = [0] * self.nodes  # 0 = unvisited, 1 = temporary, 2 = permanent
        topo_order = []

        def visit(u):
            if visited[u] == 2:
                return
            if visited[u] == 1:
                raise ValueError("Graph has at least one cycle")
            visited[u] = 1
            for v in self.adj_list[u]:
                visit(v)
            visited[u] = 2
            topo_order.append(u)

        try:
            for u in range(self.nodes):
                if visited[u] == 0:
                    visit(u)
            topo_order.reverse()
            print("Topological order (Tarjan):", " ".join(map(str, topo_order)))
        except ValueError as e:
            print(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--user-provided', action='store_true')
    args = parser.parse_args()

    if args.generate:
        nodes = int(input("nodes > "))
        saturation = float(input("saturation (0-1) > "))
        from random import sample

        graph = Graph(nodes)
        max_edges = (nodes * (nodes - 1)) // 2
        edge_count = int(saturation * max_edges)
        possible_edges = [(i, j) for i in range(nodes) for j in range(i+1, nodes)]
        selected_edges = sample(possible_edges, edge_count)

        for u, v in selected_edges:
            graph.add_edge(u, v)

    elif args.user_provided:
        nodes = int(input("nodes > "))
        graph = Graph(nodes)
        for u in range(nodes):
            raw = input(f"{u} > ").strip()
            if raw:
                neighbors = list(map(int, raw.split()))
                for v in neighbors:
                    graph.add_edge(u, v)
    else:
        print("Provide either --generate or --user-provided")
        return

    while True:
        action = input("action> ").strip()
        if action == "print":
            rep = input("representation? matrix / list / table > ").strip()
            if rep == "matrix":
                graph.print_matrix()
            elif rep == "list":
                graph.print_list()
            elif rep == "table":
                graph.print_table()
        elif action == "find":
            u = int(input("from> "))
            v = int(input("to> "))
            print("True" if graph.edge_exists(u, v) else "False")
        elif action == "bfs":
            start = int(input("start node> "))
            print("inline:", " ".join(map(str, graph.bfs(start))))
        elif action == "dfs":
            start = int(input("start node> "))
            print("inline:", " ".join(map(str, graph.dfs(start))))
        elif action == "tikz":
            graph.to_tikz()
        elif action == "kahn":
            graph.kahn_topological_sort()
        elif action == "tarjan":
            graph.tarjan_topological_sort()
        elif action == "exit":
            break
        else:
            print("Unknown command")

if __name__ == '__main__':
    main()
