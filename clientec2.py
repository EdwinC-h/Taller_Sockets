import socket

# Configuración del socket del cliente
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
direccion_servidor = ("localhost", 5000)

# Mensaje inicial para saludar al servidor y arrancar el cuestionario
mensaje_inicial = "Hola soy el cliente"
socket_cliente.sendto(mensaje_inicial.encode(), direccion_servidor)

try:
    while True:
        # Recibir la pregunta o el resultado final del servidor
        data, direccion = socket_cliente.recvfrom(1024)
        mensaje = data.decode()
        
        # Mostrar el mensaje recibido (pregunta, evaluación o resultado final)
        print("\n" + mensaje)
        
        # Si el servidor indica que el cuestionario finalizó, rompemos el bucle
        if "=== CUESTIONARIO FINALIZADO ===" in mensaje:
            break
            
        # Pedir la respuesta al usuario por consola
        respuesta_usuario = input("\nTu respuesta: ")
        
        # Enviar la respuesta al servidor
        socket_cliente.sendto(respuesta_usuario.encode(), direccion_servidor)

finally:
    socket_cliente.close()
    print("\n[Conexión cerrada con el servidor]")