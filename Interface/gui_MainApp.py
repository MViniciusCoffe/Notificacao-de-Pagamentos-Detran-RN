import sys
import os
import configparser

pasta_relativa_programa = '..'

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), pasta_relativa_programa))

configs_dir = os.path.join(app_dir, 'Configurações')

sys.path.append(configs_dir)

import customtkinter as ct
import pandas as pd

from CTkListbox import *
from tkinter import filedialog, messagebox
from classes import Veiculo, Auto
from config_geral import ConfigGerais
from gui_config import InterfaceConfig


def selecionar_pasta_e_atualizar_bd(lista_veiculo, input_placa, input_renavam):
    caminho_arquivo = filedialog.askopenfilename()
    if caminho_arquivo:
        config = configparser.ConfigParser()
        config.read(r'Configurações\config.ini')
        config.set('Database', 'pasta', caminho_arquivo)

        with open(r'Configurações\config.ini', 'w') as configfile:
            config.write(configfile)

        update_lista_veiculo(lista_veiculo, input_placa, input_renavam)


def update_lista_veiculo(lista_veiculo, input_placa, input_renavam):
    while lista_veiculo.size() > 0:
        lista_veiculo.delete(0)
    
    input_placa.delete(0, ct.END)
    input_renavam.delete(0, ct.END)

    config = configparser.ConfigParser()
    config.read(r'Configurações\config.ini')

    pasta_database = config.get('Database', 'pasta', fallback=r'Banco de dados\informações licenciamento dos transportes.xlsx')
    if not pasta_database:
        return False
    
    try:
        data = pd.read_excel(pasta_database, skiprows=1)
        veiculos = data[["Nome", "Renavam", "Placa"]].values.tolist()
    except PermissionError:
        veiculos = []
        messagebox.showerror('ERRO', 'ERRO DE PERMISSÃO')
    except FileNotFoundError:
        selecionar_pasta_e_atualizar_bd(lista_veiculo, input_placa, input_renavam)
        veiculos = data[["Nome", "Renavam", "Placa"]].values.tolist()
    except KeyError as e:
        veiculos = []
        messagebox.showerror('ERRO', f'A Coluna {e} não foi encontrada na base de dados')
    except Exception:
        veiculos = []
        messagebox.showerror('ERRO', 'Houve um erro na hora de atualizar o banco de dados')
    
    Veiculo.get_veiculos(data)
    
    for veiculo in veiculos:
        lista_veiculo.insert(ct.END, veiculo[0])


def on_selecionar_veiculo(lista_veiculo, input_placa, input_renavam):
    indice_selecao = lista_veiculo.curselection()
    input_placa.configure(state='normal')
    input_renavam.configure(state='normal')
    if indice_selecao != None:
        item_selecionado = lista_veiculo.get(indice_selecao)
        for veiculo in Veiculo.veiculos:
            if veiculo.nome_veiculo == item_selecionado:
                input_placa.delete(0, ct.END)
                input_placa.insert(0, veiculo.placa)
                input_renavam.delete(0, ct.END)
                input_renavam.insert(0, veiculo.renavam)
                break
    else:
        messagebox.showwarning('Aviso', 'Por favor, escolha um veículo antes de clicar em mostrar detalhes')


def run_app(input_placa, input_renavam):
    placa = input_placa.get()
    renavam = input_renavam.get()
    
    if placa and renavam:
        auto = Auto()
        if auto.abrir_edge():
            if auto.preencher_site(placa, renavam) == 404:
                messagebox.showerror('Erro', 'Houve um erro na hora de automatizar, verifique se o veículo realmente existe ou se o site mudou de endereço.')
        else:
            messagebox.showerror('Erro', 'Não foi possível iniciar o navegador.')
    else:
        messagebox.showerror('ERRO', 'Por favor, preencha as informações de placas.')


def abrir_config_gui():
    cg = ConfigGerais()
    config_interface = InterfaceConfig(cg)
    config_interface.rodar_gui(cg)


def abrir_gui_app():
    principal = ct.CTk()
    principal.geometry('350x575')
    principal.title("Meu Programa Principal")

    lista_veiculo = CTkListbox(principal)
    input_placa = ct.CTkEntry(principal)
    input_renavam = ct.CTkEntry(principal)

    selecionar_pasta = ct.CTkButton(principal, 
                                    text="Selecionar Banco de Dados", 
                                    command=lambda: 
                                        selecionar_pasta_e_atualizar_bd(lista_veiculo, 
                                                                        input_placa, 
                                                                        input_renavam))
    selecionar_pasta.pack(padx=10, pady=10)

    label_veiculo = ct.CTkLabel(principal, text="Selecione um veículo:")
    label_veiculo.pack(padx=10)

    lista_veiculo.pack(padx=10, pady=2)

    botao_preencher = ct.CTkButton(principal, text='Mostrar Detalhes', command=lambda: on_selecionar_veiculo(lista_veiculo, 
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

    rodar_app = ct.CTkButton(principal, text="Rodar App", command=lambda: run_app(input_placa, input_renavam))
    rodar_app.pack(padx=10, pady=10)

    botao_config = ct.CTkButton(principal, text="Configurações", command=lambda: abrir_config_gui())
    botao_config.pack(padx=10, pady=10)

    input_placa.configure(state='disabled')
    input_renavam.configure(state='disabled')
    
    update_lista_veiculo(lista_veiculo, input_placa, input_renavam)

    principal.mainloop()
        