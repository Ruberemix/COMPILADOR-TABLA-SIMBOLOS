# Actividad Práctica U2 — Fase de Síntesis
## Tabla de Símbolos y Manejo de Ámbitos Anidados

**Curso:** Compiladores  
**Programa:** Ingeniería de Sistemas  
**Docente:** Lucy Tatiana Polanco Aya

---

## 1. Relación de Conceptos (Prerrequisito)

Antes de programar, es fundamental entender el flujo completo:

```
Entrada          →   Proceso            →   Memoria           →   Salida (Síntesis)
─────────────────────────────────────────────────────────────────────────────────────
"var a = 5"      →   ¿declaración?      →   Tabla de          →   Resultado del
"a + b"          →   ¿operación?        →   Símbolos          →   cálculo o
                     ¿error?            →   (Diccionario)     →   error semántico
```

### ¿Qué es la Tabla de Símbolos?

La **Tabla de Símbolos** es la memoria del compilador. Guarda cada variable que el
programa declara, junto con su valor. Sin ella, el compilador no podría recordar
que `a = 10` cuando más adelante encuentre `a + 5`.

### ¿Qué es un Ámbito (Scope)?

Un **ámbito** es la región del programa donde una variable existe y es visible.
Cuando entramos a un bloque (`if`, `función`, `while`), se crea un ámbito nuevo.
Al salir, ese ámbito y sus variables desaparecen.

**Ejemplo conceptual:**
```
var a = 10          ← a existe en el ámbito GLOBAL
{                   ← abrimos un bloque nuevo
    var a = 99      ← esta 'a' TAPA a la global (shadowing)
    var c = 5       ← c solo existe AQUÍ dentro
    print(a)        → imprime 99   (usa la a local)
}                   ← cerramos el bloque: 'a' local y 'c' desaparecen
print(a)            → imprime 10   (la a global recupera su valor)
print(c)            → ERROR: c ya no existe
```

---

## 2. Desarrollo Temático: El Desafío

### Paso 1 — Definir la Estructura de la Tabla

La clave del diseño es **no usar un solo mapa**, sino una **pila de mapas**.
Cada mapa representa un ámbito. La pila permite abrir y cerrar ámbitos fácilmente.

| Lenguaje | Estructura usada |
|----------|-----------------|
| Python   | `self.ambitos = [{}]` → lista de diccionarios |
| Java     | `Stack<Map<String, Integer>> ambitos` → pila de mapas |
| C++      | `std::vector<std::map<std::string, int>> ambitos` → vector de mapas |

**Visualización de la pila de ámbitos:**
```
ANTES del bloque:          DENTRO del bloque:         DESPUÉS del bloque:

[ {a=10, b=20} ]           [ {a=10, b=20} ]           [ {a=10, b=20} ]
  ↑ ámbito global            {a=99, c=5}   ← tope       ↑ ámbito global
                             ↑ ámbito 1
```

### Paso 2 — Implementar la Lógica de Búsqueda

Para buscar una variable se recorre la pila **desde el tope (más interno)
hacia la base (global)**. Esto implementa el *shadowing*: la primera
variable que coincida con el nombre gana.

```
Buscar 'a' cuando hay dos ámbitos:

  Pila:  [ {a=10, b=20},  {a=99, c=5} ]
                           ↑ revisamos aquí primero → encontramos a=99 → retornamos 99
```

```
Buscar 'b' cuando hay dos ámbitos:

  Pila:  [ {a=10, b=20},  {a=99, c=5} ]
                           ↑ no tiene 'b' → bajamos
           ↑ encontramos b=20 → retornamos 20
```

---

## 3. Implementación en Python

```python
class TablaDeSimbolos:

    def __init__(self):
        self.ambitos = [{}]          # pila con el ámbito global vacío

    def entrar_ambito(self):
        self.ambitos.append({})      # apilar un nuevo mapa vacío

    def salir_ambito(self):
        self.ambitos.pop()           # desapilar el ámbito más interno

    def declarar(self, nombre, valor):
        self.ambitos[-1][nombre] = valor   # insertar en el ámbito actual (tope)

    def buscar(self, nombre):
        for ambito in reversed(self.ambitos):   # de adentro hacia afuera
            if nombre in ambito:
                return ambito[nombre]
        raise NameError(f"Error semántico: '{nombre}' no declarada.")
```

**Simulación y salida:**
```
[Tabla] Ámbito global creado.
[Ámbito 0] Declarada: a = 10
[Ámbito 0] Declarada: b = 20

-- Estado de la Tabla de Simbolos --
Ámbito 0 (global): {'a': 10, 'b': 20}

[Ámbito 1] Nuevo bloque abierto.
[Ámbito 1] Declarada: a = 99
[Ámbito 1] Declarada: c = 5

-- Estado de la Tabla de Simbolos --
Ámbito 0 (global): {'a': 10, 'b': 20}
Ámbito 1 (bloque 1): {'a': 99, 'c': 5}

Dentro del bloque:
  a = 99   ← usa la 'a' local (shadowing)
  b = 20   ← hereda del ámbito global
  c = 5

[Ámbito 1] Bloque cerrado. Variables eliminadas: ['a', 'c']

-- Estado de la Tabla de Simbolos --
Ámbito 0 (global): {'a': 10, 'b': 20}

Después del bloque:
  a = 10   ← la 'a' global recuperó su valor
  Error semántico: variable 'c' no declarada.
```

