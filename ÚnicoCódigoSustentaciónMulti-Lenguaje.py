import json
import time
from abc import ABC, abstractmethod

# =====================================================================
# 🏛️ 1. CAPA DE SERVICIO CENTRALIZADA: PATRÓN FACADE (Fachada de Red)
# =====================================================================
class ServidorCentralFacade:
    """
    Esta clase actúa como un Punto de Acceso Unificado (Fachada). 
    Encapsula la complejidad del protocolo de red e interactúa con el 
    Backend Central en C++ de la Fase 2.
    """
    @staticmethod
    def enviar_al_servidor_cpp(nodo_origen, lenguaje, datos_json):
        """
        Simula la comunicación de red (Sockets/HTTP) desde el nodo nativo
        hacia tu Backend Centralizado en C++ (Fase Práctica 2).
        """
        print(f"\n📡 [RED - FACADE] Enviando paquete desde Nodo {nodo_origen} ({lenguaje})...")
        print(f"📦 Paquete JSON transmitido: {json.dumps(datos_json, indent=2)}")
        print("⏳ Procesando en Servidor C++ bajo RNF-1 (<60s)...")
        time.sleep(1.0)
        
        # Respuesta simulada del servidor en C++ de la Fase 2
        respuesta_servidor = {
            "status": 200,
            "msg": "SUCCESS!!!",
            "timestamp": "2026-11-20T14:30:00Z",
            "autorizado": True
        }
        print(f"📥 [RESPUESTA SERVIDOR C++] -> {respuesta_servidor['msg']} (Código {respuesta_servidor['status']})")
        return respuesta_servidor


# =====================================================================
# 🧩 2. CAPA DE CANALES COGNITIVOS: PATRÓN STRATEGY (Estrategias de Canal)
# =====================================================================
class CanalEstrategiaInterface(ABC):
    """
    Interfaz abstracta del Patrón Strategy. Define un contrato común 
    para que todos los nodos físicos ejecuten su interfaz de forma polimórfica.
    """
    @abstractmethod
    def simular_nodo(self):
        pass


class ATMCppStrategy(CanalEstrategiaInterface):
    """ DEMOSTRACIÓN NODO ATM: ESCRITO EN C++ (Windows IoT) """
    def simular_nodo(self):
        print("\n" + "="*60)
        print("🏧 SIMULANDO: NODO ATM (Nautilus Hyosung Halo II)")
        print("💻 LENGUAJE NATIVO DEL NODO: C++ (Compilado para Windows IoT)")
        print("="*60)
        
        # [Interfaz 1] Autenticación básica
        print("[Interfaz 1] Hello! I'm Colibrí Sabe. Ask me.")
        password = input("PASSWORD (8 caracteres): ")
        if len(password) != 8:
            print("❌ C++ Exception: Longitud inválida. Acceso negado.")
            return

        # [Interfaz 2] Datos de cliente y códigos de acceso
        print("\n[Interfaz 2] TELL ME!")
        user = input("USER NAME: ")
        cedula = input("IDENTIFICATION (# cédula): ")
        code1 = input("ACCESS CODE 1: ")
        code2 = input("ACCESS CODE 2: ")  # 🛠️ CORREGIDO: Se limpió la comilla inclinada corrupta
        
        payload_cpp = {
            "canal": "ATM",
            "operacion": "auth_3_capas",
            "cedula": cedula,
            "token_verificacion": code1 + code2
        }
        
        res = ServidorCentralFacade.enviar_al_servidor_cpp("ATM_01", "C++ Nativo", payload_cpp)
        
        if res["autorizado"]:
            # [Interfaz 3] Menú Principal e ingreso de montos de retiro
            print("\n[Interfaz 3] ENTER ATM CODE!")
            monto_retiro = int(input("WITHDRAW MONEY (Ingresar números enteros): $"))
            
            tx_payload = {"canal": "ATM", "operacion": "retiro", "monto": monto_retiro, "cedula": cedula}
            res_tx = ServidorCentralFacade.enviar_al_servidor_cpp("ATM_01", "C++ Nativo", tx_payload)
            
            # [Interfaz 4] Sección de depósito (Deposit Money)
            print("\n[Interfaz 4] DEPOSIT SECTION!")
            monto_deposito = int(input("DEPOSIT MONEY (Ingresar números enteros positivos): $"))
            if monto_deposito <= 0:
                print("❌ Transacción negada: El monto debe ser un entero positivo.")
                return
                
            dep_payload = {"canal": "ATM", "operacion": "deposito", "monto": monto_deposito, "cedula": cedula}
            ServidorCentralFacade.enviar_al_servidor_cpp("ATM_01", "C++ Nativo", dep_payload)
            print("\n🎉 [Interfaz 4 - SALIDA] THANK YOU!!! Transacción de depósito recibida.")

            # [Interfaz 5] Pantalla Final de éxito del Retiro solicitado en la Interfaz 3
            if res_tx["autorizado"]:
                print("\n🎉 [Interfaz 5] ¡SUCCESSES!!!")
                print(f"💰 Retiro autorizado y dispensado por: ${monto_retiro} COP.")
                print("💵 Por favor retire su dinero del dispositivo físico.")
                print("⏳ Saliendo de la interfaz de usuario de forma segura (Timeout < 1 min)...")
                time.sleep(1.0)


