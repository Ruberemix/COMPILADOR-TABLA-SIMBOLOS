"""

  ACTIVIDAD 2 — FASE DE SÍNTESIS
  Tabla de Símbolos con Ámbitos Anidados
  Curso: Compiladores | Ingeniería de Sistemas
  Lenguaje: Python 3.x


CONCEPTO CLAVE:
  Un ámbito (scope) es una región del programa donde una variable
  existe y es visible. Cuando entramos a un bloque (if, función, etc.)
  creamos un ámbito nuevo. Al salir, ese ámbito desaparece y la
  variable externa "recupera" su valor.

ESTRUCTURA:
  self.ambitos = [ {ámbito_global}, {ámbito_1}, {ámbito_2}, ... ]
  La lista actúa como una PILA: el último elemento es el más interno.
"""

#  CLASE: TABLA DE SÍMBOLOS
class TablaDeSimbolos:
    """
    Gestiona variables en múltiples ámbitos usando una pila de diccionarios.

    Analogía: es como una pila de cajones.
    - El cajón de abajo = ámbito global (siempre existe).
    - Cada cajón nuevo encima = un bloque nuevo (if, función, etc.).
    - Buscamos siempre desde el cajón de arriba hacia abajo.
    """

    def __init__(self):
        # La pila comienza con UN diccionario vacío: el ámbito global
        self.ambitos = [{}]
        print("  [TablaDeSimbolos] Ámbito global creado.")

    # ── Paso 1: Entrar a un nuevo bloque ──────────────────────────
    def entrar_ambito(self):
        """
        Abre un nuevo ámbito interno (como entrar a un bloque { }).
        Se añade un diccionario vacío al tope de la pila.
        """
        self.ambitos.append({})
        nivel = len(self.ambitos) - 1
        print(f"  [Ámbito {nivel}] Nuevo bloque abierto.")

    # ── Paso 2: Salir del bloque actual ───────────────────────────
    def salir_ambito(self):
        """
        Cierra el ámbito más interno (como salir de un bloque { }).
        Se elimina el diccionario del tope de la pila.
        """
        if len(self.ambitos) == 1:
            raise RuntimeError("Error: no se puede cerrar el ámbito global.")
        cerrado = self.ambitos.pop()
        nivel = len(self.ambitos)
        print(f"  [Ámbito {nivel}] Bloque cerrado. Variables eliminadas: {list(cerrado.keys())}")

    # ── Paso 3: Declarar una variable ────────────────────────────
    def declarar(self, nombre, valor):
        """
        Declara una variable en el ámbito ACTUAL (el más interno).
        Si ya existe en este mismo ámbito, la sobreescribe.

        Entrada: nombre (str), valor (int)
        """
        self.ambitos[-1][nombre] = valor
        nivel = len(self.ambitos) - 1
        print(f"  [Ámbito {nivel}] Declarada: {nombre} = {valor}")

    # ── Paso 4: Buscar una variable ───────────────────────────────
    def buscar(self, nombre):
        """
        Busca una variable recorriendo la pila desde el tope
        (ámbito más interno) hacia la base (ámbito global).

        Si la encuentra → devuelve su valor.
        Si no la encuentra en ningún ámbito → error semántico.

        Esta es la lógica de 'shadowing': una variable interna
        tapa a la externa con el mismo nombre.
        """
        # Recorremos de derecha a izquierda (del más interno al global)
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]

        # Si llegamos aquí, la variable no existe en ningún ámbito
        raise NameError(f"Error semántico: variable '{nombre}' no declarada.")

    # ── Paso 5: Asignar valor a una variable existente ────────────
    def asignar(self, nombre, valor):
        """
        Modifica el valor de una variable YA EXISTENTE.
        La busca en la pila (de adentro hacia afuera) y actualiza
        el primer ámbito donde la encuentre.
        """
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                ambito[nombre] = valor
                print(f"  Asignada: {nombre} = {valor}")
                return

        raise NameError(f"Error semántico: variable '{nombre}' no declarada.")

    # ── Extra: Mostrar el estado completo de la tabla ─────────────
    def mostrar(self):
        print("\n  -- Estado de la Tabla de Simbolos --")
        for i, ambito in enumerate(self.ambitos):
            etiqueta = "global" if i == 0 else f"bloque {i}"
            print(f"  Ámbito {i} ({etiqueta}): {ambito}")
        print()


# ─────────────────────────────────────────────
#  SIMULACIÓN DEL COMPILADOR
# ─────────────────────────────────────────────
def simular_compilador():
    """
    Simula el procesamiento de este pseudocódigo:

        var a = 10        ← ámbito global
        var b = 20        ← ámbito global
        inicio_bloque     ← entramos a un bloque interno
            var a = 99    ← 'a' local TAPA a la 'a' global
            var c = 5     ← solo existe en el bloque interno
            print(a)      → debe mostrar 99  (la local)
            print(b)      → debe mostrar 20  (la global, heredada)
        fin_bloque        ← salimos, 'a' local y 'c' desaparecen
        print(a)          → debe mostrar 10  (la global recupera su valor)
        print(c)          → ERROR: 'c' ya no existe
    """

    print("=" * 55)
    print("  SIMULACIÓN DE ÁMBITOS ANIDADOS — Python")
    print("=" * 55)

    tabla = TablaDeSimbolos()

    # ── Ámbito global ──────────────────────────────────────────
    print("\n--- Ámbito Global ---")
    tabla.declarar("a", 10)
    tabla.declarar("b", 20)
    tabla.mostrar()

    # ── Entramos al bloque interno ─────────────────────────────
    print("--- Entrando al bloque interno ---")
    tabla.entrar_ambito()
    tabla.declarar("a", 99)   # Esta 'a' TAPA a la 'a' global
    tabla.declarar("c", 5)    # 'c' solo existe en este bloque
    tabla.mostrar()

    print("  Dentro del bloque:")
    print(f"  a = {tabla.buscar('a')}")   # → 99 (la local)
    print(f"  b = {tabla.buscar('b')}")   # → 20 (heredada del global)
    print(f"  c = {tabla.buscar('c')}")   # → 5

    # ── Salimos del bloque interno ─────────────────────────────
    print("\n--- Saliendo del bloque interno ---")
    tabla.salir_ambito()
    tabla.mostrar()

    print("  Después del bloque:")
    print(f"  a = {tabla.buscar('a')}")   # → 10 (la global recuperó su valor)

    try:
        print(f"  c = {tabla.buscar('c')}")  # → ERROR esperado
    except NameError as e:
        print(f"  {e}")

    print("\n" + "=" * 55)


# ─────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == '__main__':
    simular_compilador()
