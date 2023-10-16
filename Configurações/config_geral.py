import configparser
import os

class ConfigGerais:
    def __init__(self):
        self.programar_hora = False
        self.hora_notif = '8:30'


    def salvar_config(self, programar_hora, hora_notif):
        self.programar_hora = programar_hora
        self.hora_notif = hora_notif

        config = configparser.ConfigParser()

        pasta_codigo = os.path.join(os.path.dirname(__file__))
        config_file = os.path.join(pasta_codigo, 'config.ini')

        config.add_section('Titulo')
        config.set('Titulo', 'padrao1', 'Brasil Paraiba Mine')

        config.add_section('Mensagem')
        config.set('Mensagem', 'padrao2', 'Clique em mim para saber se o pagamento está em dia')

        config.add_section('Programar_hora')
        config.set('Programar_hora', 'padrao3', str(self.programar_hora))

        config.add_section('Icone')
        pasta_icone = r'Banco de dados\logo.png'
        config.set('Icone', 'padrao4', pasta_icone)

        config.add_section('Hora_notif')
        config.set('Hora_notif', 'padrao5', self.hora_notif)

        config.add_section('Database')
        pasta_database = r'Banco de dados\informações licenciamento dos transportes.xlsx'
        config.set('Database', 'pasta', pasta_database)

        with open(config_file, 'w') as configfile:
            config.write(configfile)
    