class CashRegisterCSharpStrategy(CanalEstrategiaInterface):
    """ DEMOSTRACIÓN NODO CASH REGISTER: ESCRITO EN C# (Windows POS) """
    def simular_nodo(self):
        print("\n" + "="*60)
        print("🛒 SIMULANDO: NODO CASH REGISTER (Posiflex)")
        print("💻 LENGUAJE NATIVO DEL NODO: C# con .NET (Ecosistema Windows POS)")
        print("="*60)
        
        # [Interfaz 1] Login de Cajero
        print("[Interfaz 1] PASSWORD LOGIN!")
        pass_cr = input("PASSWORD (8 caracteres): ")
        
    if len(pass_cr) != 8:
                print("❌ C# Object Error: Auth failed.")
                return
                
                # [Interfaz 2] Recaudo / Depósito de Inversionistas
                print("\n[Interfaz 2] ENTER CASHIER CODE!")
                cashier = input("CASHIER CODE: ")
                monto_deposito = int(input("DEPOSIT MONEY (Aporte de Inversionista): $"))
            
                payload_cs = {
                    "canal": "CashRegister",
                    "operacion": "recaudo_oficina",
                    "cajero_id": cashier,
                    "monto": monto_deposito
                }
                
                res = ServidorCentralFacade.enviar_al_servidor_cpp("CR_OFI_CENTRAL", "C# / .NET", payload_cs)
                if res["autorizado"]:
                    print("\n🎉 [Interfaz 3] ¡THANK YOU!!!")
                    print("🧾 [DIAN] Enviando comando a Impresora Fiscal Homologada en Colombia.")
                    
                # [Interfaz 4] Retiro de Intereses de Socios (Withdraw Money)
                print("\n[Interfaz 4] WITHDRAW SECTION (Retiro de Intereses de Socios)!")
                cedula_socio = input("ENTER INVESTOR ID (Cédula del socio): ")
                monto_retiro = int(input("WITHDRAW MONEY (Monto de retiro de intereses): $"))
                
                withdraw_payload = {
                    "canal": "CashRegister",
                    "operacion": "retiro_intereses_oficina",
                    "cajero_id": cashier,
                    "cedula_socio": cedula_socio,
                    "monto": monto_retiro
                }
            
                res_withdraw = ServidorCentralFacade.enviar_al_servidor_cpp("CR_OFI_CENTRAL", "C# / .NET", withdraw_payload)
                if res_withdraw["autorizado"]:
                    print("\n🎉 [Interfaz 4 - SALIDA] ¡SUCCESSES!!! Entregar efectivo al socio.")
                    print("🧾 [DIAN] Imprimiendo comprobante fiscal de retiro de intereses.")


class PortalWebJSStrategy(CanalEstrategiaInterface):
    """ DEMOSTRACIÓN NODO PORTAL WEB PC: JAVASCRIPT / REACT """
    def simular_nodo(self):
        print("\n" + "="*60)
        print("🌐 SIMULANDO: PORTAL WEB PC (Navegador Chrome/Edge)")
        print("💻 TECNOLOGÍA DEL FRONTEND: JavaScript / React.js + Bootstrap")
        print("="*60)
        
        print("[Interfaz 1] WELCOME! ACCESS!!!")
        print("[Interfaz 2] 1. ¿Qué es COLIBRÍ SABE? | 2. INGRESO SOCIOS")
        input("Click en INGRESO SOCIOS (Presione Enter)...")
        
        print("\n[Interfaz 3] Membership Admission")
        password = input("Password (8 caracteres): ")
        
        payload_js = {
            "canal": "Web_PC",
            "operacion": "login_web",
            "session_token": "JWT_REACT_GENERATED_9921"
        }
        
        res = ServidorCentralFacade.enviar_al_servidor_cpp("Web_Browser_PC", "JavaScript / Fetch API", payload_js)
        if res["autorizado"]:
            # 🛠️ CORREGIDO: Se resolvió el salto de línea ilegal que rompía el string literal
            print("\n[Interfaz 4] Welcome to Colibrí Sabe Investor Dashboard")
            print("💰 ACCOUNT BALANCE: $35.000.000 COP")
            print("\n[Interfaz 5] Redireccionando a modulo de transferencias...")
            print("Monto a Transferir: $12.000.000 | Origen: Banco Occidente -> Destino: Banco de Bogotá")


class AppMovilKotlinStrategy(CanalEstrategiaInterface):
    """ DEMOSTRACIÓN NODO MÓVIL: KOTLIN (App Nativa Android) """
    def simular_nodo(self):
        print("\n" + "="*60)
        print("📱 SIMULANDO: APLICACIÓN MÓVIL")
        print("💻 LENGUAJE NATIVO DEL NODO: Kotlin (Android SDK)")
        print("="*60)
        
        print("[Interfaz 1] HELLO!!! Enter Colibrí Sabe!!!")
        password = input("Password (8 caracteres): ")
        
        payload_kotlin = {
            "canal": "Mobile_Android",
            "operacion": "biometric_jwt_auth",
            "hardware_id": "ARM64_DEVICE_SAMSUNG"
        }
        
        res = ServidorCentralFacade.enviar_al_servidor_cpp("Android_App", "Kotlin / Retrofit Client", payload_kotlin)
        if res["autorizado"]:
            print("\n[Interfaz 2] ACCOUNT BALANCE: $42.000.000 COP")
            print("\n[Interfaz 3] TRANSACTIONS -> Successful transaction")
            print("📦 Comprobante digital encriptado localmente con Android Keystore.")


# =====================================================================
# 🎮 3. CONTEXTO DE EJECUCIÓN (Orquestador Principal)
# =====================================================================
# 🛠️ CORREGIDO: Bloque final del Contexto y Menú de Pruebas totalmente reconstruido
class EcosistemaColibriContext:
    """
    Esta clase maneja el Contexto del Patrón Strategy. 
    Se encarga de configurar y despachar dinámicamente el nodo seleccionado.
    """
