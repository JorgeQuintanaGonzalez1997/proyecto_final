
class Puja:
    def __init__(self, idLibro, idUsuario, precio, fecha):
        self.idLibro = idLibro
        self.idUsuario = idUsuario
        self.precio = precio
        self.fecha = fecha

    def getIdLibro(self):
        return self.idLibro

    def getIdUsuario(self):
        return self.idUsuario

    def getPrecio(self):
        return self.precio

    def getFecha(self):
        return self.fecha

    def setIdLibro(self, idLibro):
        self.idLibro = idLibro

    def setIdUsuario(self, idUsuario):
        self.idUsuario = idUsuario

    def setPrecio(self, precio):
        self.precio = precio

    def setFecha(self, fecha):
        self.fecha = fecha