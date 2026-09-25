import unittest
from gestor_recaudo import GestorRecaudoDAO

class TestControlCalidadColibri(unittest.TestCase):

    def test_escenario_1_registro_exitoso_efectivo(self):
        """Valida que un cliente registrado y monto válido pasen con éxito"""
        recaudo = GestorRecaudoDAO(
            id_transaccion=101, 
            id_empleado_cajero=77, 
            identificacion_cliente="12345", 
            monto_aporte=850000.0
        )
        resultado = recaudo.ejecutar_transaccion_atomica()
        self.assertTrue(resultado)
        self.assertEqual(recaudo.obtener_estado(), "Exitosa")
        self.assertIn("IMPRIMIENDO RECIBO", recaudo.enviar_datos_impresion())

    def test_escenario_2_cliente_no_registrado(self):
        """Valida que un cliente no registrado sea bloqueado por seguridad"""
        recaudo_invalido = GestorRecaudoDAO(
            id_transaccion=102, 
            id_empleado_cajero=77, 
            identificacion_cliente="99999", 
            monto_aporte=50000.0
        )
        resultado = recaudo_invalido.ejecutar_transaccion_atomica()
        self.assertFalse(resultado)
        self.assertEqual(recaudo_invalido.obtener_estado(), "Transacción Rechazada: Cliente no existe")
        self.assertEqual(recaudo_invalido.enviar_datos_impresion(), "No se genera recibo: Transacción inválida")

if __name__ == '__main__':
    unittest.main()
