from tkinter.messagebox import *
from peewee import *
from tkinter import *
import re
from datetime import datetime
from observador import *
import os
from PIL import ImageTk, Image

##### Creación de la base de datos mediante peewee #####
try:
    # Se define el tipo de base y su nombre
    db = SqliteDatabase("personaje_creado.db")

    class BaseModel(Model):
        class Meta:
            database = db

    # Se definen las columnas
    class Personaje(BaseModel):
        id = PrimaryKeyField()
        mail = CharField(unique=True)
        usuario = CharField(default="None")
        contraseña = CharField(default="None")
        nombre = CharField(default="None")
        sexo = CharField(default="None")
        raza = CharField(default="None")
        clase = CharField(default="None")
        vitalidad = CharField(default="None")
        agilidad = CharField(default="None")
        inteligencia = CharField(default="None")
        fuerza = CharField(default="None")
        suerte = CharField(default="None")

    # Se conecta con la base y se crea la tabla con el nombre de la clase en la que se definieron las columnas
    db.connect()
    db.create_tables([Personaje])
except:
    print("La base ya ha sido creada")

##### Clase donde se concentra la mayor parte del apartado funcional (backend) de la app #####
class Abmc(Sujeto):
    def __init__(self):
        pass

    def deco_log(metodo):
        """Metodo que funciona como decorador, el cual registra el inicio de sesión, registro,
        y todas las modificaciones que afecten a la base de datos, exeptuando su creación, en el archivo log.txt"""

        def envoltura(*args, **kwargs):
            # Variable con el nombre del metodo que activo el decorador pasado a mayusculas
            n_metodo = metodo.__name__.upper()
            # Variable con la fecha actual (año-mes-dia hora,minuto,segundo)
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Dependiendo del metodo que haya activado al decorador, la variable "modificaciones"
            #   obtendra valores diferentes
            if n_metodo == "GUARDAR":
                modificaciones = (
                    "{} /// {} /// SE HAN REALIZADO LAS SIGUIENTES MODIFICACIONES /// NOMBRE: {} - SEXO: {} - RAZA: {} - CLASE: {} /// CORRESPONDIENTES A LA CUENTA: {}"
                ).format(fecha, n_metodo, args[1], args[2], args[3], args[4], args[5])
            elif n_metodo == "INSERTAR_REGISTRO":
                modificaciones = (
                    "{} /// {} /// SE HA CREADO UNA CUENTA NUEVA /// USUARIO: {} - MAIL: {} - CONTRASEÑA: {}"
                ).format(fecha, n_metodo, args[1], args[2], args[3])
            elif n_metodo == "ELIMINAR_USUARIO":
                modificaciones = (
                    "{} /// {} /// SE HA ELIMINADO LA CUENTA CORRESPONDIENTE AL MAIL: {}"
                ).format(fecha, n_metodo, args[1])
            elif n_metodo == "COMPROBAR_USUARIO":
                modificaciones = "{} /// {} /// SE HA INICIADO SESIÓN EN LA CUENTA CORRESPONDIENTE AL MAIL: {}".format(
                    fecha, n_metodo, args[1]
                )

            # Se abre/crea el archivo log.txt y se registra en este el contenido de la variable modificaciones
            log = open("log.txt", "a", encoding="utf-8")
            log.write(modificaciones)
            log.write("\n")
            log.close()

            return metodo(*args, **kwargs)

        return envoltura

    @deco_log
    def eliminar_usuario(self, mail, root):
        """Metodo para eliminar todos los datos correspondientes a la hilera en la base de datos
        que coincida con el mail dado, y luego destruir la ventana de creacion de personaje"""
        Personaje.delete().where(Personaje.mail == mail).execute()
        showinfo("", "Su usuario ha sido eliminado")

        # Llamada al metodo notificar() de la clase Sujeto() en el archivo observador.py,
        #   para registrar en el archivo log_observador.txt las modificaciones hechas
        self.notificar(
            "SE HA ELIMINADO LA CUENTA CORRESPONDIENTE AL MAIL: {}".format(mail)
        )
        root.destroy()

    def center_window(self, root, width=200, height=100):
        # Funcion para centrar la ventana Tk() con respecto a la pantalla del pc
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        root.geometry("%dx%d+%d+%d" % (width, height, x, y))

    @deco_log
    def guardar(self, e1, e2, e3, e4, mail):
        """Funcion para actualizar hilera de la tabla, que corresponda con el mail ingresado por el usuario,
        con aquellos valores que el mismo introdujo mediante los Entry en visual.py"""
        # Actualización de los datos en la tabla
        Personaje.update(nombre=e1, sexo=e2, raza=e3, clase=e4).where(
            Personaje.mail == mail
        ).execute()

        # Llamada al metodo notificar() de la clase Sujeto() en el archivo observador.py,
        #   para registrar en el archivo log_observador.txt las modificaciones hechas
        self.notificar(
            f"SE HAN REALIZADO LAS SIGUIENTES MODIFICACIONES /// NOMBRE: {e1} - "
            + "SEXO: {} - RAZA: {} - CLASE: {} /// CORRESPONDIENTES A LA CUENTA: {}".format(
                e2, e3, e4, mail
            )
        )

        fetch = Personaje.select().where(Personaje.mail == mail)
        # Dependiendo de la clase elegida se asignaran automaticamente los puntos mediante
        #   el metodo update() a las columnas correspondientes en la base de datos
        for value in fetch:
            if value.raza != "":
                if value.sexo != "":
                    if "Mago" == value.clase:
                        self.update("10", "6", "17", "4", "13", mail)
                        showinfo("", "Su personaje ha sido actualizado exitosamente")
                    elif "Guerrero" == value.clase:
                        self.update("15", "8", "3", "14", "9", mail)
                        showinfo("", "Su personaje ha sido actualizado exitosamente")
                    elif "Arquero" == value.clase:
                        self.update("12", "15", "8", "7", "8", mail)
                        showinfo("", "Su personaje ha sido actualizado exitosamente")
                    elif "Asesino" == value.clase:
                        self.update("9", "17", "11", "14", "0", mail)
                        showinfo("", "Su personaje ha sido actualizado exitosamente")
                    elif "Nigromante" == value.clase:
                        self.update("15", "3", "14", "8", "10", mail)
                        showinfo("", "Su personaje ha sido actualizado exitosamente")
                    else:
                        showerror(
                            "Alerta",
                            "Parece que no has introducido una clase para tu personaje",
                        )
                else:
                    showerror(
                        "Alerta",
                        "Parece que no has introducido un sexo para tu personaje",
                    )
            else:
                showerror(
                    "Alerta",
                    "Parece que no has introducido una raza para tu personaje",
                )

    def update(self, v, a, i, f, s, mail):
        # Metodo para abreviar la asignación de puntos en el metodo guardar()
        Personaje.update(
            vitalidad=v, agilidad=a, inteligencia=i, fuerza=f, suerte=s
        ).where(Personaje.mail == mail).execute()

    @deco_log
    def comprobar_usuario(self, get1, get2, vista, root_login, root_question):
        """Funcion para comprobar que el usuario existe en la base de datos, y que la contraseña
        ingresada coincide con el mail"""
        # Pasos que si son True permitiran al usuario ingresar a la ventana de creación de personaje
        step1 = False
        step2 = False

        # Creación de lista con todos los mails en la base de datos
        fetch = Personaje.select(Personaje.mail).tuples()
        lista_mails = []
        for e in fetch:
            lista_mails += e

        # Condicional que comprueba si el mail ingresado por el usuario esta en lista_mails y pone a step1 en True
        if get1 in lista_mails:
            step1 = True
            print("step1=True")
        else:
            showerror(
                "Alerta",
                "El correo electronico introducido no se encuentra registrado",
            )
            print(get1)
            print(lista_mails)

        fetch2 = Personaje.select().where(Personaje.mail == get1)

        # Condicional que comprueba que la contraseña ingresada por el usuario coincida con la de la base de datos
        #   y pone a step2 en True
        for e in fetch2:
            usuario = e.usuario
            if get2 == e.contraseña:
                step2 = True
                print("step2=True")
            else:
                showerror(
                    "Alerta",
                    "La contraseña ingresada no coincide con el mail introducido",
                )

        # Condicional que comprueba que step1 y step2 esten en True, y da paso libre al usuario para ingresar. Tambien
        #   se encarga de crear la ventana de creación de personaje, ya que esta es un TopLevel()
        if step1 == True and step2 == True:
            welcome = "Bienvenido {}".format(usuario)
            showinfo("", welcome)
            self.vista = vista(root_login, get1, root_question)
            self.observador = ConcreteObserver(self.vista.modelo)
            # Llamada al metodo notificar() de la clase Sujeto() en el archivo observador.py,
            #   para registrar en el archivo log_observador.txt las modificaciones hechas
            self.notificar(
                "SE HA INICIADO SESIÓN EN LA CUENTA CORRESPONDIENTE AL MAIL: {}".format(
                    get1
                )
            )
        else:
            pass

    @deco_log
    def insertar_registro(
        self, get1, get2, get3, get4, root_registro, root_question, vista
    ):
        """Metodo para comprobar que los datos ingresados por el usuario en el registro,
        cumplan con los requisitos y pueda crearse una nueva hilera/cuenta en la base de datos"""
        try:
            # Llamada al metodo mail_validation() donde se comprueba que el mail tenga estilo de mail via regex
            self.mail_valiadation(get2)
            passw = False

            # Condicional que comprueba si ambas contraseñas ingresadas por el usuario coinciden
            if get3 == get4:
                passw = True
            else:
                showerror("Alerta", "Las contraseñas introducidas no coinciden")

            # Condicional que comprueba si passw es True y si el mail paso el chequeo de mail_validation, y en
            #   dicho caso insertara el mail y la contraseña en una nueva hilera en la base de datos, y creara la
            #   ventana de creación de personaje
            if passw == True and self.check == True:
                Personaje.insert(usuario=get1, mail=get2, contraseña=get3).execute()
                self.vista = vista(root_registro, get2, root_question)
                self.observador = ConcreteObserver(self.vista.modelo)
            else:
                pass

            # Llamada al metodo notificar() de la clase Sujeto() en el archivo observador.py,
            # para registrar en el archivo log_observador.txt las modificaciones hechas
            self.notificar(
                "SE HA CREADO UNA CUENTA NUEVA /// USUARIO: {} - MAIL: {} - CONTRASEÑA: {}".format(
                    get1, get2, get3
                )
            )
        except IntegrityError:
            showerror(
                "Alerta",
                "El correo electronico introducido ya esta vinculado a una cuenta",
            )

    def fetch_values(self, mail):
        # Metodo por el cual se recuperan los valores asociados al mail ingresado por el usuario, en la base de datos.
        fetch = Personaje.select().where(Personaje.mail == mail)
        for e in fetch:
            self.vitalidad = e.vitalidad
            self.nombre = e.nombre
            self.sexo = e.sexo
            self.raza = e.raza
            self.clase = e.clase
            self.inteligencia = e.inteligencia
            self.agilidad = e.agilidad
            self.fuerza = e.fuerza
            self.suerte = e.suerte

    def create_labels(self, my_canvas):
        """Metodo por el cual se crean Labels de Canvas con los nombres de los valores
        recuperados en fetch_values() y para ser expuestas en el metodo status() de la
        clase Vista() en el archivo visual.py"""
        self.define_labels(33, my_canvas, self.nombre)
        self.define_labels(58, my_canvas, self.sexo)
        self.define_labels(83, my_canvas, self.raza)
        self.define_labels(108, my_canvas, self.clase)
        self.define_labels(133, my_canvas, self.vitalidad)
        self.define_labels(158, my_canvas, self.agilidad)
        self.define_labels(183, my_canvas, self.inteligencia)
        self.define_labels(208, my_canvas, self.fuerza)
        self.define_labels(233, my_canvas, self.suerte)

    def define_labels(self, y, my_canvas, text):
        # Metodo donde se definen los Labels de Canvas
        my_canvas.create_text(
            130, y, text=text, font=("Helvetica", 12), fill="aquamarine"
        )

    def imagen(self, width, height):
        """Metodo por el cual se designa la imagen que sera usada como fondo de la ventana
        del metodo status() en la clase Vista(), y se reasigna su tamaño al adecuado para la ventana"""
        # Directorio relativo a la carpeta en la que se encuentra este archivo
        BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
        # Nombre que coincidira con una de las carpetas dentro de img
        carpeta = self.raza.lower()
        # Condicional que toma los valores de raza, clase y sexo extraidos en fetch_values() y asigna
        #   un string a nombre_img, el cual coincidira con el nombre de una imagen en la carpeta img. Si
        #   la carpeta en la cual se buscara la imagen es "no muerto", se omitira el sexo del personaje ya que
        #   este daria lo mismo.
        if carpeta == "no muerto":
            nombre_img = "{}_{}.jpg".format(self.raza, self.clase)
        else:
            nombre_img = "{}_{}_{}.jpg".format(self.sexo, self.raza, self.clase)
        # Ruta de la imagen
        ruta = os.path.join(BASE_DIR, "img", carpeta, nombre_img)
        imagen = Image.open(ruta)
        # Reasignacion del tamaño de la imagen para que coincida con la ventana
        resized_image = imagen.resize((width, height), Image.ANTIALIAS)
        # Nueva imagen que sera usada como fondo de la ventana
        self.new_image = ImageTk.PhotoImage(resized_image)
        return self.new_image

    def mail_valiadation(self, email):
        # Validacion del formato de mail correcto para el registro de usuarios
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, str(email)):
            self.check = True
        else:
            self.check = False
            showerror(
                "Alerta",
                "El correo electronico introducido no coincide con el formato: alguien@mail.dominio",
            )
            raise SyntaxError(
                "El mail introducido no coincide con el formato: alguien@mail.dominio"
            )
