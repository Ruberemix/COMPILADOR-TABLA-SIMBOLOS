#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>

// ─────────────────────────────────────────────
//  CLASE: TABLA DE SÍMBOLOS
// ─────────────────────────────────────────────
class TablaDeSimbolos {
public:

    // Paso 1: Estructura — vector de mapas (pila de ámbitos)
    std::vector<std::map<std::string, int>> ambitos;

    /** Constructor: crea el ámbito global automáticamente */
    TablaDeSimbolos() {
        ambitos.push_back({});  // ámbito global vacío
        std::cout << "  [Tabla] Ambito global creado." << std::endl;
    }

    // ── Entrar a un nuevo bloque ──────────────────────────────
    void entrarAmbito() {
        ambitos.push_back({});  // nuevo mapa vacío al tope
        int nivel = (int)ambitos.size() - 1;
        std::cout << "  [Ámbito " << nivel << "] Nuevo bloque abierto." << std::endl;
    }

    // ── Salir del bloque actual ───────────────────────────────
    void salirAmbito() {
        if (ambitos.size() == 1) {
            throw std::runtime_error("Error: no se puede cerrar el ámbito global.");
        }
        // Mostrar variables que se eliminan
        std::cout << "  [Ámbito " << ambitos.size()-1 << "] Bloque cerrado. "
                  << "Variables eliminadas: {";
        for (auto& par : ambitos.back()) {
            std::cout << par.first << " ";
        }
        std::cout << "}" << std::endl;

        ambitos.pop_back();  // eliminar el ámbito más interno
    }

    // ── Declarar una variable en el ámbito actual ─────────────
    void declarar(const std::string& nombre, int valor) {
        ambitos.back()[nombre] = valor;  // back() = tope del vector
        int nivel = (int)ambitos.size() - 1;
        std::cout << "  [Ámbito " << nivel << "] Declarada: "
                  << nombre << " = " << valor << std::endl;
    }

    // ── Paso 2: Buscar una variable (de adentro hacia afuera) ──
    int buscar(const std::string& nombre) {
        // Recorremos desde el último elemento (más interno) hacia el primero (global)
        for (int i = (int)ambitos.size() - 1; i >= 0; i--) {
            auto it = ambitos[i].find(nombre);
            if (it != ambitos[i].end()) {
                return it->second;  // encontrada → devuelve el valor
            }
        }
        // No encontrada en ningún ámbito → error semántico
        throw std::runtime_error(
            "Error semántico: variable '" + nombre + "' no declarada."
        );
    }

    // ── Asignar valor a variable existente ────────────────────
    void asignar(const std::string& nombre, int valor) {
        for (int i = (int)ambitos.size() - 1; i >= 0; i--) {
            auto it = ambitos[i].find(nombre);
            if (it != ambitos[i].end()) {
                it->second = valor;
                std::cout << "  Asignada: " << nombre << " = " << valor << std::endl;
                return;
            }
        }
        throw std::runtime_error(
            "Error semántico: variable '" + nombre + "' no declarada."
        );
    }

    // ── Mostrar estado completo de la tabla ───────────────────
    void mostrar() {
        std::cout << "\n  ── Estado de la Tabla de Simbolos ──" << std::endl;
        for (int i = 0; i < (int)ambitos.size(); i++) {
            std::string etiqueta = (i == 0) ? "global" : "bloque " + std::to_string(i);
            std::cout << "  Ámbito " << i << " (" << etiqueta << "): {";
            for (auto& par : ambitos[i]) {
                std::cout << par.first << "=" << par.second << " ";
            }
            std::cout << "}" << std::endl;
        }
        std::cout << std::endl;
    }
};


// ─────────────────────────────────────────────
//  FUNCIÓN MAIN — SIMULACIÓN
// ─────────────────────────────────────────────
int main() {
    std::cout << std::string(55, '=') << std::endl;
    std::cout << "  SIMULACIÓN DE ÁMBITOS ANIDADOS — C++" << std::endl;
    std::cout << std::string(55, '=') << std::endl;

    TablaDeSimbolos tabla;

    // ── Ámbito global ──────────────────────────────────────────
    std::cout << "\n--- Ámbito Global ---" << std::endl;
    tabla.declarar("a", 10);
    tabla.declarar("b", 20);
    tabla.mostrar();

    // ── Entramos al bloque interno ─────────────────────────────
    std::cout << "--- Entrando al bloque interno ---" << std::endl;
    tabla.entrarAmbito();
    tabla.declarar("a", 99);  // 'a' local tapa a la 'a' global
    tabla.declarar("c", 5);   // 'c' solo vive en este bloque
    tabla.mostrar();

    std::cout << "  Dentro del bloque:" << std::endl;
    std::cout << "  a = " << tabla.buscar("a") << std::endl;  // → 99
    std::cout << "  b = " << tabla.buscar("b") << std::endl;  // → 20
    std::cout << "  c = " << tabla.buscar("c") << std::endl;  // → 5

    // ── Salimos del bloque interno ─────────────────────────────
    std::cout << "\n--- Saliendo del bloque interno ---" << std::endl;
    tabla.salirAmbito();
    tabla.mostrar();

    std::cout << "  Después del bloque:" << std::endl;
    std::cout << "  a = " << tabla.buscar("a") << std::endl;  // → 10 (global)

    try {
        std::cout << "  c = " << tabla.buscar("c") << std::endl;  // → ERROR
    } catch (const std::runtime_error& e) {
        std::cout << "  " << e.what() << std::endl;
    }

    std::cout << "\n" << std::string(55, '=') << std::endl;

    system("pause");
    return 0;
}
