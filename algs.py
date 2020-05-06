# Algorithms


# used in mst function
class Graph:
    def __init__(self, count):
        self.graph = {}
        self.count = count

    def add(self, edge):  # (src, dest)
        try:
            self.graph[edge[0]].append(edge[1])
        except KeyError:
            self.graph[edge[0]] = [edge[1]]

    def get_pred(self, preds, node):
        if preds[node] == -1:
            return node
        else:
            return self.get_pred(preds, preds[node])

    def has_cycle(self):
        preds = [-1]*self.count
        for nodeA in self.graph:
            for nodeB in self.graph[nodeA]:
                A = self.get_pred(preds, nodeA)
                B = self.get_pred(preds, nodeB)
                if A == B:
                    return True
                else:
                    A = self.get_pred(preds, A)
                    B = self.get_pred(preds, B)
                    preds[A] = B


# minimum spanning tree
def mst(matrix):
    edges = []
    tree = []
    nodeCount = len(matrix)

    for r in range(0, nodeCount):
        for c in range(r, nodeCount):
            if (matrix[r][c] > -1) and (r != c):
                edges.append((r, c, matrix[r][c]))

    # remove weights from tuples after sorting
    sortedEdges = [(x[0], x[1], x[2]) for x in sorted(edges, key=lambda t: -t[2])]
    e = sortedEdges.copy()

    tree.append(e.pop())
    while len(tree) < (nodeCount-1):
        g = Graph(nodeCount)
        tree.append(e.pop())
        for edge in tree:
            g.add(edge)

        if g.has_cycle():
            tree.pop()

    return edges, sortedEdges, tree
