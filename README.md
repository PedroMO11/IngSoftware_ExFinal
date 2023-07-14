# Pregunta 3

Para que el software soporte un valor máximo de transferencia de 200 soles al día por cada usuario, se debería agregar un atributo a la clase Cuenta que tenga como valor fijo 200, de modo que se vaya restando cada que se realice una operación. Se tendría que realizar una validación adicional con este nuevo campo parecido a como se hace con el saldo de la cuenta.

Los nuevos casos de prueba serían los siguientes:
- Intentar realizar un pago de más de 200 (No debería permitir)
- Realizar un pago con un monto menor al saldo de una cuenta y luego realizar otro pago que sumándolo con el anterior pago de más de 200 (No debería permitirlo).
- Realizar un pago con un monto menor al saldo de una cuenta y luego realizar otro pago que sumándolo con el anterior pago de exactamente 200 (Debería permitirlo).
- Realizar un pago con un monto menor al saldo de una cuenta y luego realizar otro pago que sumándolo con el anterior pago de menos de 200 (Debería permitirlo).

Hay poco riesgo de romper lo que ya funciona puesto que es un cambio pequeño y solo debería agregarse una validación adicional. De igual forma se debe corroborar el funcionamiento de la aplicación con las nuevas pruebas unitarias.