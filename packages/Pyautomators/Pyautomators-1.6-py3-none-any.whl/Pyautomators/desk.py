# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
import os 
from selenium import webdriver 
from .mouse_teclado import Teclado
from .mouse_teclado import Mouse
from .Verifica import Valida
from .Error import Elemento_erro
import subprocess

''' Este arquivo tem o intuito dos metodos em selenium para Desktop,
    na qual os passamos um elemento chave e seu tipo e ele executa a acao descrita'''

class Desk(Teclado,Mouse,Valida):
    ''' Esta classe tem o intuito de prover conexão com selenium em Desktop'''
    def __init__(self,aplicacao:str,Driver_Winium="Winium.Desktop.Driver.exe"):
        '''No construtor temos dois parametros sendo um obrigatorio
        aplicacao(obrigatorio): Qual Aplicação será Testada
        Driver_Winium:Local Aonde esta o Driver do Winium
        
        '''
        #Ira abrir um subprocesso, em background para o driver
        self.sub=subprocess.Popen(Driver_Winium)
        #Ira abrir o webdriver desktop, com o nome da aplicação
        self.driver= webdriver.Remote(command_executor="http://localhost:9999",desired_capabilities={"app": aplicacao})
        
    @staticmethod
    def Open_comandLine(Comand):
        '''Este metodo abre a aplicação apartir de uma linha de comando
        Exemplo:
        Open_comandLine("C:/APP/main_interface.exe")'''
        #Ira executar um comando por linha de comano para abrir um programa, este metodo não consegue construir um objeto que tenha os comandos webdriver
        os.system(Comand)
        
    def fechar_programa(self):
        '''Este metodo fecha conexão com o driver. Exemplo: fechar()'''
        #Ira fechar o driver e o subprocesso do Winium
        self.driver.close()
        self.sub.terminate()
        
    
        
    def elemento(self,elemento,tipo,implicit=None):
        r'''Esta procura um elemento e retorna o objeto do elemento
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        elemento("id.user","id",10)
        elemento("class_user_login","class",1)
        elemento("login","name")
        
       lista de elementos:
        
        id:    Desk    
        
        name:    Desk   
        
        class:    Desk     
        
        xpath:    Desk                  
                                          
        '''
        #Verifica se precisa executar alguma espera.
        
        if(implicit!=None):
            self.driver.implicitly_wait(implicit)
            
        #Verifica se é de algum tipo para proccurar, caso contrario leva uma exceçao
        if(tipo == 'id'):
            element=self.driver.find_element_by_id(elemento)
        elif(tipo == 'name'):
            element=self.driver.find_element_by_name(elemento) 
        elif(tipo == 'class'):            
            element=self.driver.find_element_by_class_name(elemento) 
        elif(tipo == 'xpath'):            
            element=self.driver.find_element_by_xpath(elemento) 
        
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Desk
                name:    Desk
                class:    Desk
                xpath:    Desk
                               
                """
            raise Elemento_erro(Erro)
        #Retorna o elemento encontrado
        return element
      
    def elemento_list(self,elemento,tipo,indice_lista,implicit=None):
        '''Esta procura um elemento  dentro de uma lista de elementos com o mesmo parametro
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        indice_lista(obrigatorio):Indice de ordem do elemento na lista
        
        Exemplos:
        elemento_list("id.user","id",0)
        elemento_list("class_user_login","class",3)
        elemento_list("login","name",2)
        
        lista de elementos:
        
        id:    Desk            
        name:    Desk  
        class:    Desk    
        xpath:    Desk                                       
        
        '''
        #Vefificando todos os elementos com esse padrão
        elements=self.elementos_list(elemento, tipo,implicit)
        #Retirando da lista um elemento especifico, baseado no indice
        element=elements[indice_lista]
        #Retorna o elemento especifico
        return element
    
    def elementos_list(self,elemento,tipo,implicit=None):
        '''Esta procura todos os elementos de elementos com o mesmo parametro
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        
        Exemplos:
        elementos_list("login","name")
        
        lista de elementos:
        
        id:    Desk   
        
        name:    Desk    
        
        class:    Desk    
        
        xpath:    Desk
        '''
        #Vefificando todos os elementos com esse padrão
        if(implicit!=None):
            self.driver.implicitly_wait(implicit)
        if(tipo == 'id'):           
            elements=self.driver.find_elements_by_id(elemento)  
        elif(tipo == 'name'):
            elements=self.driver.find_elements_by_name(elemento)
        elif(tipo == 'class'):            
            elements=self.driver.find_elements_by_class_name(elemento)
        elif(tipo == 'xpath'):            
            elements=self.driver.find_elements_by_xpath(elemento)
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Desk
                name:    Desk
                class:    Desk
                xpath:    Desk
               
                
                """
        
            raise Elemento_erro(Erro)
        #Retorna todos os elemento buscados
        return elements
    
    def escreve(self,elemento,conteudo,tipo,implicit=None):
        '''Este metodo escreve em um elemento, na qual temos cinco parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
                 escreve("gsfi","QUALQUER TEXTO","class",10)
        '''
        #Encontrado o elemento
        element=self.elemento(elemento,tipo,implicit) 
        #Escrevendo neste elemento, caso haja conteudo, pode ser apagado antes da escrita
        element.send_keys(conteudo)
        #Retorna o elemento 
        return element
    
           
    def clica(self,elemento,tipo,implicit=None):
        '''Este metodo clica em um elemento, na qual temos tres parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            
                clica("gsfi","class",10)
        '''
        
        #Encontrado o elemento
        element=self.elemento(elemento,tipo,implicit) 
        #Ação de clicar neste elemento
        element.click()
        #Retorna o elemento
        return element
             
    
    
                
    def escrever_elemento_lista(self,elemento,conteudo,tipo,indice_lista:int,implicit=None):
        '''Este metodo escreve em um elemento de uma lista de elementos com o mesmo tipo e elemento, na qual temos seis parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a busca na lista de elementos com a mesma descricao
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        indice_lista(obrigatorio): Qual dos itens que achamos queremos usar, este sempre retorna uma lista na ordem que foi achado 
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        Exemplos:
        
           
                escrever_elemento_lista("input","QUAL QUER TEXTO","tag",2)
        '''
        #Encontrado o elemento, em uma lista de elementos        
        element=self.elemento_list(elemento,tipo,indice_lista,implicit)
        #Escrevendo neste elemento
        element.send_keys(conteudo)
        #Retornando o elemento
        return  element     
            
    def clica_elemento_lista(self,elemento,tipo,indice_lista:int,implicit=None):
        '''Este metodo clica em um elemento de uma lista de elementos com o mesmo tipo e elemento. na qual temos quatro parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a busca na lista de elementos com a mesma descricao
        indice_lista(obrigatorio): Qual dos itens que achamos queremos usar, este sempre retorna uma lista na ordem que foi achado
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        Exemplos:
        
            
                clica_elemento_lista("input","tag",1,10)
        '''
        #Encontrado o elemento, em uma lista de elementos        
        element=self.elemento_list(elemento,tipo,indice_lista,implicit)
        #Clica no elemento
        element.click()
        #Retorna o elemento
        return element
        
    def get_element_location(self,element,tipo,implicit=None):
        '''Este metodo clica em um elemento de uma lista de elementos com o mesmo tipo e elemento. na qual temos quatro parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a busca na lista de elementos com a mesma descricao
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            
                get_element_location("input","tag",10)
        '''
        #Encontra o elemento
        elemento=self.elemento(element,tipo,implicit)
        #Retira as medidas, e retorna uma string
        valor=elemento.get_attribute('BoundingRectangle')
        #Cria uma lista com os valores, pontos,x,y e a altura e largura
        localizacao=str(valor).split(',')
        #Retorna uma tupla, com os valores x,y inicial e os pontos x,y final
        return (int(localizacao[0]),int(localizacao[1]),int(localizacao[0])+int(localizacao[2]),int(localizacao[1])+int(localizacao[3]))