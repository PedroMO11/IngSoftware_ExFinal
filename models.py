from datetime import date
import json


class Operacion:
    def __init__(self, numero_origen, nombre_origen, numero_destino, nombre_destino, fecha, valor):
        self.numero_destino = numero_destino
        self.numero_origen = numero_origen
        self.nombre_origen = nombre_origen
        self.nombre_destino = nombre_destino
        self.fecha = fecha
        self.valor = valor


class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos, operaciones):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = operaciones

    def historial(self):
        response = {"nombre": self.nombre,
                    "saldo": self.saldo}
        response["pagos_recibidos"] = [
            {"origen": pago.nombre_origen,
             "monto": pago.valor} for pago in self.operaciones if pago.numero_destino == self.numero
        ]
        response["pagos_enviados"] = [
            {"destino": pago.nombre_destino,
             "monto": pago.valor} for pago in self.operaciones if pago.numero_origen == self.numero
        ]

        return json.dumps(response)

    def pagar(self, destino, nombre_destino, valor):
        # Validar que este en la lista de contactos y haya saldo suficiente
        if destino in self.contactos and int(valor) <= self.saldo:
            fecha_actual = date.today()
            self.operaciones.append(Operacion(self.numero, self.nombre, destino, nombre_destino, fecha_actual, int(valor)))
            self.saldo -= int(valor)
            return "Realizado el {}".format(fecha_actual)
        else:
            if int(valor) > self.saldo:
                return "SI" #Saldo Insuficiente
            else:
                return "NE" #Numero no encontrado en lista de contactos
