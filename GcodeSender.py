# serial -> se usa para comms con arduino por los puertos serie
import serial
import serial.tools.list_ports
# tkinter -> se usa para la parte grafica de la aplicacion
import tkinter as tk
import tkinter.filedialog
from tkinter.messagebox import showerror

# globales del sistema
arduino = None # conexion
puertoAct = None # puerto actual 
habilitado = False # True si se inició la transferencia de instrucciones
archivoC = False # True si se cargó un gcode

# creamos la ventana
root = tk.Tk()
ancho,alto=800,400
root.geometry(f'{ancho}x{alto}')
root.resizable(False,False)
root.title('Gcode Sender') # titulo de la ventana
root.config(bg='lightgrey') # color fondo
# texto en pantalla
# indicador de estado de la conexion
estado = tk.Label(root,text='Desconectado',bg='red')
estado.grid(column=0,row=0,columnspan=2,sticky=tk.NSEW)
# mostrador del gcode en la interfaz
log = tk.Text(root)
log.config(width=45) # 40 caracteres por linea
log.grid(column=0,row=1,columnspan=2,sticky=tk.NSEW)


# funciones
def insertar(contenedor,texto): # inserta lineas en un widget de texto
    contenedor['state']='normal'
    contenedor.insert('end',texto)
    contenedor['state']='disabled'

def limpiar(contenedor): # limpia el widget de texto
    contenedor['state']='normal'
    contenedor.delete('1.0', 'end')
    contenedor['state']='disabled'

def eliminarLinea(contenedor,linea): # elimina una linea del widget de texto
    contenedor['state']='normal'
    contenedor.delete(linea+'.0',linea+'.end + 1 char')
    contenedor['state']='disabled'

def cargarGcode(): # carga del gcode
    global archivoC
    try: # intentamos cargar la direccion de un archivo .gcode
        pathGcode = tkinter.filedialog.askopenfilename(filetypes=(("gcode files","*.gcode"),("All files","*.*")))
        if pathGcode != '': # si se selecciono una ruta se limpia el mostrador
            limpiar(log)
        with open(pathGcode) as gcode:
            """
                Eliminamos los comentarios de cada linea
                y las escribimos en el mostrador si no están vacias
            """
            for line in gcode:
                if not line.startswith(';') and line != '\n':
                    line = ''.join(line.split())+'\n' # elimina los caracteres especiales como saltos de linea, espacios en blanco, etc
                    if ";" in line:
                        line = line[:line.index(';')]+'\n' # elimina los comentarios
                    insertar(log,line)
        archivoC = True # establecemos que ya hay un archivo cargado
    except:
        pass

def conectar(puertoAct):
    global arduino
    try: # intentamos conectar al puerto seleccionado, si da error se avisará con un mensaje
        arduino = serial.Serial(port=puertoAct, baudrate=9600, timeout=.1)
        estado.config(text='Conectado',bg='green') # mostramos el estado de conexion
    except:
        showerror('Error de conexión','Hubo un error al intentar conectarse al puerto '+puertoAct)
        estado.config(text='Desconectado',bg='red')

def selecPuerto():
    # ventana de seleccion
    selPort = tk.Toplevel()
    selPort.wm_title('Seleccionar Puerto')
    # lista selectora de puerto
    availablePorts = list(serial.tools.list_ports.comports())
    # guardamos la lista en el widget de seleccion
    var = tk.Variable(value=availablePorts)
    lb = tk.Listbox(selPort,listvariable=var,height=6,selectmode=tk.EXTENDED,width=80)
    lb.pack(expand=True,fill=tk.BOTH)
    # funcion interna
    def setPuerto(event):
        global puertoAct
        # filtramos el puerto COM
        seleccion = lb.curselection()
        puertoAct = ",".join([lb.get(i) for i in seleccion]).replace(' ','')
        puertoAct = puertoAct[0:puertoAct.index('-')]
        # cerramos la ventana de seleccion
        selPort.destroy()
        # conectamos
        conectar(puertoAct)
    # le damos a la lista de seleccion la funcion interna
    lb.bind('<<ListboxSelect>>',setPuerto)

def iniciarProceso(): # habilitamos el pasaje de instrucciones al arduino
    global habilitado
    if habilitado == False and estado['text'] == 'Conectado':
        habilitado = True
    else:
        showerror('Error al iniciar','No hay un puerto seleccionado')

def detenerProceso(): # detenemos el pasaje de instrucciones al arduino
    global habilitado, arduino, puertoAct
    habilitado = False
    try:
        arduino = serial.Serial(port=puertoAct, baudrate=9600, timeout=.1)
    except:
        estado.config(text='Desconectado',bg='red')

def comArduino(): # subrutina que se repetira durante todo el programa
    global arduino,habilitado,archivoC
    if habilitado and archivoC: # si todo está dado
        ok = str(arduino.readline()) # recibimos validacion del arduino para enviarle instrucciones
        if ok.find('V') != -1: # si ya está disponible le enviamos
            comnd=log.get('1.0','2.0')
            eliminarLinea(log,'1')
            arduino.write(comnd)

    root.after(50,comArduino) # restablecemos el contador del bucle principal para ejecutar nuevamente comArduino

# menu superior
menubar = tk.Menu(root)
root.config(menu=menubar)
# botones del menu superior
menubar.add_command(label='Abrir',command=lambda:cargarGcode())
menubar.add_command(label='Conectar',command=lambda:selecPuerto())

# botones interfaz
startBtn = tk.Button(root,text='Iniciar/Reanudar',command=lambda:iniciarProceso())
startBtn.grid(column=4,row=0,sticky=tk.EW,padx=100,pady=10,ipadx=80,ipady=20)

stopBtn = tk.Button(root,text='Detener/Pausar',command=lambda:detenerProceso())
stopBtn.grid(column=4,row=1,sticky='NEW',padx=100,pady=10,ipadx=80,ipady=20)

# mensaje de bienvenida
insertar(log,'Bienvenido a GcodeSender\n')
insertar(log,'Abrir -> Seleccion del Gcode en la PC\n')
insertar(log,'Conectar -> Seleccion de puerto\n')
insertar(log,'----------------------------------------\n')

root.after(50,comArduino) # establecemos que se ejecute comArduino a los 50ms luego de iniciado el programa
root.mainloop() # bucle principal