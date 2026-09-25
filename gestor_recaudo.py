class GestorRecaudoDAO:
    def __init__(self, id_transaccion: int, id_empleado_cajero: int, identificacion_cliente: str, monto_aporte: float):
        self.__id_transaccion = id_transaccion
        self.__id_empleado_cajero = id_empleado_cajero
        self.__identificacion_cliente = identificacion_cliente
        self.__monto_aporte = monto_aporte
        self.__estado_transaccion = "Pendiente"
        self.__clientes_registrados = ["12345", "67890", "98765"]

    def validar_datos_integridad(self) -> bool:
        if self.__identificacion_cliente in self.__clientes_registrados:
            return True
        return False

    def ejecutar_transaccion_atomica(self) -> bool:
        if not self.validar_datos_integridad():
            self.__estado_transaccion = "Transacción Rechazada: Cliente no existe"
            return False
        if self.__monto_aporte <= 0:
            self.__estado_transaccion = "Transacción Rechazada: Monto inválido"
            return False
        self.__estado_transaccion = "Exitosa"
        return True

    def enviar_datos_impresion(self) -> str:
        if self.__estado_transaccion == "Exitosa":
            return f"IMPRIMIENDO RECIBO... Transacción {self.__id_transaccion} por ${self.__monto_aporte:.2f}"
        return "No se genera recibo: Transacción inválida"

    def obtener_estado(self) -> str:
        return self.__estado_transaccion
