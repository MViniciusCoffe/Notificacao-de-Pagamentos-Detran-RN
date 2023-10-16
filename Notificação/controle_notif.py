from mostrar_notif import VerNotif
from modelo_notif import ModeloNotif

modelo = ModeloNotif()

class ControleNotif:
    def __init__(self, modelo):
        self.modelo = modelo
        self.ver = VerNotif(self.modelo)

    
    def carregar_config(self):
        self.modelo.carregar_config_notif()
        
    
    def mostrar_notif(self):
        if self.ver.mostrar_notif():
            return True
        