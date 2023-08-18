#configs do selenium
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import NoSuchElementException



class Veiculo:
    veiculos = []
    def __init__(self, nome_veiculo, renavam, placa):
        self.nome_veiculo = nome_veiculo
        self.renavam = renavam
        self.placa = placa
        

    def __str__(self):
        return f"""Transportes: {self.nome_veiculo}\nRenavam: {self.renavam}\nPlaca: {self.placa}"""
    

    def get_veiculos(dados):
        for linha in dados.itertuples():
            veiculo = Veiculo(
                nome_veiculo = linha.Nome,
                renavam = linha.Renavam, 
                placa = linha.Placa
            )
            Veiculo.veiculos.append(veiculo)
        else:
            return None


class Auto:
    def __init__(self):

        self.pasta_edge = os.path.join(os.getcwd(), 'edgedriver_win64\msedgedriver.exe')
        self.service = Service(self.pasta_edge)
        self.opcoes = webdriver.EdgeOptions()
        self.driver = None

        self.mapa_site = {
            'pagina_inicial': {

                'input_placa': r'//*[@id="placa"]',
                'input_renavam': r'//*[@id="renavam"]',
                'botao_consultar': r'//*[@id="btnConsultaPlaca"]',
                'iframe_captcha': r'/html/body/div[1]/div[2]/div/div/div[2]/form/div[3]/div/div/div/iframe',
                
                'captcha': {
                    'botao_captcha': r'//*[@id="recaptcha-anchor"]/div[1]',
                    'foi_concluido_sem_clicar': r'//*[@class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-focused recaptcha-checkbox-checked"]',
                    'foi_concluido_clicar': r'//*[@class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-checked"]',
                    'concluido_mouse_em_cima': r'//*[@class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-checked recaptcha-checkbox-hover"]'
                },

                'pagina_veiculo': {
                    'info_veiculo': r'//*[@id="td2_servicos_02"]',
                    'info_pagamentos': r'/html/body/div/div[2]/div/div/div[2]/table/tbody/tr'
                }
            }
        }


    def abrir_edge(self):
        self.opcoes.add_argument("--start-maximized")
        self.opcoes.add_experimental_option('detach', True)

        try:
            self.driver = webdriver.Edge(service=self.service, options=self.opcoes)
            return True
        except SessionNotCreatedException:
            if self.driver:
                self.driver.quit()
            return False
        except Exception:
            if self.driver:
                self.driver.quit()
            return False


    def preencher_site(self, placa, renavam):
        self.driver.get('https://www2.detran.rn.gov.br/externo/consultarveiculo.asp')

        try:
            placa_veiculo = self.driver.find_element('xpath',
                                                    self.mapa_site['pagina_inicial']['input_placa'])
            placa_veiculo.send_keys(placa)
            renavam_veiculo = self.driver.find_element('xpath',
                                                    self.mapa_site['pagina_inicial']['input_renavam'])
            renavam_veiculo.send_keys(renavam)
            botao_consultar = self.driver.find_element('xpath',
                                                    self.mapa_site['pagina_inicial']['botao_consultar'])

            iframe_captcha = self.driver.find_element('xpath',
                                                    self.mapa_site['pagina_inicial']['iframe_captcha'])

            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((iframe_captcha)))

            clicar_no_captcha = self.driver.find_element('xpath',
                                                        self.mapa_site['pagina_inicial']['captcha']['botao_captcha'])
            clicar_no_captcha.click()

            try:
                WebDriverWait(self.driver,300).until(lambda driver: WaitCaptcha.espera(driver, Auto()))
                self.driver.switch_to.default_content()
            except TimeoutException:
                self.driver.quit()
                return 404

            botao_consultar.click()
            sem_info = self.driver.find_element('xpath',
                                                self.mapa_site['pagina_inicial']['pagina_veiculo']['info_veiculo'])
            sem_info.click()
            abrir_info = self.driver.find_element('xpath',
                                                self.mapa_site['pagina_inicial']['pagina_veiculo']['info_pagamentos'])
            abrir_info.click()

        except NoSuchElementException:
            self.driver.quit()
            return 404

        
class WaitCaptcha:
    @staticmethod
    def espera(driver, auto):
        foi_concluido_sem_clicar = driver.find_elements('xpath',
                                                        auto.mapa_site['pagina_inicial']['captcha']['foi_concluido_sem_clicar'])
        
        concluido_mouse_em_cima = driver.find_elements('xpath',
                                                        auto.mapa_site['pagina_inicial']['captcha']['concluido_mouse_em_cima'])
        
        foi_concluido_clicar = driver.find_elements('xpath',
                                                    auto.mapa_site['pagina_inicial']['captcha']['foi_concluido_clicar'])
        
        return foi_concluido_clicar or foi_concluido_sem_clicar or concluido_mouse_em_cima
    

