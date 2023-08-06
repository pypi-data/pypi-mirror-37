# -*- coding: utf-8 -*-
'''
Created on 24 de ago de 2018

@author: koliveirab
'''
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from .Error import Elemento_erro
from time import sleep

class Js_Script():
    
    def __init__(self,drive):
        self.driver=drive
        
    def execute_script(self,script):
        '''Este metodo executa comando javascript no console do navegador
        
            parametros:
            script(obrigatorio):o script a ser executado
           Exemplo:
        ("window.scrollTo(0, document.body.scrollHeight);")'''
        #executa javascript no driver
        self.driver.execute_script(script)   
        
    def rolagem_tela(self,valor):
        #executa a rolagem da tela pelo javascript
        '''Este metodo faz a rolagem da pagina que esta sendo usada em javaScript
        Exemplo: rolagem_tela(100)'''
        self.execute_script("window.scrollTo({}, document.body.scrollHeight);".format(valor))
        
'''Este Modulo trabalha com as esperas feitas pelo WebDriverWait'''
class Espera():
    ''' Esta classe tem o intuito de prover conexao com o WevDriverWait'''
    
    
    
        
    def aguarde_condicao(self,condicao,tempo,intervalo=0.5,menssagem_exception=''):
        ''' Este metodo trabalha com o aguarde trazendo uma condicao para o aguarde explicito
        retorna o elemento
        parametros:
            condicao(obrigatorio):Condicao de espera
            tempo: valor de tentativas
            intervalo:intervalo em cada tentativa
            menssagem_exception:mensagem que sera gerada caso de erro
        Exemplo:
        aguarde_condicao(condicao,100,1,'não foi possivel achar o elemento visivel')
            '''
        
        #cria um objeto wait passando o tempo e o intervalo de cada para cada ciclo
        wait=WebDriverWait(self.driver,tempo,intervalo)
        #ira aguardar a condição passada ser valida, caso não seja dependendo valida no tempo determinado ira gerar um erro
        #caso nao sera gerado retorna o elemento
        return wait.until(condicao,menssagem_exception)


    def aguarde_condicao_negada(self,condicao,tempo,intervalo=0.5,menssagem_exception=''):
        ''' Este metodo trabalha com o aguarde trazendo uma condicao para o aguarde explicito, aonde ela nao deve aparecer
        retorna o elemento
        parametros:
            condicao(obrigatorio):Condicao de espera
            tempo: valor de tentativas
            intervalo:intervalo em cada tentativa
            menssagem_exception:mensagem que sera gerada caso de erro
        Exemplo:
        aguarde_condicao_negada(condicao,100,1,'este elemento esta visivel')
            '''
        
        #cria um objeto wait passando o tempo e o intervalo de cada para cada ciclo

        wait=WebDriverWait(self.driver,tempo,intervalo)
        return wait.until_not(condicao, menssagem_exception)
    
class Simula():
    
    def mover_mouse(self,elemento,tipo,implicit=None):
        #simula o movimento do mouse ate um elemento especificado
        self.ActionChains.move_to_element(self.elemento(elemento,tipo,implicit)).perform()
        
    def duplo_clique(self,elemento,tipo,implicit=None):
        #simula o duplo clique do mouse ate um elemento especificado
        self.ActionsChains.double_click(self.elemento(elemento,tipo,implicit)).perform()
        
    def clique(self,elemento,tipo,implicit=None,Botao='left'):
        #simula o clique do mouse ate um elemento especificado, podendo ser o botao direito ou esquerdo

        if(Botao=="left"):
            self.ActionsChains.click(self.elemento(elemento,tipo,implicit)).perform()
        elif(Botao=='rigth'):
            self.ActionsChains.context_click(self.elemento(elemento,tipo,implicit)).perform()
        else:
            Erro="""
                Escolha um valor Valido
                Os Valores são:
                left ou rigth
                
                """
            raise Elemento_erro(Erro)
        
    def clique_arraste(self,elemento1,tipo1,implicit1,elemento2,tipo2,implicit2):
        #simula o arraste entre os elementos 1 e 2
        self.ActionsChains.drag_and_drop(self.elemento(elemento1,tipo1,implicit1),self.elemento(elemento2,tipo2,implicit2)).perform()
        
    def digitos(self,elemento,tipo,implicit,lista_de_chaves):
        #simula o a digitação em um elemento especificado
        self.ActionsChains.send_keys_to_element(self.app.elemento(elemento,tipo,implicit),*lista_de_chaves).perform()
        
class Alerta():
    def __init__(self,driver):
        #trabalha com o alert do driver criando um objeto
        self.alert=Alert(driver)
        
    def aceitar(self):
        #aceitando o alerta apresentado
        self.alert.accept()
        
    def rejeitar(self):
        #reijeitando o alerta apresentado
        self.alert.dismiss()
        
    def inserir_texto(self,texto):
        #escrevendo na entrada input do alert
        self.alert.send_keys(texto)
        
    def get_texto(self):
        #retirando o texto do alert
        return self.alert.text
    
