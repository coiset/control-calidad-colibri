#include <iostream>
#include <string>
#include <memory>
#include <map>
#include <vector>

// =====================================================================
// 📦 MODELOS DE DATOS (Estructuras Base del Dominio)
// =====================================================================
struct Client {
    int id;
    std::string cedula;
    std::string nombre;
};

struct Account {
    int id;
    int clientId;
    double balance;
    double interestAccumulated;
};

struct Transaction {
    int accountId;
    std::string tipo;
    double monto;
    std::string canal;
};

// =====================================================================
// 🗄️ CAPA DE PERSISTENCIA SIMULADA: SIMULACIÓN DEL TRANSACTION_DAO
// =====================================================================
class TransactionDAO {
private:
    std::map<std::string, Client> clientes;
    std::map<int, Account> cuentas;
    std::vector<Transaction> historial;

public:
    TransactionDAO() {
        // Inicialización de datos de prueba para el simulador
        clientes[1010] = {1, "10203040", "Amalia Castro"};
        cuentas[555] = {555, 1, 1000000.0, 0.0}; // Cuenta 555 con saldo inicial de $1'000.000 COP
    }

    Client* obtenerClientePorCedula(const std::string& cedula) {
        for (auto& pair : clientes) {
            if (pair.second.cedula == cedula) {
                return &(pair.second);
            }
        }
        return nullptr;
    }

    Account* obtenerCuenta(int numCuenta) {
        if (cuentas.find(numCuenta) != cuentas.end()) {
            return &cuentas[numCuenta];
        }
        return nullptr;
    }

    void guardarTransaccion(int numCuenta, std::string tipo, double monto, std::string canal) {
        historial.push_back({numCuenta, tipo, monto, canal});
        std::cout << "💾 [DAO] Transacción guardada en auditoría: " << tipo 
                  << " por $" << monto << " COP vía " << canal << std::endl;
    }
};

// =====================================================================
// 🏢 CAPA DE ARQUITECTURA: INTERFAZ BASE PARA EL PATRÓN COMMAND
// =====================================================================
class IComandoFinanciero {
public:
    virtual ~IComandoFinanciero() = default;
    // Método de ejecución que retorna la respuesta en formato JSON estructurado
    virtual std::string ejecutar() = 0;
};

// =====================================================================
// 🧩 COMANDOS CONCRETOS (Desacoplan la lógica del negocio)
// =====================================================================

// Comando 1: Operación de Recaudo Eficiente (RO3)
class ComandoRecaudo : public IComandoFinanciero {
private:
    TransactionDAO& dao;
    std::string cedula;
    int numCuenta;
    double monto;
    std::string canal;

public:
    ComandoRecaudo(TransactionDAO& daoData, std::string c, int cuenta, double m, std::string can)
        : dao(daoData), cedula(c), numCuenta(cuenta), monto(m), canal(can) {}

    std::string ejecutar() override {
        // Validación 1: Verificar el monto mínimo
        if (monto <= 0) {
            return "{\"status\": \"error\", \"message\": \"El monto del recaudo debe ser mayor a $0 COP.\"}";
        }

        // Validación 2: Buscar que el cliente exista en la base de datos (Uso del DAO)
        Client* cliente = dao.obtenerClientePorCedula(cedula);
        if (cliente == nullptr) {
            return "{\"status\": \"error\", \"message\": \"Cliente no registrado en el Fondo Colibri.\"}";
        }

        // Validación 3: Verificar la cuenta bancaria de destino (Uso del DAO)
        Account* cuenta = dao.obtenerCuenta(numCuenta);
        if (cuenta == nullptr) {
            return "{\"status\": \"error\", \"message\": \"La cuenta especificada no existe.\"}";
        }

        // Validación de Regla de Negocio bancaria: La cuenta debe pertenecer al cliente
        if (cuenta->clientId != cliente->id) {
            return "{\"status\": \"error\", \"message\": \"Incoherencia de datos: La cuenta no pertenece al cliente ingresado.\"}";
        }

        // OPERACIÓN FINANCIERA: Modificación del saldo base en memoria
        cuenta->balance += monto;

        // PERSISTENCIA: Registrar el movimiento en el libro contable de auditoría (DAO)
        dao.guardarTransaccion(numCuenta, "Recaudo", monto, canal);

        // RETORNO: Respuesta formateada en JSON universal para el nodo solicitante
        return "{\"status\": \"success\", \"message\": \"Recaudo procesado con exito via " + canal + 
               "\", \"nuevo_saldo\": " + std::to_string(cuenta->balance) + "}";
    }
};

