# -*- coding: utf-8 -*-
'''
Created on 24 de ago de 2018

@author: koliveirab
'''
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager,EdgeDriverManager
from selenium.webdriver.firefox.options import Options
from .Error import Driver_erro

class Tipos_de_navegadores():
    ''' Tipos de navegadores para a Class Web'''
    CHROME='Chrome'
    FIREFOX='Firefox'
    IE='Ie'
    EDGE='Edge'
    OPERA='Opera'
    SAFARI='Safari'
    
class Manager_Install():
    '''Esta classe tem o inteuito de promover conexao com driver binarios sem a necessidade de ter un driver instalado'''
    def __init__(self,tipo,version=None):
        """Cria um objeto que faz download do driver e deixa na memoria
        parametros:
        
        tipo(obrigatorio):Qual driver deve instalar dos browsers
        versão: qual a versao deve baixar
        
        """
        #Escolhendo qual o driver e verificando uma versao
        if(tipo == 'Chrome'):  
            self.__manager=ChromeDriverManager(version)
        elif(tipo == 'Firefox'): 
            self.__manager=GeckoDriverManager(version)
        elif(tipo == 'Ie'): 
            self.__manager=IEDriverManager(version)
        elif(tipo == 'Edge'): 
            self.__manager=EdgeDriverManager(version)
        else:
            Erro="""
                Não é um driver de manager valido!
                Digite um driver valido:
                Ie
                Firefox
                Chrome 
                Edge    
                    """
            raise Driver_erro(Erro) 
        
    def get_manager(self):
        """retorna a instancia do objeto driver"""
        #retornando a instancia de memoria do driver instalado
        return self.__manager.install()
    
class Chrome():
    '''Esta classe tem o intuito de retornar uma classe chromedriver'''
    def __init__(self,path_driver='chromedriver',opcoes=None,log=None,binario=None):
        """Este contrutor cria um obejto webdriver-chrome
        parametros:
        path_driver: caminho para o driver, caso seja omitido ele entende que o caminho e o atual
        opcoes: opções que são fornecidos pela classe Options_Chrome, e este parametro recebe a instancia da classe
        log é um arquivo que registra os acontecimentos no driver
        binario é o executavel no crhome no pc"""
        #criando um objeto chromedriver
        des=None
        #verificando se foi passado binario
        if(opcoes!=None):
            des=opcoes.to_capabilities()
            
        if(binario!=None and opcoes!=None):
            des['binary_location']=binario
        elif(binario!=None):
            des={'binary_location':binario}
        self.__driver=webdriver.Chrome(executable_path=path_driver, service_log_path=log, service_args=['--verbose'],desired_capabilities=des)
        
    def get_driver(self):
        """Retorna o objeto do driver"""
        #retornando a instancia chromedriver
        return self.__driver
    
class Firefox():
    '''Esta classe tem o intuito de retornar uma classe firefoxdriver'''
    def __init__(self,path_driver='geckodriver',log=None,options=None,binario=None):
        """Este contrutor cria um obejto webdriver-firefox
        parametros:
        path_driver: caminho para o driver, caso seja omitido ele entende que o caminho e o atual
        log é um arquivo que registra os acontecimentos no driver
        opcoes: opções que são fornecidos pela classe Firefox-perfil e Firefox-options, e este parametro recebe a instancia da classe
        binario: caso tenha necessidade de passar o binario do mozila Firefox"""
        #verificando se o binario foi passado
        print(options['opcoes'].to_capabilities())
        self.__driver=webdriver.Firefox(executable_path=path_driver, service_log_path=log,firefox_profile=options['perfil'],firefox_binary=binario,firefox_options=options['opcoes'])


    def get_driver(self):
        #retorna a instancia do Firefor
        return self.__driver

class Options_Firefox():
    '''Faz uso do perfil de opções do firefox'''
    def __init__(self):
        #Criando o objeto 
        self.__perfil=webdriver.FirefoxProfile()
        self.__options=Options()
        
    def backgroud(self):
        '''Criando uma instancia do driver sem a interface grafica'''
        self.__options.headless=True
        return self
    
    def private(self):
        '''Abrindo o Driver com a instancia do usuario em privado'''
        self.__perfil.set_preference("browser.privatebrowsing.autostart", True)        
        return self
    
    def proxy(self,endereco:str,porta:int):
        '''Setar o valor do proxy no navegador
        parametros:
        endereco:ip, ou endereco do proxy
        porta:Porta de entrada do proxy
        Exemplo:
        proxy('proxylatam.indra.es':8080)
        '''
        self.__perfil.set_preference("network.proxy.type", 1)
        self.__perfil.set_preference("network.proxy.http", endereco)
        self.__perfil.set_preference("network.proxy.http_port", porta)
        return self
    
    def get_options(self):
        return {'opcoes':self.__options,'perfil':self.__perfil}
    
    
    
class Options_Chrome():
    
    def __init__(self):
        self.options=ChromeOptions()
        
    def private(self):
        '''Abrindo o Driver com a instancia do usuario em privado'''
        self.options.add_argument("--incognito")
        return self
    
    def backgroud(self):
        '''Criando uma instancia do driver sem a interface grafica'''
        self.options.add_argument("--headless")
        return self
    
    def maximizado(self):
        '''Abrir o driver maximizado '''        
        self.options.add_argument('--start-maximized') 
        return self
    
    def posicao_janela(self,x,y):
        '''Colocar a posicao inicial do driver driver na tela
        parametros:
        x,y=local na tela
        
        Exemplo:
        posicao_janela(100,20)
        '''        
        self.options.add_argument('--window-position={},{}'.format(x,y))
        return self
    
    def tamanho_janela(self,largura,altura):
        '''Tamanho da largura e altura da tela
        parametros:
        largura,altura: sao as dimensões do driver
        Exemplo:
        tamanho_janela(self,1000,300)
        '''
        self.options.add_argument('--window-size={},{}'.format(largura,altura))
        return self
    
    def perfil(self,perfil_path):
        '''Recebe o caminho de memoria do perfil do seu chrome que utiliza
        parametros:
        perfil_path: local aonde esta seu perfil
        
        Exemplo:
        perfil('C:/Users/koliveirab/AppData/Local/Google/Chrome/User Data/')
        '''
        self.options.add_argument('user-data-dir={}'.format(perfil_path))
        return self
    
    def proxy(self,auto=True,endereco=None,porta=None):
        '''Setar o valor do proxy no navegador
        parametros:
        auto=detecta o proxy nativo na maquina
        endereco:ip, ou endereco do proxy
        porta:Porta de entrada do proxy
        Exemplo:
        proxy()
        proxy(False,'proxylatam.indra.es':8080)
        '''
        if(auto):
            self.options.add_argument('--proxy-auto-detect')
        else:
            self.options.add_argument("--proxy-server='{}:{}'".format(endereco,porta))
        return self
    
    def root(self):
        self.options.add_argument('--no-sandbox')
        return self
    
    def get_options(self):
        return self.options