class select_model():
    
    def __ini__(self,elemento,tipo,implicit=None):
        '''Este metodo trabalha com listas <Select> para preenchimento 
        parametros:
        elemento(obrigatorio): elemento do select
        
        Exemplo:
        
        select(app.elemento('user.select.list','id'),['masculino','São Paulo'],'texto')
        
        '''
        Erro="""
                            Não é um tipo de seleção valido
                            Digite um tipo valido:
                            
                            index
                            valor
                            texto    
                                
                                """
        self.select=Select(self.elemento(elemento,tipo,implicit))
            
    def select_index(self,*args):
        for valor in args:
            self.select.select_by_index(valor)
                        
    def select_valor(self,*args):
        for valor in args:
            self.select.select_by_value(valor)
                        
    def select_text(self,*args):
        for valor in args:
            self.select.select_by_text(valor)
            
    def deselect_index(self,*args):
        for valor in args:
            self.select.deselect_by_index(valor)
    def deselect_valor(self,*args):
        for valor in args:
            self.select.deselect_by_value(valor)
    def deselect_text(self,*args):
        for valor in args:
            self.select.deselect_by_text(valor)   
            
    def deselect_all(self):
                    
        self.select.deselect_all()
            

class MyListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        pass
    
    def after_navigate_to(self, url, driver):
        pass
    
    def before_navigate_back(self, driver):
        pass

    def after_navigate_back(self, driver):
        pass

    def before_navigate_forward(self, driver):
        pass

    def after_navigate_forward(self, driver):
        pass

    def before_find(self, by, value, driver):
        pass

    def after_find(self, by, value, driver):
        driver.execute_script("arguments[0].style.border = 'medium solid blue';",driver.find_element_by_id(value))
        sleep(3)
    
    def before_click(self, element, driver):
        pass

    def after_click(self, element, driver):
        pass

    def before_change_value_of(self, element, driver):
        pass

    def after_change_value_of(self, element, driver):
        pass

    def before_execute_script(self, script, driver):
        pass

    def after_execute_script(self, script, driver):
        pass

    def before_close(self, driver):
        pass

    def after_close(self, driver):
        pass

    def before_quit(self, driver):
        pass

    def after_quit(self, driver):
        pass

    def on_exception(self, exception, driver):
        pass
    
    
class Condicoes_de_aguarde():
    def VISIVEL(self,elemento,tipo):
        tipo=self.__definir_by(tipo)
        return expected_conditions.visibility_of_element_located(tipo(elemento))
    
    def CLICAVEL(self,elemento,tipo):
        tipo=self.__definir_by(tipo)
        return expected_conditions.element_to_be_clickable(tipo(elemento))
    
    def ALERTA_PRESENTE(self):
        return expected_conditions.alert_is_present()
    
    def NOVA_JANELA_ABERTA(self,indice_janela):
        return expected_conditions.new_window_is_opened(indice_janela)
    
    def TITULO_SER_IGUAL_A(self,titulo_ser):
        return expected_conditions.title_is(titulo_ser)
    
    def URL_CONTEM(self,url):
        return expected_conditions.url_contains(url)
    
    def TEXTO_ESTAR_PRESENTE_ELEMENTO(self,elemento,tipo,texto):
        tipo=self.__definir_by(tipo)
        return expected_conditions.text_to_be_present_in_element(tipo(elemento),texto)
        
    def __definir_by(self,tipo):
        if(tipo=='id'):
            return By.ID
        elif(tipo=='class'):
            return By.CLASS_NAME
        elif(tipo=='xpath'):
            return By.XPATH
        elif(tipo=='name'):
            return By.NAME
        elif(tipo=='tag'):
            return By.TAG_NAME
        elif(tipo=='partial_link'):
            return By.PARTIAL_LINK_TEXT
        elif(tipo=='link'):
            return By.LINK_TEXT
        elif(tipo=='css'):
            return By.CSS_SELECTOR
        else:
            Erro="""
            Escolha um valor de elemento Valido
            lista de elementos:
            id:    Desk,Web,Mobile
            name:    Desk,Web,Mobile
            class:    Desk,Web,Mobile
            xpath:    Desk,Web,Mobile
            link:    Web
            tag:    Web,Mobile
            css:    Web,Mobile
            partial_link:    Web
            
            
            """
            raise Elemento_erro(Erro)
        
class Tipos_de_elemento():
  
    ID='id'
    CLASS_NAME='class'
    XPATH='xpath'
    NAME='name'
    TAG_NAME='tag'
    PARTIAL_LINK='partial_link'
    LINK_TEXT='link'
    CSS_SELECTOR='css'
    
  
class Teclas_para_driver(Keys):
    pass