from tkinter import *
from models import *
from visual import Vista

##### Clase desde la cual se ejecuta toda la vista para iniciar sesión o registrar una cuenta nueva #####
class Login:
    def __init__(self):
        # Instanciación de la clase Abmc() del archivo models.py
        self.modelo = Abmc()
        # Primera ventana de la app donde se pregunta al usuario si desea registrarse o iniciar sesión
        self.root_question = Tk()
        self.root_question.title(" ")
        # Llamado al metodo center_window() que permite centrar la ventana de tkinter en la pantalla
        self.center_window = self.modelo.center_window
        self.center_window(self.root_question, 200, 100)

        # Label
        question = Label(
            self.root_question,
            text="¿Desea registrar un nuevo usuario o iniciar sesión?",
            font="12",
            justify=CENTER,
            wraplength=150,
        )
        # Posicionamiento de Label
        question.pack(side=TOP)

        # Button para registrarse
        boton_registrar = Button(
            self.root_question, text="Registrarse", command=self.registro
        )
        # Button para iniciar sesión
        boton_login = Button(
            self.root_question, text="Iniciar sesión", command=self.log_in
        )
        # Posicionamiento de Buttons
        boton_registrar.pack(side=LEFT, padx=10)
        boton_login.pack(side=RIGHT, padx=10)

        self.root_question.mainloop()

    def registro(self):
        # Cierre de la ventana anterior y creación de la nueva
        self.root_question.destroy()
        """Ventana de registro de usuario, donde si ambas contraseñas coinciden y el mail ingresado no existe
        en la base de datos, se creara una nueva hilera en la base y se abrira la ventana de creacion de personaje
        referente a dicha hilera"""
        self.root_registro = Tk()
        self.root_registro.title("Registro de usuario")
        # Centrado de la ventana tkinter en la pantalla
        self.center_window(self.root_registro, 270, 155)

        # Labels
        reg_l0 = Label(
            self.root_registro,
            text="Complete los siguientes campos para continuar",
            font="12",
            justify=CENTER,
            wraplength=250,
        )
        reg_l1 = Label(self.root_registro, text="Nombre de Usuario: ")
        reg_l2 = Label(self.root_registro, text="Correo electrónico: ")
        reg_l3 = Label(self.root_registro, text="Contraseña: ")
        reg_l4 = Label(self.root_registro, text="Confirmé su contraseña: ")
        # Posicionamiento de Labels
        reg_l0.grid(row=0, column=0, columnspan=16)
        reg_l1.grid(row=1, column=0)
        reg_l2.grid(row=2, column=0)
        reg_l3.grid(row=3, column=0)
        reg_l4.grid(row=4, column=0)

        # Entrys respectivos a los Labels
        self.reg_e1 = Entry(self.root_registro)
        self.reg_e2 = Entry(self.root_registro)
        self.reg_e3 = Entry(self.root_registro, show="*")
        self.reg_e4 = Entry(self.root_registro, show="*")
        # Posicionamiento de Entrys
        self.reg_e1.grid(row=1, column=1)
        self.reg_e2.grid(row=2, column=1)
        self.reg_e3.grid(row=3, column=1)
        self.reg_e4.grid(row=4, column=1)

        # Button para crear el usuario si no hay errores detectados en el metodo instertar_registro()
        reg_button1 = Button(
            self.root_registro, text="Crear usuario", command=self.insertar_registro
        )
        # Posicionamiento del Button
        reg_button1.grid(row=5, column=1)

        self.root_registro.mainloop()

    def insertar_registro(self):
        """Metodo donde se le pasan parametros a otro metodo con el mismo nombre en la clase
        Abmc(), para verificar que los datos ingresados cumplan con los requisitos necesarios."""
        self.vista3 = Vista
        self.modelo.insertar_registro(
            self.reg_e1.get(),
            self.reg_e2.get(),
            self.reg_e3.get(),
            self.reg_e4.get(),
            self.root_registro,
            self.root_question,
            self.vista3,
        )

    def log_in(self):
        """Ventana para ingresar a una cuenta preexistente en la base de datos, donde si el mail
        coincide con uno existente en la base y la contraseña con dicho mail, se abrira la ventana
        de creacion de personaje"""
        # Cierre de la ventana anterior y creación de la nueva
        self.root_question.destroy()
        self.root_login = Tk()
        self.root_login.title("Inicio de sesión")
        # Centrado de la ventana tkinter en la pantalla
        self.center_window(self.root_login, 270, 110)

        # Labels
        log_l0 = Label(
            self.root_login,
            text="Inicia sesión con tu correo electronico y contraseña",
            font="12",
            justify=CENTER,
            wraplength=260,
        )
        log_l1 = Label(self.root_login, text="Correo electrónico: ")
        log_l2 = Label(self.root_login, text="Contraseña: ")
        # Posicionamiento de Labels
        log_l0.grid(row=0, column=0, columnspan=16)
        log_l1.grid(row=1, column=0)
        log_l2.grid(row=2, column=0)

        # Entrys respectivos a los Labels
        self.log_e1 = Entry(self.root_login)
        self.log_e2 = Entry(self.root_login, show="*")
        # Posicionamiento de Entrys
        self.log_e1.grid(row=1, column=1)
        self.log_e2.grid(row=2, column=1)

        # Button para iniciar sesión si no hay errores detectados en el metodo comprobar_usuario()
        log_button1 = Button(
            self.root_login, text="Aceptar", command=self.comprobar_usuario
        )
        # Posicionamiento de Button
        log_button1.grid(row=3, column=1)

        self.root_login.mainloop()

    def comprobar_usuario(self):
        """Metodo donde se le pasan parametros a otro metodo con el mismo nombre en la clase
        Abmc(), para verificar que los datos ingresados coincidan con los de la base de datos."""
        self.vista2 = Vista
        self.modelo.comprobar_usuario(
            self.log_e1.get(),
            self.log_e2.get(),
            self.vista2,
            self.root_login,
            self.root_question,
        )
