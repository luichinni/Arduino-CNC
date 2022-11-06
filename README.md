# Arduino-CNC [Work In Progress]
En este repositorio está (estará) toda la información y programas propios para poder construir una CNC haciendo uso de 2 **L293D** junto a unos carros y motores de disqueteras/lectoras de CD-DVD y una placa arduino.

_Este proyecto nació como una tarea escolar de uno de los miembros y se fue desarrollando a lo largo de varias semanas._
Autores del proyecto: 
- **Joaquin Perez**.
- **Luciano Macias**.

# GcodeSender
El python script GcodeSender.py es una aplicación de escritorio que permite enviar las instrucciones de un Gcode por puerto serie a la placa arduino.

![Interfaz](https://user-images.githubusercontent.com/98102676/200195481-305fd8ff-3368-46e9-bec1-c1bbeaddd19c.png)

Como podemos ver en la interfaz, cada apartado corresponde a:
### 1.1. Abrir
La pestaña abrir nos deja escojer un archivo .gcode (también puede ser .txt) para cargarlo en el programa y luego ser enviado a la CNC.
### 1.2. Conectar
Esta pestaña permite seleccionar el puerto al que está conectado nuestra máquina.
_Nota: seleccionar un puerto que no corresponda o la desconeccion del aparato puede lanzar un error tanto en esta etapa como más adelante._
### 2. Estado de conexión
Esta casilla de la interfaz se iluminara en rojo cuando la máquina no está conectada y en verde una vez establecida la conexión
### 3. Visualizador de Gcode
La entrada de texto (marcada como 3), mostrará un mensaje de bienvenida al inicio del programa; una vez cargado un gcode podremos ver todas las instrucciones.
A medida que avanza el envio, las instrucciones se iran eliminando una a una.
### 4.1. Iniciar/Reanudar
Este botón se encarga de dar marcha a la máquina una vez establecido tanto el gcode como el puerto; también, en caso de haber detenido el programa, podra reanudarse la desde la ultima instrucción no ejecutada.
### 4.2 Detener/Pausar
Este botón se encarga de detener y/o pausar el programa actual que se está imprimiendo en la CNC, a su vez, al detener el programa, se comprobará el estado de la conexión con la máquina.

# GcodeCreator
[WIP]

# Programa Arduino
[WIP]

# Consideraciones
Algunas consideraciones a tener en cuenta son:
- Los códigos G soportados son:
  - G00
  - G01
  - G02
  - G03
- Las velocidades que establecen algunos Gcode con el parametro E o F, no se tiene en cuenta dentro del ecosistema creado entre los programas, el parametro de velocidad es establecido dentro del código de arduino.
- GcodeCreator posee una capacidad muy limitada en cuanto a diseño se refiere, no tiene funciones como Ctrl+Z.
- Al usarse motores de baja corriente y tensión, el circuito adjunto en el repositorio no es util para motores más grandes, no obstante, puede servir como punto de partida para entender la sencilla lógica utilizada y adaptar con una placa de potencia casera o un módulo de L293D de arduino.
