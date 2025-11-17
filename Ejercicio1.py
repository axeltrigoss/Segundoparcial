# ejercicio1 Pokedex 
from typing import List, Optional, Any, Set, Dict, Iterable, Tuple
from dataclasses import dataclass

@dataclass
class Pokemon:
    name: str
    number: int
    types: List[str]
    weaknesses: List[str]
    mega: bool
    gigamax: bool
    
    def __repr__(self):
        return (f"({self.number}) {self.name} | Types: {', '.join(self.types)} | Weaknesses: {', '.join(self.weaknesses)} | "
                f"Mega: {'Yes' if self.mega else 'No'} | Gigamax: {'Yes' if self.gigamax else 'No'}")

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        # Almacenar los números para evitar almacenar el objeto completo
        self.pokemon_numbers: Set[int] = set()
        self.is_end: bool = False

class NameTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, name: str, number: int):
        node = self.root
        name_low = name.lower()
        for ch in name_low:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            # Agregando el número en cada nodo del camino
            node.pokemon_numbers.add(number)
        node.is_end = True

    def _node_for_prefix(self, prefix: str) -> Optional[TrieNode]:
        """Devuelve el nodo que representa el final del prefijo."""
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search_prefix(self, prefix: str) -> Set[int]:
        """Devuelve set de números de Pokémon cuyos nombres empiezan con prefix (case-insensitive)."""
        node = self._node_for_prefix(prefix)
        # Si encuentra el nodo,va a devolver todos los números asociados a ese subárbol
        return set(node.pokemon_numbers) if node else set()

class BSTNode:
    def __init__(self, key: Any, value: Any = None):
        self.key = key
        self.value = value
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None

