from heapq import heappush, heappop
from collections import deque
import math

class Graph:
    def __init__(self):
        self.adj = {}          
        self.episodes = {}     

    def add_vertex(self, v, episodes=None):
        if v not in self.adj:
            self.adj[v] = {}
        if episodes is not None:
            self.episodes[v] = episodes

    def add_edge(self, a, b, weight):
        if weight < 0:
            raise ValueError("weight must be non-negative")
        self.adj.setdefault(a, {})[b] = weight
        self.adj.setdefault(b, {})[a] = weight

    def vertices(self):
        return list(self.adj.keys())

    def max_spanning_tree(self, start):
        if start not in self.adj:
            raise KeyError(f"Start vertex {start} not in graph")
       
        visited = set([start])
     
        
        for v, w in self.adj[start].items():
            heappush(edges, (-w, start, v))
            
        mst_edges = []
        total_weight = 0
        
        while edges and len(visited) < len(self.adj):
            neg_w, u, v = heappop(edges)
            w = -neg_w 
            if v in visited:
                continue
            
            visited.add(v)
            mst_edges.append((u, v, w))
            total_weight += w
            
            for nbr, wt in self.adj[v].items():
                if nbr not in visited:
                    heappush(edges, (-wt, v, nbr))
                    
        return mst_edges, total_weight

    def max_shared_pairs(self):
        max_w = -math.inf
        pairs = []
        seen = set()
        for u in self.adj:
            for v, w in self.adj[u].items():
                if tuple(sorted((u, v))) in seen:
                    continue
                seen.add(tuple(sorted((u, v))))
                
                if w > max_w:
                    max_w = w
                    pairs = [(u, v)]
                elif w == max_w:
                    pairs.append((u, v))
                    
        if max_w == -math.inf:
            return None, []
        return max_w, pairs

    def dijkstra_strongest_path(self, start, end):
        if start not in self.adj or end not in self.adj:
            return None, math.inf
        
        pq = []
        heappush(pq, (0.0, start, [start]))
        dist = {start: 0.0}
        
        while pq:
            d, u, path = heappop(pq)
            
            if u == end:
                return path, d
            
            if d > dist.get(u, math.inf):
                continue
            
            for v, weight in self.adj[u].items():
                if weight <= 0:
                    continue
                cost = 1.0 / weight
                nd = d + cost
                
                if nd < dist.get(v, math.inf):
                    dist[v] = nd
                    heappush(pq, (nd, v, path + [v]))
                    
        return None, math.inf

    def shortest_unweighted(self, start, end)
        if start not in self.adj or end not in self.adj:
            return None, None
            
        q = deque([(start, [start])])
        seen = {start}
        
        while q:
            u, path = q.popleft()
            
            if u == end:
                return path, len(path)-1
                
            for v in self.adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append((v, path + [v]))
                    
        return None, None


