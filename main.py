import argparse
from collections import deque
from random import sample


class Graph:
    def __init__(self, nodes, directed=True):
        """
        Initialize a graph with a given number of nodes.

        Args:
            nodes (int): Number of nodes in the graph
            directed (bool): Whether the graph is directed (default: True)
        """
        if nodes <= 0:
            raise ValueError("Number of nodes must be positive")

        self.nodes = nodes
        self.directed = directed
        self.adj_list = [[] for _ in range(nodes)]
        self.adj_matrix = [[0] * nodes for _ in range(nodes)]
        self.edge_list = []

    def add_edge(self, u, v):
        """
        Add an edge between nodes u and v.

        Args:
            u (int): Source node
            v (int): Destination node
        """
        if u < 0 or u >= self.nodes or v < 0 or v >= self.nodes:
            raise ValueError("Node index out of range")
        if u == v:
            raise ValueError("Self-loops are not allowed")

        if self.adj_matrix[u][v] == 1:
            return  # Edge already exists

        self.adj_list[u].append(v)
        self.adj_matrix[u][v] = 1
        self.edge_list.append((u, v))

        if not self.directed and u != v:
            self.adj_list[v].append(u)
            self.adj_matrix[v][u] = 1
            self.edge_list.append((v, u))

    def print_matrix(self):
        """Print the adjacency matrix representation of the graph."""
        for row in self.adj_matrix:
            print(" ".join(map(str, row)))

    def print_list(self):
        """Print the adjacency list representation of the graph."""
        for i, neighbors in enumerate(self.adj_list):
            print(f"{i}: {' '.join(map(str, neighbors))}")

    def print_table(self):
        """Print the edge list representation of the graph."""
        for u, v in self.edge_list:
            print(f"({u}, {v})")

    def edge_exists(self, u, v):
        """
        Check if an edge exists between nodes u and v.

        Args:
            u (int): Source node
            v (int): Destination node

        Returns:
            bool: True if edge exists, False otherwise
        """
        if u < 0 or u >= self.nodes or v < 0 or v >= self.nodes:
            return False
        return self.adj_matrix[u][v] == 1

    def bfs(self, start):
        """
        Perform Breadth-First Search starting from the given node.

        Args:
            start (int): Starting node

        Returns:
            list: BFS traversal order
        """
        if start < 0 or start >= self.nodes:
            raise ValueError("Invalid start node")

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
        """Utility function for DFS recursion."""
        visited[u] = True
        order.append(u)
        for v in self.adj_list[u]:
            if not visited[v]:
                self.dfs_util(v, visited, order)

    def dfs(self, start):
        """
        Perform Depth-First Search starting from the given node.

        Args:
            start (int): Starting node

        Returns:
            list: DFS traversal order
        """
        if start < 0 or start >= self.nodes:
            raise ValueError("Invalid start node")

        visited = [False] * self.nodes
        order = []
        self.dfs_util(start, visited, order)
        return order

    def to_tikz(self, filename="graph.tex"):
        """
        Generate TikZ code for visualizing the graph.

        Args:
            filename (str): Output file name
        """
        tikz_lines = [
            "\\documentclass{standalone}",
            "\\usepackage{tikz}",
            "\\usetikzlibrary{graphs, graphdrawing, arrows.meta}",
            "\\usegdlibrary{layered}",
            "",
            "\\begin{document}",
            "\\begin{tikzpicture}[>=Stealth, every node/.style={circle, draw, minimum size=1cm}]",
            "  \\graph [layered layout, sibling distance=2cm, level distance=2cm] {"
        ]

        for i in range(self.nodes):
            tikz_lines.append(f"    {i};")

        # For undirected graphs, we need to avoid duplicate edges
        if self.directed:
            edges = self.edge_list
        else:
            edges = list(set((min(u, v), max(u, v)) for u, v in self.edge_list))

        for u, v in edges:
            tikz_lines.append(f"    {u} -- {v};" if not self.directed else f"    {u} -> {v};")

        tikz_lines.append("  };")
        tikz_lines.append("\\end{tikzpicture}")
        tikz_lines.append("\\end{document}")

        with open(filename, "w") as f:
            f.write("\n".join(tikz_lines))

    def kahn_topological_sort(self):
        """
        Perform topological sort using Kahn's algorithm.
        Only works for directed acyclic graphs (DAGs).
        """
        if not self.directed:
            print("Topological sort only works for directed graphs")
            return

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
            print("Graph has at least one cycle - topological sort not possible")
        else:
            print("Topological order (Kahn):", " ".join(map(str, topo_order)))

    def tarjan_topological_sort(self):
        """
        Perform topological sort using Tarjan's algorithm.
        Only works for directed acyclic graphs (DAGs).
        """
        if not self.directed:
            print("Topological sort only works for directed graphs")
            return

        visited = [0] * self.nodes  # 0 = unvisited, 1 = temporary, 2 = permanent
        topo_order = []

        def visit(u):
            if visited[u] == 2:
                return
            if visited[u] == 1:
                raise ValueError("Graph contains at least one cycle")
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
    parser = argparse.ArgumentParser(description="Graph representation and algorithms")
    parser.add_argument('--generate', action='store_true', help="Generate a random graph")
    parser.add_argument('--user-provided', action='store_true', help="Input graph manually")
    parser.add_argument('--undirected', action='store_true', help="Create an undirected graph")
    args = parser.parse_args()

    try:
        if args.generate:
            nodes = int(input("Number of nodes > "))
            if nodes <= 0:
                raise ValueError("Number of nodes must be positive")

            saturation = float(input("Saturation > "))
            if not 0 <= saturation <= 1:
                raise ValueError("Saturation must be between 0 and 1")

            graph = Graph(nodes, directed=not args.undirected)
            max_edges = (nodes * (nodes - 1)) // 2 if not args.undirected else nodes * (nodes - 1)
            edge_count = int(saturation * max_edges)

            if args.undirected:
                possible_edges = [(i, j) for i in range(nodes) for j in range(i + 1, nodes)]
            else:
                possible_edges = [(i, j) for i in range(nodes) for j in range(nodes) if i != j]

            if edge_count > len(possible_edges):
                edge_count = len(possible_edges)

            selected_edges = sample(possible_edges, edge_count)

            for u, v in selected_edges:
                graph.add_edge(u, v)

        elif args.user_provided:
            nodes = int(input("Number of nodes > "))
            if nodes <= 0:
                raise ValueError("Number of nodes must be positive")

            graph = Graph(nodes, directed=not args.undirected)
            print(f"Enter neighbors for each node (0-{nodes - 1}), space separated:")
            for u in range(nodes):
                while True:
                    try:
                        raw = input(f"{u} > ").strip()
                        if not raw:
                            break
                        neighbors = list(map(int, raw.split()))
                        for v in neighbors:
                            if v < 0 or v >= nodes:
                                raise ValueError(f"Invalid neighbor index {v}")
                            graph.add_edge(u, v)
                        break
                    except ValueError as e:
                        print(f"Error: {e}. Please try again.")
        else:
            print("Error: You must specify either --generate or --user-provided")
            return

        print("\nGraph operations available:")
        print("  print [matrix/list/table] - Print graph representation")
        print("  find u v - Check if edge exists between u and v")
        print("  bfs start - Perform BFS from start node")
        print("  dfs start - Perform DFS from start node")
        print("  tikz - Generate TikZ visualization")
        print("  kahn - Perform Kahn's topological sort")
        print("  tarjan - Perform Tarjan's topological sort")
        print("  exit - Quit the program\n")

        while True:
            try:
                action = input("action> ").strip().lower()
                if not action:
                    continue

                if action == "print":
                    rep = input("representation? matrix / list / table > ").strip().lower()
                    if rep == "matrix":
                        graph.print_matrix()
                    elif rep == "list":
                        graph.print_list()
                    elif rep == "table":
                        graph.print_table()
                    else:
                        print("Invalid representation type")

                elif action == "find":
                    try:
                        u = int(input("from> "))
                        v = int(input("to> "))
                        print("Edge exists" if graph.edge_exists(u, v) else "No edge")
                    except ValueError:
                        print("Invalid node indices")

                elif action == "bfs":
                    try:
                        start = int(input("start node> "))
                        print("BFS order:", " ".join(map(str, graph.bfs(start))))
                    except ValueError as e:
                        print(e)

                elif action == "dfs":
                    try:
                        start = int(input("start node> "))
                        print("DFS order:", " ".join(map(str, graph.dfs(start))))
                    except ValueError as e:
                        print(e)

                elif action == "tikz":
                    filename = input("output filename (default: graph.tex)> ").strip()
                    if not filename:
                        filename = "graph.tex"
                    graph.to_tikz(filename)
                    print(f"TikZ code written to {filename}")

                elif action == "kahn":
                    graph.kahn_topological_sort()

                elif action == "tarjan":
                    graph.tarjan_topological_sort()

                elif action == "exit":
                    break

                else:
                    print("Unknown command")

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {e}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()