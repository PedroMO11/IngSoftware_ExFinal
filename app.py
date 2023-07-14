from flask import Flask, request
from models import *

app = Flask(__name__)

bd = [Cuenta("21345", "Arnaldo", 200,  ["123", "456"], []),
      Cuenta("123", "Luisa", 400, ["456"], []),
      Cuenta("456", "Andrea", 300, ["21345"], [])
      ]


@app.route("/billetera/contactos")
def get_contactos():
    mi_numero = request.args.get("minumero")
    response = {}

    if mi_numero not in [cuenta.numero for cuenta in bd]:
        response["mensaje"] = "Usuario no existe en la BD"
        return json.dumps(response)

    response["contactos"] = []
    contactos = []

    for cuenta in bd:
        if cuenta.numero == mi_numero:
            contactos = cuenta.contactos
            break

    for contacto in contactos:
        for cuenta in bd:
            if cuenta.numero == contacto:
                response["contactos"].append({"numero": cuenta.numero,
                                              "nombre": cuenta.nombre})
                break

    return json.dumps(response)


@app.route("/billetera/pagar")
def pagar():
    mi_numero = request.args.get("minumero")
    numero_destino = request.args.get("numerodestino")
    valor = request.args.get("valor")
    nombre_destino = ""
    mi_nombre = ""
    response = {}

    if mi_numero not in [cuenta.numero for cuenta in bd]:
        response["mensaje"] = "Usuario no existe en la BD"
        return json.dumps(response)

    for cuenta in bd:
        if cuenta.numero == numero_destino:
            nombre_destino = cuenta.nombre
            break

    for cuenta in bd:
        if cuenta.numero == mi_numero:
            response["mensaje"] = cuenta.pagar(
                numero_destino, nombre_destino, valor)
            mi_nombre = cuenta.nombre
            break

    if response["mensaje"] != "SI" and response["mensaje"] != "NE":
        for cuenta in bd:
            if cuenta.numero == numero_destino:
                cuenta.operaciones.append(Operacion(
                    mi_numero, mi_nombre, numero_destino, nombre_destino, date.today(), valor))
                break

    return json.dumps(response)


@app.route("/billetera/historial")
def get_historial():
    mi_numero = request.args.get("minumero")
    response = {}

    if mi_numero not in [cuenta.numero for cuenta in bd]:
        response["mensaje"] = "Usuario no existe en la BD"
        return json.dumps(response)

    for cuenta in bd:
        if cuenta.numero == mi_numero:
            return cuenta.historial()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
