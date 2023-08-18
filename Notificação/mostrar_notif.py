import win10toast_click
import os
import datetime


class VerNotif:
    def __init__(self, modelo):
        self.modelo = modelo


    def mostrar_notif(self):
        agora = datetime.datetime.now()
        if self.modelo.hora == agora.hour and self.modelo.minuto == agora.minute:
            notif = win10toast_click.ToastNotifier()

            notif.show_toast(
                title=self.modelo.titulo,
                msg=self.modelo.mensagem,
                icon_path=self.modelo.icone,
                duration=30,
                threaded=True,
                callback_on_click=self.rodar_app
            )
            return True
        else:
            return False
        

    def rodar_app(self):
        os.system(r'python.exe "Verificador de Pagamentos.py"')