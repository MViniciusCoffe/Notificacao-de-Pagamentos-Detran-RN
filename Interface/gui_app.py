import configparser
from os.path import dirname, abspath, join, exists
from sys import path
from tkinter import filedialog, messagebox

import customtkinter as ct
import pandas as pd
from CTkListbox import CTkListbox

parent_dir = dirname(dirname(abspath(__file__)))
path.append(parent_dir)

from Classes.classes import Veiculo, Auto
from Configurações.config_geral import ConfigGerais
from Interface.gui_config import InterfaceConfig

cg = ConfigGerais()
config_arquivo = join(parent_dir, 'Configurações', 'config.ini')

def selecionar_pasta():
    config = configparser.ConfigParser()
    config.read(config_arquivo)
    caminho_bd = config.get('Database', 'pasta', fallback='')

    if not exists(caminho_bd) or '.xlsx' not in caminho_bd:
        caminho_bd = filedialog.askopenfilename()

        if not exists(config_arquivo):
            cg.salvar_config(False, '8:30')

        if caminho_bd:
            config = configparser.ConfigParser()
            config.read(config_arquivo)
            config.set('Database', 'pasta', caminho_bd)

            with open(config_arquivo, 'w') as configfile:
                config.write(configfile)
    return caminho_bd

def selecionar_novo_bd():
    caminho_bd = filedialog.askopenfilename()
    if caminho_bd:
        config = configparser.ConfigParser()
        config.read(config_arquivo)
        config.set('Database', 'pasta', caminho_bd)

        with open(config_arquivo, 'w') as configfile:
            config.write(configfile)
    return caminho_bd

def update_lista_veiculo(lista_veiculo, input_placa, input_renavam):
    pasta_database = selecionar_pasta()

    while lista_veiculo.size() > 0:
        lista_veiculo.delete(0)

    input_placa.delete(0, ct.END)
    input_renavam.delete(0, ct.END)

    try:
        data = pd.read_excel(pasta_database, skiprows=1)
    except PermissionError:
        messagebox.showerror('ERRO', 'ERRO DE PERMISSÃO')
        data = None
    except FileNotFoundError:
        messagebox.showerror('ERRO', 'Arquivo não encontrado, tente novamente')
        selecionar_pasta()
        data = pd.read_excel(pasta_database, skiprows=1)
    except KeyError as e:
        messagebox.showerror('ERRO', f'A Coluna {e} não foi encontrada na base de dados')
        data = None
    except UnboundLocalError:
        messagebox.showerror('ERRO', 'Arquivo de banco de dados não selecionado')
        data = None
    except Exception as e:
        messagebox.showerror('ERRO', f'Houve um erro na hora de atualizar o banco de dados\n{e}')
        data = None

    if data is not None:
        veiculos = data[["Nome", "Renavam", "Placa"]].values.tolist()
    else:
        veiculos = []

    Veiculo.get_veiculos(data)

    for veiculo in veiculos:
        lista_veiculo.insert(ct.END, veiculo[0])


def on_selecionar_veiculo(lista_veiculo, input_placa, input_renavam):
    indice_selecao = lista_veiculo.curselection()
    input_placa.configure(state='normal')
    input_renavam.configure(state='normal')
    if indice_selecao is not None:
        item_selecionado = lista_veiculo.get(indice_selecao)
        for veiculo in Veiculo.veiculos:
            if veiculo.nome_veiculo == item_selecionado:
                input_placa.delete(0, ct.END)
                input_placa.insert(0, veiculo.placa)
                input_renavam.delete(0, ct.END)
                input_renavam.insert(0, veiculo.renavam)
                break
    else:
        messagebox.showwarning('Aviso',
                               'Por favor, escolha um veículo antes de clicar em mostrar detalhes')


def run_app(input_placa, input_renavam):
    placa = input_placa.get()
    renavam = input_renavam.get()

    if placa and renavam:
        auto = Auto()
        if auto.abrir_edge():
            if auto.preencher_site(placa, renavam) == 404:
                messagebox.showerror('Erro', 'Houve um erro na hora de automatizar, verifique se o veículo realmente existe ou se o site mudou de endereço.')
        else:
            messagebox.showerror('Erro', 'Não foi possível iniciar o navegador, verifique se o edge webdriver x64 está atualizado.')
    else:
        messagebox.showerror('ERRO', 'Por favor, preencha as informações de veículos.')


def selecionar_pasta_e_atualizar_bd(lista_veiculo, input_placa, input_renavam):
    selecionar_novo_bd()
    update_lista_veiculo(lista_veiculo, input_placa, input_renavam)


def abrir_config_gui():
    config_interface = InterfaceConfig(cg)
    config_interface.rodar_gui(cg)


def abrir_gui_app():
    ct.set_appearance_mode('dark')

    principal = ct.CTk()
    principal.geometry('350x575')
    principal.title("Meu Programa Principal")


    lista_veiculo = CTkListbox(principal)
    input_placa = ct.CTkEntry(principal)
    input_renavam = ct.CTkEntry(principal)

    selecionar_path = ct.CTkButton(principal,
                                    text="Selecionar Banco de Dados",
                                    command=lambda:
                                        selecionar_pasta_e_atualizar_bd(lista_veiculo,
                                                                        input_placa,
                                                                        input_renavam)
                                                                        )
    selecionar_path.pack(padx=10, pady=10)

    label_veiculo = ct.CTkLabel(principal, text="Selecione um veículo:")
    label_veiculo.pack(padx=10)

    lista_veiculo.pack(padx=10, pady=2)

    botao_preencher = ct.CTkButton(principal,
                                   text='Mostrar Detalhes',
                                   command=lambda:
                                        on_selecionar_veiculo(lista_veiculo,
                                                              input_placa,
                                                              input_renavam
                                                              ))
    botao_preencher.pack(padx=10, pady=10)

    label_placa = ct.CTkLabel(principal, text="Placa:")
    label_placa.pack(padx=10)

    input_placa.pack(padx=10, pady=2)

    renavam_label = ct.CTkLabel(principal, text="Renavam:")
    renavam_label.pack(padx=10)

    input_renavam.pack(padx=10, pady=2)

    rodar_app = ct.CTkButton(principal,
                             text="Rodar App",
                             command=lambda:
                                run_app(input_placa,
                                        input_renavam))
    rodar_app.pack(padx=10, pady=10)

    botao_config = ct.CTkButton(principal, text="Configurações", command=lambda: abrir_config_gui())
    botao_config.pack(padx=10, pady=10)

    input_placa.configure(state='disabled')
    input_renavam.configure(state='disabled')

    update_lista_veiculo(lista_veiculo, input_placa, input_renavam)

    principal.mainloop()
        