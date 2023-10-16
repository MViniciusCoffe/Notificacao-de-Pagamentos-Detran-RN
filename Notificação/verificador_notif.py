import sys
import os

pasta_relativa_programa = '..'

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), pasta_relativa_programa))
interface_dir = os.path.join(app_dir, 'Interface')

sys.path.append(interface_dir)

from time import sleep

from controle_notif import ControleNotif
from modelo_notif import ModeloNotif


def checar_e_notificar():
    while True:
        if cn.mostrar_notif():
            break
        else:
            sleep(60)


if __name__ == '__main__':
    modelo = ModeloNotif()
    cn = ControleNotif(modelo)

    cn.carregar_config()

    checar_e_notificar()
    