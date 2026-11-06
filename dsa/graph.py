from collections import deque


class OrderGraph:
    """
    Graph representing relationships between
    departments, services and collection points.
    """

    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        """
        Add a vertex.
        """

        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        """
        Add an undirected edge.
        """

        self.add_vertex(vertex1)
        self.add_vertex(vertex2)

        if vertex2 not in self.graph[vertex1]:
            self.graph[vertex1].append(vertex2)

        if vertex1 not in self.graph[vertex2]:
            self.graph[vertex2].append(vertex1)

    def bfs(self, start):
        """
        Breadth First Search.
        """

        if start not in self.graph:
            return []

        visited = set()
        queue = deque()

        result = []

        queue.append(start)
        visited.add(start)

        while queue:

            current = queue.popleft()

            result.append(current)

            for neighbour in self.graph[current]:

                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return result

    def dfs(self, start):
        """
        Depth First Search.
        """

        if start not in self.graph:
            return []

        visited = set()
        result = []

        def traverse(vertex):

            visited.add(vertex)
            result.append(vertex)

            for neighbour in self.graph[vertex]:

                if neighbour not in visited:
                    traverse(neighbour)

        traverse(start)

        return result

    def display(self):
        return self.graph


if __name__ == "__main__":

    graph = OrderGraph()

    graph.add_edge("CSE Department", "Xerox Service")
    graph.add_edge("Xerox Service", "Main Collection Point")
    graph.add_edge("Main Collection Point", "Library")
    graph.add_edge("Library", "Printing Service")
    graph.add_edge("CSE Department", "Printing Service")

    print("===== GRAPH =====")

    print("\nGraph:")
    print(graph.display())

    print("\nBFS from CSE Department:")
    print(graph.bfs("CSE Department"))

    print("\nDFS from CSE Department:")
    print(graph.dfs("CSE Department"))