def build_example_graph():
    G = Graph()
    required = [
        "Luke Skywalker", "Darth Vader", "Yoda", "Boba Fett", "C-3PO",
        "Leia", "Rey", "Kylo Ren", "Chewbacca", "Han Solo", "R2-D2", "BB-8"
    ]
    extras = [
        "Obi-Wan Kenobi", "Palpatine", "Finn", "Poe Dameron", "Mace Windu",
        "Padmé Amidala", "Jango Fett", "Anakin Skywalker", "Lando Calrissian"
    ]

    episodes_counts = {
        "Luke Skywalker": 6,
        "Darth Vader": 4,
        "Yoda": 5,
        "Boba Fett": 2,
        "C-3PO": 9,
        "Leia": 8,
        "Rey": 3,
        "Kylo Ren": 3,
        "Chewbacca": 8,
        "Han Solo": 4,
        "R2-D2": 9,
        "BB-8": 1,
        "Obi-Wan Kenobi": 6,
        "Palpatine": 5,
        "Finn": 2,
        "Poe Dameron": 2,
        "Mace Windu": 1,
        "Padmé Amidala": 3,
        "Jango Fett": 1,
        "Anakin Skywalker": 4,
        "Lando Calrissian": 3
    }

    for name, eps in episodes_counts.items():
        G.add_vertex(name, episodes=eps)

    edges = [
        ("Luke Skywalker", "Leia", 5),
        ("Luke Skywalker", "Han Solo", 4),
        ("Luke Skywalker", "Darth Vader", 3),
        ("Luke Skywalker", "R2-D2", 6),
        ("Luke Skywalker", "C-3PO", 6),
        ("Leia", "Han Solo", 5),
        ("Leia", "C-3PO", 6),
        ("Leia", "R2-D2", 5),
        ("Han Solo", "Chewbacca", 5),
        ("Chewbacca", "C-3PO", 4),
        ("C-3PO", "R2-D2", 7),
        ("Darth Vader", "Palpatine", 4),
        ("Darth Vader", "Anakin Skywalker", 2),
        ("Yoda", "Luke Skywalker", 3),
        ("Yoda", "Darth Vader", 1),
        ("Boba Fett", "Jango Fett", 1),
        ("Rey", "BB-8", 2),
        ("Rey", "Kylo Ren", 2),
        ("Kylo Ren", "Finn", 1),
        ("Poe Dameron", "Finn", 1),
        ("Obi-Wan Kenobi", "Anakin Skywalker", 3),
        ("Obi-Wan Kenobi", "Padmé Amidala", 2),
        ("Palpatine", "Anakin Skywalker", 2),
        ("Lando Calrissian", "Han Solo", 2),
        ("Chewbacca", "R2-D2", 3),
        ("BB-8", "R2-D2", 1),
        ("Boba Fett", "Darth Vader", 1),
        ("C-3PO", "BB-8", 1)
    ]

    for a, b, w in edges:
        G.add_edge(a, b, w)

    return G, required, extras


def main():
    G, required, extras = build_example_graph()
  
    starts = ["C-3PO", "Yoda", "Leia"]
    print("--- Árboles de expansión MÁXIMA (Prim adaptado) ---")
    print(" (Busca el máximo de episodios compartidos para conectar a todos)")
    for s in starts:
        try:
            mst_edges, total_w = G.max_spanning_tree(s)
            print(f"\nInicio: {s} | Peso total del MaxST (conexión más fuerte): {total_w}")
            for u, v, w in mst_edges:
                print(f"   {u} -- {v}  (aparecieron juntos en {w} episodios)")
            
        except KeyError:
            print(f"Vertice {s} no encontrado en el grafo")

    max_w, pairs = G.max_shared_pairs()
    print("\n--- Máximo número de episodios compartidos entre dos personajes ---")
    print(f"Valor máximo: {max_w}")
    print("Pares con ese valor:")
    for a, b in pairs:
        print(f"  - {a} <--> {b}  ({max_w} episodios)")
    print()

    print("--- Caminos más 'fuertes' (cost = 1 / shared_episodes) ---")
    p1, c1 = G.dijkstra_strongest_path("C-3PO", "R2-D2")
    print(f"C-3PO -> R2-D2 (camino): {p1}   costo total = {c1:.6f} (busca minimizar la suma de 1/peso)")
    p2, c2 = G.dijkstra_strongest_path("Yoda", "Darth Vader")
    if p2:
        print(f"Yoda -> Darth Vader (camino): {p2}   costo total = {c2:.6f}")
    else:
        print("No existe camino entre Yoda y Darth Vader en este grafo")

    print('\n--- Caminos por menor número de saltos (BFS) ---')
    p1u, hops1 = G.shortest_unweighted("C-3PO", "R2-D2")
    print(f"C-3PO -> R2-D2 (fewest hops): {p1u}  saltos = {hops1}")
    p2u, hops2 = G.shortest_unweighted("Yoda", "Darth Vader")
    print(f"Yoda -> Darth Vader (fewest hops): {p2u}  saltos = {hops2}")

    nine_eps = [v for v, eps in G.episodes.items() if eps == 9]
    print('\n--- Personajes que aparecen en 9 episodios (según datos cargados) ---')
    if nine_eps:
        for ch in nine_eps:
            print('  -', ch)
    else:
        print('  Ninguno (según los datos actuales)')

    print('\n--- Listas de personajes cargados ---')
    print('Requeridos:', ', '.join(required))
    print('Extras   :', ', '.join(extras))


if __name__ == '__main__':
    main()
