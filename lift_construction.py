from itertools import product

def get_ordered_r_minus_1_cliques(G, r):
    r = int(r)
    V = list(G.vertices())
    if r == 2:
        return [(v,) for v in V]

    cliques = []
    def is_clique(t):
        return all(G.has_edge(t[i], t[j]) for i in range(len(t)) for j in range(i + 1, len(t)))

    def build_tuples(prefix):
        if len(prefix) == r - 1:
            if is_clique(prefix):
                cliques.append(tuple(prefix))
            return
        for v in V:
            if v not in prefix:
                build_tuples(prefix + [v])

    build_tuples([])
    return cliques

def build_HL_lift_graph(G, r, d, mode='ordered'):
    r = int(r)
    d = int(d)
    Kr = get_ordered_r_minus_1_cliques(G, r)
    B = Graph()

    B.add_vertices([("T", x) for x in Kr])
    B.add_vertices([("B", x) for x in Kr])

    for x in Kr:
        for y in Kr:
            if x == y:
                continue
            diffs = [i for i in range(r - 1) if x[i] != y[i]]
            if len(diffs) == d:
                if mode == 'ordered':
                    if all(G.has_edge(x[i], y[i]) and x[i] < y[i] for i in diffs):
                        B.add_edge(("T", x), ("B", y))
                elif mode == 'symmetric':
                    if all(G.has_edge(x[i], y[i]) for i in diffs):
                        B.add_edge(("T", x), ("B", y))
                        B.add_edge(("T", y), ("B", x))

    return B.line_graph()


