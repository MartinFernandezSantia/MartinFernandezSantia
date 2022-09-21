from tkinter.ttk import *
from tkinter import *
from tkinter.messagebox import *
from models import *

##### Clase desde la cual se ejecuta toda la vista para la creación de personaje y su posterior ventana de estado #####
class Vista:
    def __init__(self, window, mail, root_question):
        # Cierre visual de la ventana de registro/inicio de sesión, porque todavía se necesitan los datos ingresados allí.
        self.window = window
        self.window.withdraw()
        self.mail = mail
        # Instanciación de la clase Abmc() del archivo models.py
        self.modelo = Abmc()

        # Ventana de creación de personaje
        self.root = Toplevel(self.window)
        self.root.configure(bg="violet")
        self.root.title("Creador de Personaje")
        # Centrado de ventana en la pantalla
        self.center_window = self.modelo.center_window
        self.center_window(self.root, 328, 195)

        # Labels
        l1 = Label(
            self.root, text="Selector de Personaje", bg="purple", foreground="white"
        )
        l2 = Label(self.root, text="Nombre:", bg="violet")
        l3 = Label(self.root, text="Sexo:", bg="violet")
        l4 = Label(self.root, text="Raza:", bg="violet")
        l5 = Label(self.root, text="Clase:", bg="violet")
        # Posicionamiento de Labels
        l1.grid(row=0, column=0, columnspan=20, pady=2, sticky=W + E)
        l2.grid(row=1, column=0, sticky=W, padx=2, pady=3)
        l3.grid(row=2, column=0, sticky=W, padx=2, pady=3)
        l4.grid(row=3, column=0, sticky=W, padx=2, pady=3)
        l5.grid(row=4, column=0, sticky=W, padx=2, pady=3)

        # Variables para los Combobox
        sexos = ["Masculino", "Femenino"]
        razas = ["Humano", "Elfo", "Enano", "Orco", "No Muerto"]
        clases = ["Guerrero", "Arquero", "Mago", "Asesino", "Nigromante"]

        # Entry y Comboboxs
        self.e1 = Entry(self.root)
        self.e2 = Combobox(self.root, state="readonly", values=sexos)
        self.e3 = Combobox(self.root, state="readonly", values=razas)
        self.e4 = Combobox(self.root, state="readonly", values=clases)
        # Posicionamiento de Entry y Comboboxs
        self.e1.grid(row=1, column=2, columnspan=2, sticky=W + E, padx=10)
        self.e2.grid(row=2, column=2, columnspan=2, sticky=W + E, padx=10)
        self.e3.grid(row=3, column=2, columnspan=2, sticky=W + E, padx=10)
        self.e4.grid(row=4, column=2, columnspan=2, sticky=W + E, padx=10)

        # Button para guardar los cambios hechos en el personaje si no se detectan errores en el metodo guardar()
        b1 = Button(
            self.root,
            text="Guardar Cambios",
            command=self.guardar,
            bg="purple",
            fg="white",
            activebackground="violet",
        )
        # Button para borrar todos los datos de la cuenta en la base de datos y cerrar la app
        b2 = Button(
            self.root,
            text="Borrar Usuario",
            command=lambda: self.modelo.eliminar_usuario(
                mail,
                self.window,
            ),
            bg="purple",
            fg="white",
            activebackground="violet",
        )
        # Button para abrir una ventana donde se muestran los datos del personaje y sus
        # puntos de habilidad a traves del metodo status()
        b3 = Button(
            self.root,
            text="Ventana de Estado",
            command=self.status,
            bg="purple",
            fg="white",
            activebackground="violet",
        )
        # Posicionamiento de Buttons
        b1.grid(row=5, column=2, columnspan=10)
        b2.grid(row=6, column=2, columnspan=10, pady=5)
        b3.grid(row=6, column=1)

    def guardar(self):
        """Metodo que llama y pasa parametros a otro metodo con el mismo nombre en la clase
        Abmc(), para actualizar la hilera en la base de datos correspondiente a la cuenta,
        siempre que todos los campos hayan sido completados"""
        self.modelo.guardar(
            self.e1.get(), self.e2.get(), self.e3.get(), self.e4.get(), self.mail
        )

    def status(self):
        """Ventana donde se muestran los datos correspondientes al personaje del usuario
        en la base de datos y posee una imagen de fondo relacionada a la raza, clase y
        sexo ingresados"""
        # Creación de la ventana
        self.root2 = Toplevel(self.root)
        self.root2.geometry("183x283")
        self.root2.update()
        self.root2.title(" ")
        # Centrado de la ventana
        self.modelo.center_window(self.root2, 183, 283)

        # Llamada al metodo fetch_values() de la clase Abmc(), para pasarle el mail de la cuenta
        #   por el obtendra los valores de todas las columnas y seran usados por otros metodos de Abmc()
        self.modelo.fetch_values(self.mail)

        # Obtención del ancho y alto de la ventana
        width_root2 = self.root2.winfo_width()
        height_root2 = self.root2.winfo_height()
        # Definicion del Canvas
        my_canvas = Canvas(self.root2, width=width_root2, height=height_root2)
        my_canvas.pack(fill="both", expand=True)
        # Llamada al metodo imagen() de la clase Abmc() para definir la imagen de fondo
        image = self.modelo.imagen(width_root2, height_root2)
        my_canvas.create_image(0, 0, image=image, anchor="nw")

        # Labels que se posicionan mediante los primeros dos parametros (x,y)
        my_canvas.create_text(
            90,
            13,
            text="Estado",
            font=("Helvetica", 14),
            fill="aquamarine",
        )
        my_canvas.create_text(
            35, 33, text="Nombre:", font=("Helvetica", 12), fill="aquamarine"
        )
        my_canvas.create_text(
            25, 58, text="Sexo:", font=("Helvetica", 12), fill="aquamarine"
        )
        my_canvas.create_text(
            25, 83, text="Raza:", font=("Helvetica", 12), fill="aquamarine"
        )
        my_canvas.create_text(
            26, 108, text="Clase:", font=("Helvetica", 12), fill="aquamarine"
        )
        my_canvas.create_text(
            39, 133, text="Vitalidad:", font=("Helvetica", 12), fill="aquamarine"
        )
        my_canvas.create_text(
            37, 158, text="Agilidad:", font=("Helvetica", 12), fill="aquamarine"
        )
        my_canvas.create_text(
            32, 183, text="Fuerza:", font=("Helvetica", 12), fill="aquamarine"
        )
        my_canvas.create_text(
            48, 208, text="Inteligencia:", font=("Helvetica", 12), fill="aquamarine"
        )
        my_canvas.create_text(
            33, 233, text="Suerte:", font=("Helvetica", 12), fill="aquamarine"
        )

        # Llamada al metodo create_labels() de Abmc(), el cual creara las Labels de Canvas y les dara
        # como nombre valores de la base de datos
        self.modelo.create_labels(my_canvas)

        # Button para cerrar la ventana de Estado
        button1 = Button(
            self.root2,
            text="Cerrar",
            command=lambda: self.root2.withdraw(),
        )
        # Posicionamiento del Button
        my_canvas.create_window(130, 252, anchor="nw", window=button1)
