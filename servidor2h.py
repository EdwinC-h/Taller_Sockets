import socket
import threading
from datetime import datetime 

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_socket.bind(("localhost", 5000))
print("Servidor UDP esperando mensajes")

preguntas = [
    {"pregunta": "1. ¿Cuanto es 13*9? ","respuesta": "117"},
    {"pregunta": "2. ¿Github permite control de versiones de software? ","respuesta": "si"},
    {"pregunta": "3. ¿? ","respuesta": "JAVA"},
    {"pregunta": "4. ¿Framework que permite manejar software por componentes independientes? ","respuesta": "REACT"},
    {"pregunta": "5. ¿Que herramienta tecnologica centraliza la informacion y resuelve problemas internos en una empresa? ","respuesta": "ERPs"}
] 

clientes_estado = {}


def manejar_cliente(mensaje_bytes, direccion, servidor):
    mensaje = mensaje_bytes.decode().strip().lower()
    
    # Si el cliente es nuevo, inicializamos su estado y le enviamos la primera pregunta
    if direccion not in clientes_estado:
        clientes_estado[direccion] = {
            "indice": 0,
            "puntaje": 0,
            "inicio": datetime.now()
        }
        
        tiempo_inicio = clientes_estado[direccion]["inicio"].strftime("%Y-%m-%d %H:%M:%S")
        print(f"Conexion iniciada con el cliente {direccion} a las {tiempo_inicio}")
        
        primera_pregunta = preguntas[0]["pregunta"]
        respuesta_inicial = f"Cuestionario Iniciado\n\n{primera_pregunta}"
        servidor.sendto(respuesta_inicial.encode(), direccion)
        
    else:
        # Recuperar el estado actual del cliente
        estado = clientes_estado[direccion]
        idx_actual = estado["indice"]
        
        # Evaluar la respuesta del cliente a la pregunta actual
        respuesta_correcta = preguntas[idx_actual]["respuesta"]
        
        if mensaje == respuesta_correcta:
            estado["puntaje"] += 1
            evaluacion = "Respuesta CORRECTA."
        else:
            evaluacion = f"Respuesta INCORRECTA. La correcta era: {preguntas[idx_actual]['respuesta']}"
        
        # Avanzar al siguiente índice de pregunta
        estado["indice"] += 1
        
        # Verificar si aún quedan preguntas
        if estado["indice"] < len(preguntas):
            siguiente_pregunta = preguntas[estado["indice"]]["pregunta"]
            respuesta_envio = f"{evaluacion}\n\n{siguiente_pregunta}"
            servidor.sendto(respuesta_envio.encode(), direccion)
        else:
            # Fin del cuestionario (se respondieron las 5 preguntas)
            tiempo_fin = datetime.now()
            duracion = tiempo_fin - estado["inicio"]
            
            resultado_final = (
                f"{evaluacion}\n\n"
                f"=== CUESTIONARIO FINALIZADO ===\n"
                f"Puntaje total: {estado['puntaje']} / 5\n\n"
                f"--- Registro de Conexion ---\n"
                f"Inicio: {estado['inicio'].strftime('%H:%M:%S')}\n"
                f"Fin: {tiempo_fin.strftime('%H:%M:%S')}\n"
                f"Duracion de la sesion: {duracion.seconds} segundos"
            )
            servidor.sendto(resultado_final.encode(), direccion)
            
            print(f"Conexion finalizada con el cliente {direccion} a las {tiempo_fin.strftime('%Y-%m-%d %H:%M:%S')}. Puntaje: {estado['puntaje']}/5")
            
            # Limpiar el estado del cliente al terminar
            del clientes_estado[direccion]


# Bucle principal del servidor que escucha y delega a los hilos
while True:
    mensaje_bytes, direccion = servidor_socket.recvfrom(1024)
    
    # Creamos un hilo independiente para manejar cada mensaje recibido de forma concurrente
    hilo = threading.Thread(target=manejar_cliente, args=(mensaje_bytes, direccion, servidor_socket))
    hilo.start()
    