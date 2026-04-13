"""
PROYECTO: MUD LA COMARCA - CALLE DE LOS ARTESANOS
MODULO: DOCUMENTACION TECNICA (README)

Este documento detalla la implementacion del sistema de multiprocesamiento 
y comunicacion asincrona para la simulacion de comercios.

1. REQUISITOS DEL SISTEMA Y ARQUITECTURA
----------------------------------------
El sistema cumple con los siguientes pilares de diseño:

* Procesos Independientes: Cada comercio (Herreria y Carpinteria) se ejecuta 
  en un proceso separado del sistema operativo mediante 'multiprocessing.Process'.
* Comunicacion mediante Colas: Se utilizan 'multiprocessing.Queue' para el 
  intercambio de mensajes entre el jugador y los artesanos, y para la 
  cooperacion entre comercios (inter-comercio).
* Ejecucion en una sola maquina: Toda la logica de comunicacion y gestion de 
  recursos ocurre de forma local.

2. LOGICA DE NEGOCIO IMPLEMENTADA
---------------------------------
Cada comercio gestiona de forma autonoma:

* Catalogos: Definidos en 'catalogos.py' con nombres, recursos, tiempos y precios.
* Produccion Asincrona: La fabricacion de objetos utiliza hilos ('threading.Thread') 
  para no bloquear el bucle de mensajes del proceso.
* Tiempos y Estados: El sistema gestiona tiempos de espera reales y permite 
  que los productos pasen a estar 'disponibles' una vez terminados.

3. COOPERACION INTER-COMERCIO (RELACION)
----------------------------------------
Las profesiones estan relacionadas y dependen una de otra para completar pedidos:

* Solicitud Automatica: Si un comercio carece de un recurso primario que su 
  vecino produce, emite una peticion automatica por la cola correspondiente.
* Ejemplo: La Carpinteria solicita 'lingote_hierro' a la Herreria para fabricar 
  un escudo. La Herreria puede entregar stock existente o fabricar los clavos/bisagras 
  necesarios bajo demanda.

4. ESTRUCTURA DE ARCHIVOS
-------------------------
* calle.py: Orquestador principal, gestiona la interfaz del usuario y los procesos.
* comercio.py: Logica generica de produccion, venta y comunicacion entre hilos.
* catalogos.py: Definicion de datos de productos y recetas.

5. CONTROL DE CONCURRENCIA
--------------------------
* Exclusion Mutua: Se utiliza 'threading.Lock' para garantizar que las 
  operaciones de verificacion y consumo de recursos sean atomicas, evitando 
  condiciones de carrera entre pedidos simultaneos.
* Gestion de Monedas: El dinero se gestiona mediante referencias mutables 
  para que los hilos de produccion puedan actualizar la caja del comercio.

6. INSTRUCCIONES DE USO
-----------------------
Ejecucion: python calle.py
Flujo:
1. Iniciar sesion como jugador.
2. Entrar en un comercio.
3. Solicitar un producto (si no hay stock, se inicia produccion).
4. El sistema notificara cuando el proceso independiente termine la tarea.
"""