class BST:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: Any, value: Any):
        def _insert(node, key, value):
            if node is None:
                return BSTNode(key, value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                # Si la clave existe, actualizamos/extendemos.el value
                if isinstance(node.value, set):
                    # Asumimos que el nuevo 'value' es un conjunto o un elemento individual
                    node.value.update(value if isinstance(value, set) else {value})
                elif isinstance(node.value, list):
                    node.value.extend(value if isinstance(value, list) else [value])
                else:
                    node.value = value
            return node
        self.root = _insert(self.root, key, value)

    def find(self, key: Any) -> Optional[Any]:
        """Busca y devuelve el valor asociado a la clave."""
        node = self.root
        while node:
            if key == node.key:
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def inorder(self) -> List[Tuple[Any, Any]]:
        """Recorrido Inorden: devuelve lista de tuplas (key, value) ordenadas por clave."""
        out = []
        def _in(node):
            if not node: return
            _in(node.left)
            out.append((node.key, node.value))
            _in(node.right)
        _in(self.root)
        return 
      
class Pokedex:
    def __init__(self, pokemons: Iterable[Dict[str, Any]]):
        # 1. Almacenar pokemon por número para acceso
        self.by_number: Dict[int, Pokemon] = {}
        # 2. Árboles/índices
        self.name_trie = NameTrie()    # índice por nombre 
        self.number_bst = BST()        # índice por número 
        self.type_bst = BST()          # índice por tipo 

        # Construir índices
        for p in pokemons:
            pk = Pokemon(
                name=p["name"],
                number=int(p["number"]),
                types=[t for t in p.get("types", [])],
                weaknesses=[w for w in p.get("weaknesses", [])],
                mega=bool(p.get("mega", False)),
                gigamax=bool(p.get("gigamax", False))
            )
            self.by_number[pk.number] = pk
            # a. índice por nombre
            self.name_trie.insert(pk.name, pk.number)
            # b. índice por número
            self.number_bst.insert(pk.number, pk)
            # c. índice por tipo
            for t in pk.types:
                # Usando el insert de BST que maneja la actualización de sets
                self.type_bst.insert(t, pk.number)

    ## Muestra todos los datos de un Pokémon a partir de su número
    def get_by_number(self, number: int) -> Optional[Pokemon]:
        """Acceso O(log n) a través del BST de números o O(1) con el dict auxiliar."""
        # Acceso al dict auxiliar:
        return self.by_number.get(number)

    ## Miestra todos los datos de un Pokémon a partir de su nombre 
    def search_name_proximity(self, query: str) -> List[Pokemon]:
        """
        Búsqueda por proximidad: devuelve Pokémons cuyo nombre **empiece** por query (usando Trie)
        o lo **contenga** (usando un scan simple).
        """
        q = query.lower()
        result_numbers = set()

        # 1. Búsqueda por prefijo 
        prefix_matches = self.name_trie.search_prefix(q)
        result_numbers.update(prefix_matches)

        # 2. Búsqueda de contencióm
        for pk in self.by_number.values():
            if q in pk.name.lower():
                result_numbers.add(pk.number)

        # Devolverobjetos Pokémon, ordenados por número para consistencia
        return sorted((self.by_number[n] for n in result_numbers), key=lambda x: x.number)

    ## Muestra todos los nombres de los Pokémons de un determinado tipo
    def get_names_by_type(self, type_name: str) -> List[str]:
        """Usa el BST de tipos para obtener números y luego el dict para nombres."""
        numbers = self.type_bst.find(type_name)
        if not numbers:
            return []
        # Devolver nombres ordenados alfabéticamente
        return sorted([self.by_number[n].name for n in numbers])

    ## Listado en orden ascendente por número
    def list_sorted_by_number(self) -> List[Pokemon]:
        """Usa el recorrido Inorden del BST de números."""
        # El Inorden del number_bst devuelve , ya ordenado por número
        return [val for (k, val) in self.number_bst.inorder()]

    ## Listado en orden ascendente por nombre
    def list_sorted_by_name(self) -> List[Pokemon]:
        """Requiere ordenar la lista completa (O(n log n))."""
        return sorted(self.by_number.values(), key=lambda p: p.name.lower())

    ## Listado por nivel por nombre 
    def list_grouped_by_name_length(self) -> Dict[int, List[Pokemon]]:
        """Agrupa Pokémons por la longitud de su nombre (nivel)."""
        grouping: Dict[int, List[Pokemon]] = {}
        for p in self.by_number.values():
            L = len(p.name)
            grouping.setdefault(L, []).append(p)

        # Ordena cada lista por nombre
        for k in grouping:
            grouping[k].sort(key=lambda x: x.name.lower())
        # Ordena el diccionario por la clave 
        return dict(sorted(grouping.items()))

    ## Muestra todos los Pokémons que son débiles frente a Jolteon, Lycanroc y Tyrantrum
    def pokemons_weak_to_attackers(self, attackers: List[str]) -> List[Pokemon]:
        """
        Determina qué Pokémons son débiles a los tipos de los atacantes.
        Asume los tipos de los atacantes conocidos: Jolteon (Electric), Lycanroc (Rock), Tyrantrum (Rock, Dragon).
        """
        # Mapa de tipos de los atacantes
        attacker_type_map: Dict[str, List[str]] = {
            "jolteon": ["Electric"],
            "lycanroc": ["Rock"],
            "tyrantrum": ["Rock", "Dragon"],
        }
        
        target_types = set()
        # Recolectar todos los tipos relevantes
        for a in attackers:
            tlist = attacker_type_map.get(a.lower(), [])
            for t in tlist:
                target_types.add(t.lower())

        result: List[Pokemon] = []
        for p in self.by_number.values():
            # Comparar si alguna debilidad del Pokémon está en los tipos de ataque
            if any(w.lower() in target_types for w in p.weaknesses):
                result.append(p)
                
        # Ordenar por número
        result.sort(key=lambda x: x.number)
        return result

    ## Muestraa todos los tipos de Pokémons y cuántos hay de cada tipo
    def count_by_type(self) -> Dict[str, int]:
        """Usa el recorrido Inorden del BST de tipos para obtener los tipos ordenados y su conteo."""
        counts = {}
        # k=tipo, v=set de números
        for k, v in self.type_bst.inorder():
            counts[k] = len(v) if v else 0
        return counts

    ## Determinar cuantos Pokémons tienen megaevolucion.
    def count_mega(self) -> int:
        return sum(1 for p in self.by_number.values() if p.mega)

    ## Determinar cuantos Pokémons tiene forma gigamax.
    def count_gigamax(self) -> int:
        return sum(1 for p in self.by_number.values() if p.gigamax)

# Datos de ejemplo 
pokemons_30 = [
    {"name":"Bulbasaur","number":1,"types":["Grass","Poison"],
     "weaknesses":["Fire","Ice","Flying","Psychic"],"mega":False,"gigamax":False},
    {"name":"Ivysaur","number":2,"types":["Grass","Poison"],
     "weaknesses":["Fire","Ice","Flying","Psychic"],"mega":False,"gigamax":False},
    {"name":"Venusaur","number":3,"types":["Grass","Poison"],
     "weaknesses":["Fire","Ice","Flying","Psychic"],"mega":True,"gigamax":True},
    {"name":"Charmander","number":4,"types":["Fire"],
     "weaknesses":["Water","Ground","Rock"],"mega":False,"gigamax":False},
    {"name":"Charmeleon","number":5,"types":["Fire"],
     "weaknesses":["Water","Ground","Rock"],"mega":False,"gigamax":False},
    {"name":"Charizard","number":6,"types":["Fire","Flying"],
     "weaknesses":["Water","Electric","Rock"],"mega":True,"gigamax":True},
    {"name":"Squirtle","number":7,"types":["Water"],
     "weaknesses":["Grass","Electric"],"mega":False,"gigamax":False},
    {"name":"Wartortle","number":8,"types":["Water"],
     "weaknesses":["Grass","Electric"],"mega":False,"gigamax":False},
    {"name":"Blastoise","number":9,"types":["Water"],
     "weaknesses":["Grass","Electric"],"mega":True,"gigamax":True},
    {"name":"Pikachu","number":25,"types":["Electric"],
     "weaknesses":["Ground"],"mega":False,"gigamax":True},
    {"name":"Raichu","number":26,"types":["Electric"],
     "weaknesses":["Ground"],"mega":False,"gigamax":False},
    {"name":"Jigglypuff","number":39,"types":["Normal","Fairy"],
     "weaknesses":["Steel","Poison"],"mega":False,"gigamax":False},
    {"name":"Wigglytuff","number":40,"types":["Normal","Fairy"],
     "weaknesses":["Steel","Poison"],"mega":False,"gigamax":False},
    {"name":"Zubat","number":41,"types":["Poison","Flying"],
     "weaknesses":["Electric","Ice","Psychic","Rock"],"mega":False,"gigamax":False},
    {"name":"Golbat","number":42,"types":["Poison","Flying"],
     "weaknesses":["Electric","Ice","Psychic","Rock"],"mega":False,"gigamax":False},
    {"name":"Oddish","number":43,"types":["Grass","Poison"],
     "weaknesses":["Fire","Ice","Flying","Psychic"],"mega":False,"gigamax":False},
    {"name":"Gloom","number":44,"types":["Grass","Poison"],
     "weaknesses":["Fire","Ice","Flying","Psychic"],"mega":False,"gigamax":False},
    {"name":"Vileplume","number":45,"types":["Grass","Poison"],
     "weaknesses":["Fire","Ice","Flying","Psychic"],"mega":False,"gigamax":False},
    {"name":"Growlithe","number":58,"types":["Fire"],
     "weaknesses":["Water","Ground","Rock"],"mega":False,"gigamax":False},
    {"name":"Arcanine","number":59,"types":["Fire"],
     "weaknesses":["Water","Ground","Rock"],"mega":False,"gigamax":False},
    {"name":"Geodude","number":74,"types":["Rock","Ground"],
     "weaknesses":["Water","Grass","Fighting","Ice","Ground","Steel"],
     "mega":False,"gigamax":False},
    {"name":"Graveler","number":75,"types":["Rock","Ground"],
     "weaknesses":["Water","Grass","Fighting","Ice","Ground","Steel"],
     "mega":False,"gigamax":False},
    {"name":"Golem","number":76,"types":["Rock","Ground"],
     "weaknesses":["Water","Grass","Fighting","Ice","Ground","Steel"],
     "mega":False,"gigamax":False},
    {"name":"Magnemite","number":81,"types":["Electric","Steel"],
     "weaknesses":["Fire","Fighting","Ground"],"mega":False,"gigamax":False},
    {"name":"Magneton","number":82,"types":["Electric","Steel"],
     "weaknesses":["Fire","Fighting","Ground"],"mega":False,"gigamax":False},
    {"name":"Gengar","number":94,"types":["Ghost","Poison"],
     "weaknesses":["Ghost","Psychic","Dark","Ground"],
     "mega":True,"gigamax":True},
    {"name":"Onix","number":95,"types":["Rock","Ground"],
     "weaknesses":["Water","Grass","Fighting","Ice","Ground","Steel"],
     "mega":False,"gigamax":False},
    {"name":"Voltorb","number":100,"types":["Electric"],
     "weaknesses":["Ground"],"mega":False,"gigamax":False},
    {"name":"Electrode","number":101,"types":["Electric"],
     "weaknesses":["Ground"],"mega":False,"gigamax":False},
    {"name":"Jolteon","number":135,"types":["Electric"],
     "weaknesses":["Ground"],"mega":False,"gigamax":False},
]
# Demostración del uso

class TestPokedex:
    def __init__(self, data):
        self.pdx = Pokedex(data)

    def run_tests(self):
        print("🧪 Demostración de Consultas de Pokedex\n" + "="*40)

        # 1. Muestra todos los datos de un Pokémon a partir de su número y nombre 
        print("## 1. Búsqueda por Número (Pikachu, #25) 🔍")
        pk_num = self.pdx.get_by_number(25)
        print(f"Resultado: {pk_num}")
        print("-" * 40)

        print("## 2. Búsqueda por Nombre (proximidad: 'bul' y 'ar') 🔎")
        print("Búsqueda 'bul' (prefijo):", [p.name for p in self.pdx.search_name_proximity("bul")])
        print("Búsqueda 'ar' (contiene):", [p.name for p in self.pdx.search_name_proximity("ar")])
        print("-" * 40)

        # 2. Mostrar todos los nombres de los Pokémons de un determinado tipo: fantasma, fuego, acero y eléctrico
        print("## 3. Nombres de Pokémons por Tipo 👻🔥⚙️⚡")
        for t in ["Ghost", "Fire", "Steel", "Electric"]:
            names = self.pdx.get_names_by_type(t)
            print(f"Tipo **{t}** ({len(names)}): {names}")
        print("-" * 40)

        # 3. Listado en orden ascendente por número y nombre
        print("## 4. Listados Ordenados 🔢🔤")
        print("Listado por Número (primeros 5):", [p.name for p in self.pdx.list_sorted_by_number()[:5]])
        print("Listado por Nombre (primeros 5):", [p.name for p in self.pdx.list_sorted_by_name()[:5]])
        print("-" * 40)

        # 4. Listado por nivel por nombre 
        print("## 5. Listado Agrupado por Longitud de Nombre (Nivel) 📏")
        grouped = self.pdx.list_grouped_by_name_length()
        for length, names in grouped.items():
            print(f"Longitud **{length}** ({len(names)}): {[p.name for p in names]}")
        print("-" * 40)

        # 5. Mostrar todos los Pokémons que son débiles frente a Jolteon, Lycanroc y Tyrantrum
        print("## 6. Débiles a Jolteon (Electric), Lycanroc (Rock), Tyrantrum (Rock, Dragon) 💥")
        weak_to_attackers = self.pdx.pokemons_weak_to_attackers(["Jolteon", "Lycanroc", "Tyrantrum"])
        print(f"Total débiles: **{len(weak_to_attackers)}**")
        print("Nombres:", [p.name for p in weak_to_attackers])
        
        print("-" * 40)
        
        # 6. Mostrar todos los tipos de Pokémons y cuántos hay de cada tipo
        print("## 7. Conteo de Pokémons por Tipo 📊")
        counts = self.pdx.count_by_type()
        for t, c in counts.items():
            print(f"Tipo **{t}**: {c}")
        print("-" * 40)

        # 7. Determinar cuantos Pokémons tienen megaevolucion.
        print("## 8. Conteo de Megaevoluciones 🧬")
        print("Pokémons con Megaevolución:", self.pdx.count_mega())
        print("-" * 40)

        # 8. Determinar cuantos Pokémons tiene forma gigamax.
        print("## 9. Conteo de Formas Gigamax 🦹")
        print("Pokémons con Gigamax:", self.pdx.count_gigamax())
        print("="*40)


if __name__ == "__main__":
    tester = TestPokedex(pokemons_30)
    tester.run_tests()