---

## 4. Implementación en Java

```java
import java.util.Stack;
import java.util.Map;
import java.util.HashMap;

class Tabla {
    Stack<Map<String, Integer>> ambitos = new Stack<>();

    Tabla() {
        ambitos.push(new HashMap<>());  // ámbito global
    }

    void entrarAmbito() { ambitos.push(new HashMap<>()); }
    void salirAmbito()  { ambitos.pop(); }

    void declarar(String nombre, int valor) {
        ambitos.peek().put(nombre, valor);   // peek = tope sin sacar
    }

    int buscar(String nombre) {
        for (int i = ambitos.size() - 1; i >= 0; i--) {
            if (ambitos.get(i).containsKey(nombre))
                return ambitos.get(i).get(nombre);
        }
        throw new RuntimeException("Error semántico: '" + nombre + "' no declarada.");
    }
}
```

**Salida esperada:**
```
Ámbito 0 (global): {a=10, b=20}
Ámbito 1 (bloque 1): {a=99, c=5}

Dentro del bloque:
  a = 99
  b = 20
  c = 5

Después del bloque:
  a = 10
  Error semántico: 'c' no declarada.
```

---

## 5. Implementación en C++

```cpp
#include <vector>
#include <map>
#include <string>
#include <stdexcept>

class TablaDeSimbolos {
public:
    std::vector<std::map<std::string, int>> ambitos;

    TablaDeSimbolos() { ambitos.push_back({}); }

    void entrarAmbito() { ambitos.push_back({}); }
    void salirAmbito()  { ambitos.pop_back(); }

    void declarar(const std::string& nombre, int valor) {
        ambitos.back()[nombre] = valor;   // back() = último elemento
    }

    int buscar(const std::string& nombre) {
        for (int i = ambitos.size()-1; i >= 0; i--) {
            auto it = ambitos[i].find(nombre);
            if (it != ambitos[i].end()) return it->second;
        }
        throw std::runtime_error("Error semántico: '" + nombre + "' no declarada.");
    }
};
```

**Compilar y ejecutar:**
```bash
g++ -std=c++11 -o tabla tabla_simbolos.cpp
./tabla
```

**Salida esperada:**
```
Ámbito 0 (global): {a=10 b=20}
Ámbito 1 (bloque 1): {a=99 c=5}

Dentro del bloque:
  a = 99
  b = 20
  c = 5

Después del bloque:
  a = 10
  Error semántico: 'c' no declarada.
```

---

## 6. Tabla Comparativa de Implementaciones

| Característica | Python | Java | C++ |
|---|---|---|---|
| Estructura de pila | `list` con `append/pop` | `Stack<Map<>>` | `vector<map<>>` |
| Añadir ámbito | `append({})` | `push(new HashMap())` | `push_back({})` |
| Eliminar ámbito | `pop()` | `pop()` | `pop_back()` |
| Leer tope | `[-1]` | `peek()` | `back()` |
| Recorrer de interno a global | `reversed(self.ambitos)` | `for i = size-1; i>=0; i--` | `for i = size-1; i>=0; i--` |
| Error semántico | `raise NameError(...)` | `throw RuntimeException(...)` | `throw runtime_error(...)` |

---

## 7. Casos de Prueba

| Operación | Pila de ámbitos | Resultado esperado |
|---|---|---|
| `declarar("a", 10)` | `[{a:10}]` | a=10 en global |
| `entrar_ambito()` | `[{a:10}, {}]` | nuevo bloque abierto |
| `declarar("a", 99)` | `[{a:10}, {a:99}]` | a=99 en bloque interno |
| `buscar("a")` | `[{a:10}, {a:99}]` | **99** (shadowing) |
| `buscar("b")` | `[{a:10,b:20}, {a:99}]` | **20** (hereda global) |
| `salir_ambito()` | `[{a:10,b:20}]` | bloque cerrado |
| `buscar("a")` | `[{a:10,b:20}]` | **10** (global recuperada) |
| `buscar("c")` | `[{a:10,b:20}]` | **ERROR semántico** |

---

## 8. Conclusiones

1. **La Tabla de Símbolos es la memoria del compilador.** Sin ella no es posible
   mantener el estado de las variables entre instrucciones.

2. **Una pila de mapas es la estructura idónea.** Permite crear y destruir ámbitos
   en tiempo constante (O(1)) simplemente apilando o desapilando un mapa.

3. **El shadowing es un comportamiento natural.** Al buscar siempre desde el ámbito
   más interno, una variable local automáticamente tapa a una externa con el mismo
   nombre, sin necesidad de lógica adicional.

4. **El error semántico es diferente al sintáctico.** Usar una variable no declarada
   (`c` fuera de su bloque) no es un error de escritura sino de significado.
   Detectarlo requiere la Tabla de Símbolos, no el Parser.

5. **Los tres lenguajes comparten el mismo algoritmo.** La diferencia es solo
   sintáctica. La lógica de pila es universal.

---

## 9. Archivos del Proyecto

| Archivo | Descripción |
|---|---|
| `tabla_simbolos.py` | Implementación completa en Python |
| `TablaSimbolos.java` | Implementación completa en Java |
| `tabla_simbolos.cpp` | Implementación completa en C++ |
| `ACTIVIDAD2_COMPILADORES.md` | Este documento académico |

---

*Actividad Práctica U2 — Curso Compiladores — Ingeniería de Sistemas*
