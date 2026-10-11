"""
Act. de Seguimiento 3 - Algoritmos 2
Opción 5: Red social de amigos (Grafos)

Representación: grafo NO dirigido con LISTA DE ADYACENCIA,
implementado manualmente con un diccionario:
    { "Ana": ["Carlos", "Luis"], "Carlos": ["Ana", "Pedro"], ... }
Cada clave es un vértice (estudiante) y su lista contiene sus amigos (aristas).
"""

from collections import deque  # solo se usa como COLA para el BFS (no es una librería de grafos)


class RedSocial:
    """Grafo no dirigido que representa amistades entre estudiantes."""

    def __init__(self):
        # Lista de adyacencia: nombre -> lista de amigos
        self.adyacencia = {}

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    @staticmethod
    def normalizar(nombre):
        """Quita espacios sobrantes y pone formato 'Nombre Apellido'."""
        return " ".join(nombre.split()).title()

    def existe(self, nombre):
        return self.normalizar(nombre) in self.adyacencia

    def _verificar(self, nombre):
        """Lanza error si el estudiante no está registrado."""
        if not self.existe(nombre):
            raise ValueError(f"El estudiante '{self.normalizar(nombre)}' no está registrado.")

    # ------------------------------------------------------------------
    # 1. Registrar estudiantes (agregar vértice)
    # ------------------------------------------------------------------
    def registrar_estudiante(self, nombre):
        nombre = self.normalizar(nombre)
        if nombre == "" or not nombre.replace(" ", "").isalpha():
            raise ValueError("El nombre solo puede contener letras y no puede estar vacío.")
        if nombre in self.adyacencia:
            raise ValueError(f"'{nombre}' ya está registrado.")
        self.adyacencia[nombre] = []

    # ------------------------------------------------------------------
    # 2. Crear amistad (agregar arista en ambos sentidos)
    # ------------------------------------------------------------------
    def crear_amistad(self, a, b):
        self._verificar(a)
        self._verificar(b)
        a, b = self.normalizar(a), self.normalizar(b)
        if a == b:
            raise ValueError("Un estudiante no puede ser amigo de sí mismo.")
        if b in self.adyacencia[a]:
            raise ValueError(f"{a} y {b} ya son amigos.")
        self.adyacencia[a].append(b)
        self.adyacencia[b].append(a)  # grafo no dirigido

    # ------------------------------------------------------------------
    # 3. Mostrar amigos de un estudiante
    # ------------------------------------------------------------------
    def amigos_de(self, nombre):
        self._verificar(nombre)
        return list(self.adyacencia[self.normalizar(nombre)])

    # ------------------------------------------------------------------
    # 4. Consultar si dos estudiantes son amigos directos
    # ------------------------------------------------------------------
    def son_amigos(self, a, b):
        self._verificar(a)
        self._verificar(b)
        return self.normalizar(b) in self.adyacencia[self.normalizar(a)]

    # ------------------------------------------------------------------
    # 5. BFS (recorrido en anchura) - usa una COLA
    # ------------------------------------------------------------------
    def bfs(self, inicio):
        self._verificar(inicio)
        inicio = self.normalizar(inicio)
        visitados = [inicio]          # orden de visita
        cola = deque([inicio])
        while cola:                   # mientras haya vértices por explorar
            actual = cola.popleft()   # saca el más antiguo (FIFO)
            for vecino in self.adyacencia[actual]:
                if vecino not in visitados:
                    visitados.append(vecino)
                    cola.append(vecino)
        return visitados

    # ------------------------------------------------------------------
    # 6. DFS (recorrido en profundidad) - recursivo (usa la pila de llamadas)
    # ------------------------------------------------------------------
    def dfs(self, inicio):
        self._verificar(inicio)
        visitados = []
        self._dfs_recursivo(self.normalizar(inicio), visitados)
        return visitados

    def _dfs_recursivo(self, actual, visitados):
        visitados.append(actual)                      # se marca como visitado
        for vecino in self.adyacencia[actual]:
            if vecino not in visitados:               # caso recursivo: ir a fondo
                self._dfs_recursivo(vecino, visitados)
        # caso base implícito: si todos los vecinos ya fueron visitados, retorna

    # ------------------------------------------------------------------
    # 7. Contar amigos de cada estudiante (grado de cada vértice)
    # ------------------------------------------------------------------
    def contar_amigos(self):
        return {nombre: len(amigos) for nombre, amigos in self.adyacencia.items()}

    # ------------------------------------------------------------------
    # Reto: ruta entre dos estudiantes (BFS con padres -> ruta más corta)
    # ------------------------------------------------------------------
    def ruta(self, origen, destino):
        """Devuelve la lista de nombres de la ruta más corta, o [] si no hay conexión."""
        self._verificar(origen)
        self._verificar(destino)
        origen, destino = self.normalizar(origen), self.normalizar(destino)

        padres = {origen: None}       # de quién llegué a cada vértice
        cola = deque([origen])
        while cola:
            actual = cola.popleft()
            if actual == destino:
                break
            for vecino in self.adyacencia[actual]:
                if vecino not in padres:
                    padres[vecino] = actual
                    cola.append(vecino)

        if destino not in padres:
            return []                 # no hay camino

        # Reconstruir la ruta desde el destino hacia atrás
        camino = []
        nodo = destino
        while nodo is not None:
            camino.append(nodo)
            nodo = padres[nodo]
        camino.reverse()
        return camino


