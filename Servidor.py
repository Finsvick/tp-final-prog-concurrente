import socket
import threading
import time

# Variable global: Inventario de entradas
entradas_disponibles = 5
lock_inventario = threading.Lock()
semaforo_clientes = threading.Semaphore(3)

# --- NUEVO REQUERIMIENTO A: Sistema de Actualización ---
# Bandera booleana para pausar el servidor.
en_actualizacion = threading.Event()
en_actualizacion.set()

def simular_actualizacion():
    """Hilo independiente que frena el servidor a los 2 segundos"""
    time.sleep(2)
    print("\n[ALERTA] Iniciando actualización del sistema. Pausando ventas...")
    en_actualizacion.clear()
    time.sleep(3) # La actualización dura 3 segundos
    print("[ALERTA] Actualización terminada. Reanudando ventas...\n")
    en_actualizacion.set()
    
# --- NUEVO REQUERIMIENTO B: Envío de Emails ---
def enviar_email_confirmacion(direccion):
    """Simula el tiempo de conexión a un servidor SMTP externo"""
    print(f" -> [Mail] Conectando al servidor para enviar ticket a {direccion}...")
    # Retraso de red bloqueante
    time.sleep(2)
    print(f" -> [Mail] Email enviado con éxito a {direccion}.")

def manejar_cliente(conexion, direccion):
    global entradas_disponibles
    try:
        en_actualizacion.wait()
        peticion = conexion.recv(1024).decode('utf-8')

        if peticion == "COMPRAR":
            with semaforo_clientes:
                with lock_inventario:
                    if entradas_disponibles > 0:
                        time.sleep(0.5)
                        entradas_disponibles -= 1
                        respuesta = f"Compra exitosa. Quedan {entradas_disponibles} entradas."
                    else:
                        respuesta = "Operación rechazada. Entradas agotadas."

               
                if "exitosa" in respuesta:
                    hilo_mail = threading.Thread(target=enviar_email_confirmacion,args=(direccion,),)
                    hilo_mail.start()

        else:
            respuesta = "Petición no reconocida."

      
        conexion.send(respuesta.encode('utf-8'))

    finally:
        conexion.close()


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 5555))
    servidor.listen()
    print("[SERVIDOR] TicketFast iniciado. Entradas disponibles: 5")

    # Lanzamos el hilo que provocará la actualización
    hilo_update = threading.Thread(target=simular_actualizacion)
    hilo_update.start()

    while True:
        conexion, direccion = servidor.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion,
        direccion))
        hilo_cliente.start()

if __name__ == "__main__": iniciar_servidor()