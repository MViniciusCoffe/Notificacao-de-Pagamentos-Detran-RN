import customtkinter as ct
from Configurações.config_geral import ConfigGerais

class InterfaceConfig:
    def __init__(self, cg):
        self.cg = cg
        self.janela_config = ct.CTk()


    def rodar_gui(self, cg):
        self.janela_config.geometry('350x250')

        escolher_veiculo_texto = ct.CTkLabel(self.janela_config, text='CONFIGURAÇÕES')
        escolher_veiculo_texto.pack(padx=10, pady=10)

        programar_hora = ct.BooleanVar()
        programar_hora_chk = ct.CTkCheckBox(self.janela_config,
                                            text='Programar Horário',
                                            variable=programar_hora,
                                            command=lambda: self.aparece_caixa_texto(programar_hora,
                                                                                     entrada_tempo,
                                                                                     botao_salvar))
        programar_hora_chk.pack(padx=30, pady=5, anchor='w')



        tempo_texto = ct.CTkLabel(self.janela_config, text="""Digite a hora na qual notificação deverá ser enviada""")
        tempo_texto.pack(padx=10, pady=5, anchor='n')

        entrada_tempo = ct.CTkEntry(self.janela_config)

        entrada_tempo.pack(padx=0, pady=0, anchor='center')
        entrada_tempo.configure(state='disabled', fg_color='grey')
        entrada_tempo.bind('<KeyRelease>',
                        lambda event:
                        self.validar_tempo(event,
                                        programar_hora,
                                        entrada_tempo,
                                        botao_salvar
                                        ))


        texto_explicativo = ct.CTkLabel(self.janela_config, text='Caso esteja desmarcada essa opção, a notificação\n será enviada assim que o computador ligar')
        texto_explicativo.pack(padx=10, pady=10)

        cg = ConfigGerais()

        botao_salvar = ct.CTkButton(self.janela_config,
                                    text='Salvar Configurações',
                                    command=lambda:
                                    self.salvar_e_fechar(cg,
                                                         programar_hora.get(),
                                                         entrada_tempo.get())
                                    )

        botao_salvar.pack(padx=10, pady=10, side='bottom')

        self.janela_config.mainloop()


    def aparece_caixa_texto(self, programar_hora, entrada_tempo, botao_salvar):
        if programar_hora.get():
            entrada_tempo.configure(state='normal', fg_color='black', text_color='white')
            botao_salvar.configure(state='disabled')
        else:
            entrada_tempo.configure(state='disabled', fg_color='grey')
            botao_salvar.configure(state='normal')


    def validar_tempo(self, event, programar_hora, entrada_tempo, botao_salvar):
        try:
            if programar_hora.get():
                hora, minuto = map(int, entrada_tempo.get().split(':'))
                botao_salvar.configure(state='disabled')
                if 0 <= hora <= 23 and 0 <= minuto <= 59:
                    botao_salvar.configure(state='normal')
                else:
                    botao_salvar.configure(state='disabled')
            else:
                botao_salvar.configure(state='normal')
                entrada_tempo.delete(0, 'end')
        except ValueError:
            botao_salvar.configure(state='disabled')


    def salvar_e_fechar(self, cg, programar_hora, entrada_tempo):
        cg.salvar_config(programar_hora, entrada_tempo)
        self.fechar()


    def fechar(self):
        self.janela_config.destroy()
