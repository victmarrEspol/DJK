import os
import math
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from grafosDinamicos.Grafos import Grafos

class InterfazGrafos:

    def __init__(self, root):
        self.root = root
        self.root.title("DJK")
        self.root.geometry("1000x800")
        self.root.configure(bg="white")

        self.g1 = None
        self.nombreOrigen = ""
        self.nombreDestino = ""
        self.rutaOriginal = []
        self.distanciaOriginal = math.inf
        self.nodosCerrados = []

        self.imagenTk = None
        self.varsNodos = {}

        self.contenedor = tk.Frame(self.root, bg="white")
        self.contenedor.pack(fill="both", expand=True)

        self.mostrarPantalla1()

    def limpiarPantalla(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def reiniciarEstado(self):
        self.g1 = None
        self.nombreOrigen = ""
        self.nombreDestino = ""
        self.rutaOriginal = []
        self.distanciaOriginal = math.inf
        self.nodosCerrados = []
        self.varsNodos = {}
        self.imagenTk = None

    def crearEntrada(self, parent, ancho=30):
        marco = tk.Frame(parent, bg="black", padx=2, pady=2)
        entrada = tk.Entry(marco, font=("Arial", 14), relief="flat", width=ancho)
        entrada.pack()
        return marco, entrada

    def generarImagenDesdeGrafo(self, ruta, cerrados):
        import matplotlib.pyplot as plt

        funcionOriginalShow = plt.show
        plt.show = lambda *args, **kwargs: None

        try:
            self.g1.mostrarGrafo(ruta, cerrados)
        finally:
            plt.show = funcionOriginalShow
            plt.close("all")

    def cargarImagenEnLabel(self, rutaArchivo, labelDestino, maximo=(530, 420)):
        imagen = Image.open(rutaArchivo)
        imagen.thumbnail(maximo)
        self.imagenTk = ImageTk.PhotoImage(imagen)
        labelDestino.config(image=self.imagenTk)

    # Widget 1

    def mostrarPantalla1(self):
        self.limpiarPantalla()
        self.reiniciarEstado()

        marcoPrincipal = tk.Frame(self.contenedor, bg="white")
        marcoPrincipal.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(
            marcoPrincipal,
            text="DJK",
            font=("Comic Sans MS", 36, "bold"),
            bg="white",
            fg="black"
        )
        titulo.pack(pady=(10, 20))

        resumenTitulo = tk.Label(
            marcoPrincipal,
            text="Análisis de ruta menos costosa en una matriz origen - destino",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="black"
        )
        resumenTitulo.pack(pady=(0, 10))

        resumenTexto = (
            "Indicaciones para que el programa funcione correctamente:\n"
            "- La matriz debe estar posicionada desde la casilla A1.\n"
            "- Las primeras celdas de cada fila y columna deben contener los\n nombres de los lugares de origen y destino, en el mismo orden.\n"
            "- Las celdas interiores deben contener las respectivas ponderaciones.\n"
            "- La matriz en la hoja de Excel debe ser simétrica.\n"
            "Ejemplo:"
        )

        resumen = tk.Label(
            marcoPrincipal,
            text=resumenTexto,
            font=("Arial", 13),
            bg="white",
            fg="black",
            wraplength=650,
            justify="center"
        )
        resumen.pack(pady=(0, 25))

        # Imagen de presentación
        imagen = Image.open("imagenEjemplo2.png")

        # Ajustar dimensiones sin deformar
        imagen.thumbnail((550, 400))

        # Convertir imagen
        self.imagenPresentacion = ImageTk.PhotoImage(imagen)

        # Crear widget
        labelPresentacion = tk.Label(
            marcoPrincipal,
            image=self.imagenPresentacion,
            bg="white"
        )

        labelPresentacion.pack(pady=(0, 25))

        ingresarArchivo = tk.Label(
            marcoPrincipal,
            text="Ingrese archivo .xlsx",
            font=("Arial", 16),
            bg="white",
            fg="black"
        )
        ingresarArchivo.pack(pady=(0, 15))

        botonArchivo = tk.Button(
            marcoPrincipal,
            text="Subir archivo",
            font=("Arial", 14),
            bg="#e6e6e6",
            activebackground="#d0d0d0",
            command=self.subirArchivo
        )
        botonArchivo.pack(pady=(0, 12))

        self.labelErrorArchivo = tk.Label(
            marcoPrincipal,
            text="",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="red"
        )
        self.labelErrorArchivo.pack()

    def subirArchivo(self):
        rutaArchivo = filedialog.askopenfilename(
            title="Seleccionar archivo .xlsx",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )

        if not rutaArchivo:
            return

        if not rutaArchivo.lower().endswith(".xlsx"):
            self.labelErrorArchivo.config(
                text="Su archivo no es .xlsx, vuelva a intentar"
            )
            return

        try:
            shutil.copy(rutaArchivo, "transporteMatriz.xlsx")
            self.g1 = Grafos("Grafo1", "transporteMatriz.xlsx")
            self.mostrarPantalla2()
        except Exception:
            self.labelErrorArchivo.config(
                text="No se pudo cargar el archivo, vuelva a intentar"
            )

    # Widget 2

    def mostrarPantalla2(self):
        self.limpiarPantalla()

        botonRegresar = tk.Button(
            self.contenedor,
            text="←",
            font=("Arial", 16, "bold"),
            bg="#e6e6e6",
            activebackground="#d0d0d0",
            command=self.mostrarPantalla1
        )
        botonRegresar.place(x=20, y=20)

        marcoCentral = tk.Frame(self.contenedor, bg="white")
        marcoCentral.place(relx=0.5, rely=0.45, anchor="center")

        labelOrigen = tk.Label(
            marcoCentral,
            text="Nombre del origen de la ruta:",
            font=("Arial", 16),
            bg="white",
            fg="black"
        )
        labelOrigen.grid(row=0, column=0, padx=10, pady=18, sticky="e")

        marcoOrigen, self.entryOrigen = self.crearEntrada(marcoCentral, ancho=25)
        marcoOrigen.grid(row=0, column=1, padx=10, pady=18)

        labelDestino = tk.Label(
            marcoCentral,
            text="Nombre del destino de la ruta:",
            font=("Arial", 16),
            bg="white",
            fg="black"
        )
        labelDestino.grid(row=1, column=0, padx=10, pady=18, sticky="e")

        marcoDestino, self.entryDestino = self.crearEntrada(marcoCentral, ancho=25)
        marcoDestino.grid(row=1, column=1, padx=10, pady=18)

        self.labelErrorLugares = tk.Label(
            marcoCentral,
            text="",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="red"
        )
        self.labelErrorLugares.grid(row=2, column=0, columnspan=2, pady=(5, 10))

        botonCalcular = tk.Button(
            marcoCentral,
            text="Calcular ruta",
            font=("Arial", 14),
            bg="#e6e6e6",
            activebackground="#d0d0d0",
            command=self.validarLugares
        )
        botonCalcular.grid(row=3, column=0, columnspan=2, pady=20)

    def validarLugares(self):
        self.nombreOrigen = self.entryOrigen.get().strip()
        self.nombreDestino = self.entryDestino.get().strip()

        nombresValidos = self.g1.grafo.vs["name"]

        if self.nombreOrigen not in nombresValidos or self.nombreDestino not in nombresValidos:
            self.labelErrorLugares.config(
                text="El lugar no existe, vuelva a intentar"
            )
            return

        self.mostrarPantalla3()

    # Widget 3

    def mostrarPantalla3(self):
        self.limpiarPantalla()

        botonRegresar = tk.Button(
            self.contenedor,
            text="←",
            font=("Arial", 16, "bold"),
            bg="#e6e6e6",
            activebackground="#d0d0d0",
            command=self.mostrarPantalla2
        )
        botonRegresar.place(x=20, y=20)

        titulo = tk.Label(
            self.contenedor,
            text="Información sobre ruta menos costosa",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="black"
        )
        titulo.pack(pady=(20, 10))

        # Variables iniciales pedidas
        mapaPredecesores, mapaDistancias = self.g1.algDijkstra(self.nombreOrigen, [])

        destino = self.g1.grafo.vs.find(name=self.nombreDestino)
        self.distanciaOriginal = mapaDistancias[destino]

        if self.distanciaOriginal == math.inf:
            self.rutaOriginal = []
        else:
            self.rutaOriginal = self.g1.obtenerCamino(
                self.nombreOrigen,
                self.nombreDestino,
                mapaPredecesores
            )

        # Marco superior: imagen + datos
        marcoSuperior = tk.Frame(self.contenedor, bg="white")
        marcoSuperior.pack(fill="x", padx=25, pady=10)

        # Imagen
        marcoImagen = tk.Frame(marcoSuperior, bg="white")
        marcoImagen.pack(side="left", padx=15, pady=10)

        self.labelImagen = tk.Label(
            marcoImagen,
            bg="white",
            bd=2,
            relief="solid",
            width=530,
            height=420
        )
        self.labelImagen.pack()

        # Datos
        marcoDatos = tk.Frame(marcoSuperior, bg="white")
        marcoDatos.pack(side="left", fill="both", expand=True, padx=20)

        self.labelDistanciaTitulo = tk.Label(
            marcoDatos,
            text="Costo total:",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black",
            anchor="w"
        )
        self.labelDistanciaTitulo.pack(fill="x", pady=(10, 5))

        self.labelDistanciaValor = tk.Label(
            marcoDatos,
            text="",
            font=("Arial", 14),
            bg="white",
            fg="black",
            justify="left",
            anchor="w",
            wraplength=380
        )
        self.labelDistanciaValor.pack(fill="x", pady=(0, 15))

        self.labelRutaTitulo = tk.Label(
            marcoDatos,
            text="Ruta:",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black",
            anchor="w"
        )
        self.labelRutaTitulo.pack(fill="x", pady=(0, 5))

        self.labelRutaValor = tk.Label(
            marcoDatos,
            text="",
            font=("Arial", 14),
            bg="white",
            fg="black",
            justify="left",
            anchor="w",
            wraplength=380
        )
        self.labelRutaValor.pack(fill="x", pady=(0, 15))

        self.labelCambioTitulo = tk.Label(
            marcoDatos,
            text="Información de cambio:",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black",
            anchor="w"
        )
        self.labelCambioTitulo.pack(fill="x", pady=(0, 5))

        self.labelCambioValor = tk.Label(
            marcoDatos,
            text="",
            font=("Arial", 13),
            bg="white",
            fg="black",
            justify="left",
            anchor="w",
            wraplength=420
        )
        self.labelCambioValor.pack(fill="x", pady=(0, 15))

        # Sección de nodos
        seccionNodos = tk.Frame(self.contenedor, bg="white")
        seccionNodos.pack(fill="both", expand=True, padx=25, pady=10)

        #////
        # Encabezado de la sección de nodos
        encabezadoNodos = tk.Frame(seccionNodos, bg="white")
        encabezadoNodos.pack(fill="x", pady=(0, 15))

        tituloNodos = tk.Label(
            encabezadoNodos,
            text="Simular cierres de nodos:",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="black"
        )
        tituloNodos.pack(side="left")

        # Buscador
        self.busquedaNodo = tk.StringVar()

        entradaBusqueda = tk.Entry(
            encabezadoNodos,
            textvariable=self.busquedaNodo,
            font=("Arial", 12),
            width=22
        )
        entradaBusqueda.pack(side="right", padx=10)

        labelBusqueda = tk.Label(
            encabezadoNodos,
            text="Buscar nodo:",
            font=("Arial", 12),
            bg="white"
        )
        labelBusqueda.pack(side="right")
        # ////


        # Zona con scroll para muchos nodos
        contenedorScroll = tk.Frame(seccionNodos, bg="white")
        contenedorScroll.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedorScroll, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(contenedorScroll, orient="vertical", command=canvas.yview)
        frameInterno = tk.Frame(canvas, bg="white")

        frameInterno.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frameInterno, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Crear botones toggle para nodos
        self.varsNodos = {}
        self.botonesNodos = {}
        nombresNodos = self.g1.grafo.vs["name"]

        columnas = 3
        for i, nombreNodo in enumerate(nombresNodos):
            var = tk.BooleanVar(value=False)
            self.varsNodos[nombreNodo] = var

            botonNodo = tk.Checkbutton(
                frameInterno,
                text=nombreNodo,
                variable=var,
                indicatoron=False,
                font=("Arial", 12),
                width=20,
                relief="raised",
                bd=2,
                selectcolor="#cfcfcf",
                bg="#efefef",
                activebackground="#d9d9d9",
                command=self.actualizarSimulacion
            )

            # AQUÍ VA EL PUNTO 2
            self.botonesNodos[nombreNodo] = botonNodo

            fila = i // columnas
            columna = i % columnas

            botonNodo.grid(
                row=fila,
                column=columna,
                padx=10,
                pady=8,
                sticky="ew"
            )

        # Guardar referencia al canvas
        self.canvasNodos = canvas

        # Conectar el buscador con el método de filtrado
        self.busquedaNodo.trace_add(
            "write",
            self.filtrarNodos
        )

        # Cargar estado inicial
        self.actualizarPantallaResultado(
            ruta=self.rutaOriginal,
            distancia=self.distanciaOriginal,
            textoCambio="",
            cerrados = []
        )

    def actualizarPantallaResultado(self, ruta, distancia, textoCambio, cerrados):
        # Actualizar imagen
        self.generarImagenDesdeGrafo(ruta, cerrados)
        self.cargarImagenEnLabel("imagenGrafo.png", self.labelImagen)

        # Actualizar distancia
        if distancia == math.inf:
            self.labelDistanciaValor.config(text="no se puede llegar al destino")
        else:
            self.labelDistanciaValor.config(text=str(distancia))

        # Actualizar ruta
        if distancia == math.inf:
            self.labelRutaValor.config(text="[]")
        else:
            self.labelRutaValor.config(text=str(ruta))

        # Actualizar información de cambio
        self.labelCambioValor.config(text=textoCambio)

    def actualizarSimulacion(self):
        self.nodosCerrados = [
            nombreNodo
            for nombreNodo, var in self.varsNodos.items()
            if var.get()
        ]

        # Si no hay nodos cerrados, mostrar estado original
        if len(self.nodosCerrados) == 0:
            self.actualizarPantallaResultado(
                ruta=self.rutaOriginal,
                distancia=self.distanciaOriginal,
                textoCambio="",
                cerrados = []
            )
            return

        rutaNueva, distanciaNueva = self.g1.recalcularDijkstra(
            self.nombreOrigen,
            self.nombreDestino,
            self.rutaOriginal,
            self.distanciaOriginal,
            self.nodosCerrados
        )

        # Calcular porcentaje y categoría
        # Se maneja cuidadosamente el caso de distancias infinitas o distancia original 0
        if self.distanciaOriginal == math.inf:
            textoCambio = (
                "No es posible calcular el porcentaje de cambio porque "
                "originalmente no se podía llegar al destino."
            )
        else:
            if self.distanciaOriginal == 0:
                if distanciaNueva == 0:
                    porcentaje = 0
                else:
                    porcentaje = math.inf
            else:
                porcentaje = (distanciaNueva - self.distanciaOriginal) * 100 / self.distanciaOriginal

            categoria = ""

            if porcentaje == math.inf:
                categoria = "Ruta imposible"
            elif porcentaje <= 0:
                categoria = "Sin impacto"
            elif porcentaje <= 10:
                categoria = "Urgencia baja"
            elif porcentaje <= 25:
                categoria = "Urgencia media"
            elif porcentaje <= 50:
                categoria = "Urgencia alta"
            else:
                categoria = "Urgencia crítica"

            if(porcentaje == math.inf):
                textoCambio = (
                        "Tras el cierre de " + str(self.nodosCerrados) +
                        " se ha vuelto imposible llegar al nodo de destino.\n" +
                        "Categoría: " + str(categoria)
                )
            else:
                textoCambio = (
                    "Tras el cierre de " + str(self.nodosCerrados) +
                    " el costo total ha aumentado un " + str(round(porcentaje, 3)) + "%.\n" +
                    "Categoría: " + str(categoria)
                )

        self.actualizarPantallaResultado(
            ruta=rutaNueva,
            distancia=distanciaNueva,
            textoCambio=textoCambio,
            cerrados = self.nodosCerrados
        )

    def filtrarNodos(self, *args):

        busqueda = self.busquedaNodo.get().strip().lower()

        columnas = 3
        indice = 0

        for nombre, boton in self.botonesNodos.items():

            if busqueda in str(nombre).lower():

                fila = indice // columnas
                columna = indice % columnas

                boton.grid(
                    row=fila,
                    column=columna,
                    padx=10,
                    pady=8,
                    sticky="ew"
                )

                indice += 1

            else:
                boton.grid_remove()

        # Actualizar el área desplazable
        self.root.update_idletasks()

        self.canvasNodos.configure(
            scrollregion=self.canvasNodos.bbox("all")
        )

        self.canvasNodos.yview_moveto(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafos(root)
    root.mainloop()