# ======================================================================
# Funciones de interfaz (menú)
# ======================================================================
def pedir_texto(mensaje):
    return input(mensaje).strip()


def cargar_ejemplo(red):
    """Carga el grafo del enunciado:
       Ana - Carlos - Pedro / Ana - Luis / Carlos - María / Luis - María
    """
    for n in ["Ana", "Carlos", "Pedro", "Luis", "María"]:
        if not red.existe(n):
            red.registrar_estudiante(n)
    for a, b in [("Ana", "Carlos"), ("Carlos", "Pedro"), ("Ana", "Luis"),
                 ("Carlos", "María"), ("Luis", "María")]:
        if not red.son_amigos(a, b):
            red.crear_amistad(a, b)


def consultar_amistad(red):
    a = pedir_texto("Primer estudiante: ")
    b = pedir_texto("Segundo estudiante: ")
    if red.son_amigos(a, b):
        print(f"Sí, {red.normalizar(a)} y {red.normalizar(b)} son amigos directos.")
    else:
        print("No son amigos directos.")
        camino = red.ruta(a, b)
        if camino:
            print("Pero existe una conexión indirecta: " + " → ".join(camino))
        else:
            print("Tampoco existe ninguna conexión indirecta.")


def menu():
    red = RedSocial()
    while True:
        print("\n===== RED SOCIAL DE AMIGOS =====")
        print("1. Registrar estudiante")
        print("2. Crear amistad")
        print("3. Mostrar amigos de un estudiante")
        print("4. Consultar si dos estudiantes son amigos")
        print("5. Recorrido BFS")
        print("6. Recorrido DFS")
        print("7. Contar amigos de cada estudiante")
        print("8. Mostrar ruta entre dos estudiantes (reto)")
        print("9. Cargar datos de ejemplo")
        print("10. Ejecutar casos de prueba")
        print("0. Salir")
        opcion = pedir_texto("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = pedir_texto("Nombre del estudiante: ")
                red.registrar_estudiante(nombre)
                print(f"Estudiante '{red.normalizar(nombre)}' registrado.")
            elif opcion == "2":
                a = pedir_texto("Primer estudiante: ")
                b = pedir_texto("Segundo estudiante: ")
                red.crear_amistad(a, b)
                print(f"Amistad creada entre {red.normalizar(a)} y {red.normalizar(b)}.")
            elif opcion == "3":
                nombre = pedir_texto("Estudiante: ")
                amigos = red.amigos_de(nombre)
                print(f"Amigos de {red.normalizar(nombre)}:")
                if amigos:
                    for amigo in amigos:
                        print("  -", amigo)
                else:
                    print("  (no tiene amigos todavía)")
            elif opcion == "4":
                consultar_amistad(red)
            elif opcion == "5":
                inicio = pedir_texto("Estudiante inicial: ")
                print("Recorrido BFS:")
                for n in red.bfs(inicio):
                    print("  ", n)
            elif opcion == "6":
                inicio = pedir_texto("Estudiante inicial: ")
                print("Recorrido DFS:")
                for n in red.dfs(inicio):
                    print("  ", n)
            elif opcion == "7":
                if not red.adyacencia:
                    print("No hay estudiantes registrados.")
                for nombre, cant in red.contar_amigos().items():
                    print(f"  {nombre}: {cant} amigo(s)")
            elif opcion == "8":
                a = pedir_texto("Origen: ")
                b = pedir_texto("Destino: ")
                camino = red.ruta(a, b)
                if camino:
                    print("Ruta: " + " → ".join(camino))
                else:
                    print("No existe ruta entre esos estudiantes.")
            elif opcion == "9":
                cargar_ejemplo(red)
                print("Datos de ejemplo cargados.")
            elif opcion == "10":
                ejecutar_pruebas()
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError as error:
            print("Error:", error)


# ======================================================================
# Casos de prueba (5 requeridos)
# ======================================================================
def ejecutar_pruebas():
    print("\n===== CASOS DE PRUEBA =====")

    # Caso 1 - Funcionamiento normal
    red = RedSocial()
    cargar_ejemplo(red)
    assert red.amigos_de("Carlos") == ["Ana", "Pedro", "María"]
    print("Caso 1 OK - Amigos de Carlos:", red.amigos_de("Carlos"))
    print("         BFS desde Ana:", red.bfs("Ana"))
    print("         DFS desde Ana:", red.dfs("Ana"))
    print("         Conteo:", red.contar_amigos())

    # Caso 2 - Búsqueda exitosa (amigos directos y ruta existente)
    assert red.son_amigos("Ana", "Carlos") is True
    assert red.ruta("Ana", "Pedro") == ["Ana", "Carlos", "Pedro"]
    print("Caso 2 OK - Ana y Carlos son amigos; ruta Ana→Pedro:",
          " → ".join(red.ruta("Ana", "Pedro")))

    # Caso 3 - Búsqueda fallida (estudiante inexistente / no amigos / sin ruta)
    assert red.son_amigos("Ana", "Pedro") is False
    try:
        red.amigos_de("Zoe")
        assert False, "Debió lanzar error"
    except ValueError as e:
        print("Caso 3 OK - Ana y Pedro no son amigos directos; consulta 'Zoe':", e)
    red.registrar_estudiante("Sofia")  # sin amigos -> sin ruta
    assert red.ruta("Ana", "Sofia") == []
    print("         Ruta Ana→Sofia (aislada): sin ruta")

    # Caso 4 - Estructura vacía
    vacia = RedSocial()
    assert vacia.contar_amigos() == {}
    try:
        vacia.bfs("Ana")
        assert False, "Debió lanzar error"
    except ValueError as e:
        print("Caso 4 OK - Red vacía: conteo = {}, BFS ->", e)

    # Caso 5 - Caso límite (grafo con un solo vértice + amistad consigo mismo)
    uno = RedSocial()
    uno.registrar_estudiante("Ana")
    assert uno.bfs("Ana") == ["Ana"]
    assert uno.dfs("Ana") == ["Ana"]
    try:
        uno.crear_amistad("Ana", "Ana")
        assert False, "Debió lanzar error"
    except ValueError as e:
        print("Caso 5 OK - Un solo vértice: BFS = DFS = ['Ana']; autoamistad ->", e)

    print("\nTodos los casos de prueba pasaron correctamente.")


if __name__ == "__main__":
    menu()