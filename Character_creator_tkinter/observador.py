class Sujeto:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def notificar(self, *args, **kwargs):
        for observador in self.observadores:
            observador.update(args)


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserver(Observador):
    def __init__(self, obj):
        self.observador_a = obj
        self.observador_a.agregar(self)

    def update(self, *args, **kwargs):
        print("Actualización dentro de ObservadorConcreto")
        for i in args:
            for e in i:
                print(e)
                modificacion = e
        print("-" * 50)
        log = open("log_observador.txt", "a", encoding="utf-8")
        log.write(str(modificacion))
        log.write("\n")
        log.close()