// Comando 2: Cierre Trimestral y cálculo ganancial del 40% (RO1)
class ComandoRendimiento : public IComandoFinanciero {
private:
    TransactionDAO& dao;
    int numCuenta;

public:
    ComandoRendimiento(TransactionDAO& daoData, int cuenta) 
        : dao(daoData), numCuenta(cuenta) {}

    std::string ejecutar() override {
        Account* cuenta = dao.obtenerCuenta(numCuenta);
        if (cuenta == nullptr) {
            return "{\"status\": \"error\", \"message\": \"Cuenta no encontrada para aplicar rendimiento.\"}";
        }

        // El fondo proyecta un 40% de ganancias sobre el saldo base de aportes
        double rendimientoCalculado = cuenta->balance * 0.40;
        cuenta->interestAccumulated += rendimientoCalculado;

        std::cout << "\n[CORE C++] Cierre trimestral ejecutado de forma automatica." << std::endl;
        return "{\"status\": \"success\", \"message\": \"Rendimiento del 40% aplicado\", \"rendimiento_generado\": " 
               + std::to_string(rendimientoCalculado) + ", \"interes_acumulado\": " 
               + std::to_string(cuenta->interestAccumulated) + "}";
    }
};

// =====================================================================
// 🏛️ CAPA DE CONTROLADOR EVOLUCIONADA (Patrón MVC + Command + Factory)
// =====================================================================
class FinancialController {
private:
    TransactionDAO& dao;

public:
    FinancialController(TransactionDAO& daoData) : dao(daoData) {}

    // Despachador centralizado: Recibe la petición del ecosistema y ejecuta el comando dinámicamente
    std::string procesarOperacion(const std::string& tipoOperacion, std::string cedula, int numCuenta, double monto, std::string canal) {
        std::unique_ptr<IComandoFinanciero> comando;

        // Factory Method en línea para la creación del objeto de negocio
        if (tipoOperacion == "Recaudo") {
            comando = std::make_unique<ComandoRecaudo>(dao, cedula, numCuenta, monto, canal);
        } 
        else if (tipoOperacion == "Rendimiento") {
            comando = std::make_unique<ComandoRendimiento>(dao, numCuenta);
        } 
        else {
            return "{\"status\": \"error\", \"message\": \"Operación financiera no soportada por el core central.\"}";
        }

        // Ejecución polimórfica del patrón comando
        return comando->ejecutar();
    }
};

// =====================================================================
# 🚀 FUNCIÓN DE PRUEBA DEL MOTOR DE LOGICA
// =====================================================================
int main() {
    
std::cout << "=== CORE CENTRAL C++ VALIDADO ===" << std::endl;
    
    // Instanciar el motor de datos y el controlador MVC
    TransactionDAO baseDeDatos;
    FinancialController controlador(baseDeDatos);

    // 1. Simulación de Entrada desde canal físico (Recaudo exitoso en Oficina/Cash Register)
    std::cout << "\n[Prueba 1] Procesando recaudo desde terminal CashRegister..." << std::endl;
    std::string jsonRespuesta1 = controlador.procesarOperacion("Recaudo", "10203040", 555, 250000.0, "CashRegister");
    std::cout << "📥 Respuesta JSON del Core: " << jsonRespuesta1 << std::endl;

    // 2. Simulación de ejecución automática (Cálculo del 40% de rendimiento proyectado)
    std::cout << "\n[Prueba 2] Ejecutando cálculo ganancial trimestral..." << std::endl;
    std::string jsonRespuesta2 = controlador.procesarOperacion("Rendimiento", "", 555, 0.0, "Sistema_Automatico");
    std::cout << "📥 Respuesta JSON del Core: " << jsonRespuesta2 << std::endl;

    return 0;
}
