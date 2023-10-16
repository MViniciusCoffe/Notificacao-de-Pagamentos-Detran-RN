# configs das pastas
import os
import sys

rel_pasta_program = '..'

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), rel_pasta_program))
config_dir = os.path.join(app_dir, 'Configurações')

sys.path.append(config_dir)


# configs das notificações
import configparser
import datetime
from time import *

# classe que inicializa as notificações
class ModeloNotif:
    def __init__(self):
        self.titulo = ''
        self.mensagem = ''
        self.hora = 0
        self.minuto = 0
        self.icone = ''


    def carregar_config_notif(self):
        config = configparser.ConfigParser()

        arquivo_config = config_dir + r'\config.ini'

        config.read(arquivo_config)

        self.titulo = config.get('Titulo',
                                'padrao1',
                                fallback='Brazil Paraiba Mine'
                                )
            
        self.mensagem = config.get('Mensagem',
                                    'padrao2',
                                    fallback='Notificação de pagamento de veículo, clique em mim para saber se o pagamento está em dia'
                                    )
        
        
        self.icone = config.get('Icone',
                                'padrao4',
                                fallback=r'Banco de dados\logo.png'
                                )

        self.programar_hora = config.getboolean('Programar_hora',
                                                'padrao3',
                                                fallback=False
                                                )

        if self.programar_hora == False:
            # Ele configura para inicializar na hora da inicialização do Windows
            agora = datetime.datetime.now()
            self.hora, self.minuto = agora.hour, agora.minute
        else:
            tempo = config.get('Hora_notif',
                               'padrao5',
                               fallback='8:30'
                               )
            
            self.hora, self.minuto = map(int, tempo.split(':'))

        return self.titulo, self.mensagem, self.icone, self.hora, self.minuto
        