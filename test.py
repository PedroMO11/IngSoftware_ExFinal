import unittest
import json
from app import *

class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    # Casos de Exito
    def test_contactos(self):
        # Se listan los contactos que tiene actualmente en BD el numero 21345, que corresponde a Arnaldo
        # Deberia listar a Luisa y Andrea.
        response = self.app.get("/billetera/contactos?minumero=21345")
        data = {}
        data["contactos"] = [{"numero": "123", "nombre": "Luisa"}, {"numero": "456", "nombre": "Andrea"}]
        self.assertEqual(json.dumps(data), json.dumps(json.loads(response.get_data(as_text=True))))

    def test_pagar(self):
        # El numero 21345 paga al numero 123 (su contacto) el monto de 100, que es menor que el saldo que le queda, 
        # por lo que deberia ser realizado.
        response = self.app.get("/billetera/pagar?minumero=21345&numerodestino=123&valor=100")
        data = {"mensaje": "Realizado el 2023-07-13"}
        self.assertEqual(json.dumps(data), json.dumps(json.loads(response.get_data(as_text=True))))
    
    def test_pagar_2(self):
        # El numero 123 paga al numero 456 (su contacto) el monto de 400, que es menor que el saldo que le queda, 
        # por lo que deberia ser realizado.
        response = self.app.get("/billetera/pagar?minumero=123&numerodestino=456&valor=50")
        data = {"mensaje": "Realizado el 2023-07-13"}
        self.assertEqual(json.dumps(data), json.dumps(json.loads(response.get_data(as_text=True))))
    
    def test_historial(self):
        # El numero 123 paga al numero 456 (su contacto) el monto de 400, que es menor que el saldo que le queda, 
        # por lo que deberia ser realizado.
        response = self.app.get("/billetera/pagar?minumero=123&numerodestino=456&valor=50")
        data = {"mensaje": "Realizado el 2023-07-13"}
        self.assertEqual(json.dumps(data), json.dumps(json.loads(response.get_data(as_text=True))))

        # El numero 123 ahora deberia tener un saldo de 350 y tener registrada una operacion de envio el pago al numero 456 (Andrea) 
        # por el monto de 50.
        response = self.app.get("/billetera/historial?minumero=123")
        data = {}
        data["nombre"] = "Luisa"
        data["saldo"] = 350
        data["pagos_recibidos"] = []
        data["pagos_enviados"] = [{"destino": "Andrea", "monto": 50}]
        self.assertEqual(json.dumps(data), json.dumps(json.loads(response.get_data(as_text=True))))

    # Casos de Error
    def test_numero_no_registrado_bd(self):
        # El numero 999 no esta registrado en BD, por lo que no deberia listar ningun contacto.
        response = self.app.get("/billetera/contactos?minumero=999")
        data = {}
        data["mensaje"] = "Usuario no existe en la BD"
        self.assertEqual(json.dumps(data), json.dumps(json.loads(response.get_data(as_text=True))))

    def test_saldo_insuficiente(self):
        # El numero 21345 tiene un saldo de 200, por lo que al intentar hacer un pago de 300, no deberia permitirlo.
        response = self.app.get("/billetera/pagar?minumero=21345&numerodestino=123&valor=300")
        data = {"mensaje": "SI"} # SI: Saldo Insuficiente
        self.assertEqual(json.dumps(data), json.dumps(json.loads(response.get_data(as_text=True))))

    def test_numero_no_contacto(self):
        # El numero 123 no tiene como contacto al numero 21345, por lo que tampoco deberia permitir realizar un pago.
        response = self.app.get("/billetera/pagar?minumero=123&numerodestino=21345&valor=300")
        data = {"mensaje": "NE"} # NE: Numero no encontrado en contactos
        self.assertEqual(json.dumps(data), json.dumps(json.loads(response.get_data(as_text=True))))


if __name__ == '__main__':
    unittest.main()

