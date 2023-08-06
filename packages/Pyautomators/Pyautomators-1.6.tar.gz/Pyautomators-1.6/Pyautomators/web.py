# -*- coding: utf-8 -*-

'''
@author: KaueBonfim
'''
from time import sleep
from selenium.webdriver.support.events import EventFiringWebDriver
from .mouse_teclado import Teclado,Mouse
from .Verifica import Valida
from .web_extensao import Espera,Js_Script,Simula,Alerta,MyListener,Condicoes_de_aguarde
from selenium import webdriver
from selenium.webdriver import ActionChains
from .Error import Driver_erro,Elemento_erro
from .Drivers import Firefox,Chrome
''' Este arquivo prove os metodos em selenium para web,
    na qual os passamos um elemento chave e seu tipo e ele executa a acao descrita'''


class Web(Teclado,Mouse,Valida,Espera,Js_Script,Simula):
    ''' Esta classe tem o intuito de prover conexão com selenium em web'''
    def __init__(self,driver,path_driver=None,options=None,Log_driver=None,binarios=None):
        '''No construtor temos um parametros sendo um obrigatorio
        driver(obrigatorio):Qual dos drivers a serem usados
        path_driver:Local Aonde esta o Driver web usado
        options:as configuraÃ§Ãµes passadas pelo options do driver
        '''
                  
        if(driver == 'Chrome'):
            if(path_driver==None):
                path_driver="chromedriver"
            self.__driver=Chrome(path_driver=path_driver,opcoes=options,log=Log_driver,binario=binarios).get_driver()  
            self.driver=EventFiringWebDriver(self.__driver,MyListener())
        elif(driver == 'Firefox'):  
            if(path_driver==None):
                path_driver="geckodriver"          
            self.__driver=Firefox(path_driver=path_driver,options=options,log=Log_driver,binario=binarios).get_driver()
            self.driver=EventFiringWebDriver(self.__driver,MyListener())
            
                    
        elif(driver == 'Ie'):    
            if(path_driver==None):
                path_driver="IEDriverServer.exe"          
            self.driver=webdriver.Ie(executable_path=path_driver)
            
        elif(driver == 'Edge'):    
            if(path_driver==None):
                path_driver="MicrosoftWebDriver.exe"          
            self.driver=webdriver.Edge(executable_path=path_driver)
        else:
            Erro="""
                NÃ£o é um driver de servidor valido!
                Digite um driver valido:
                
                Ie
                Firefox
                Chrome    
                Edge 
                    """
            raise Driver_erro(Erro) 
            
            
    
        
        
        
        
        self.alert=Alerta(self.driver)
        self.ActionChains=ActionChains(self.driver)
        self.Condicao=Condicoes_de_aguarde()
        
    def print_janela(self,path_imagem):
        '''Este metodo tira um print do conteudo atual da janela sendo usada
        
            parametros:
            path_imagem(obrigatorio):nome a imagem mais o caminho dela caso seja em outro diretorio
           Exemplo:
        print_janela('c:/teste.png')
        print_janela('teste.png')'''
        
        self.driver.get_screenshot_as_file(path_imagem)
        
        
    def fechar_programa(self):
        '''Este metodo fecha o driver web
        Exemplo:
        fechar_programa()''' 
        self.driver.quit()  
          
    def get_url(self):
        '''Este metodo retorna a Url atual
           Exemplo:
        get_url()''' 
        return self.driver.current_url
        
    def pagina(self,url):
        '''Este metodo vai a pagina passada para a url
           Exemplo:
        pagina('http://google.com.br')''' 
        self.driver.get(url)
        
    def maximiza(self):
        '''Este metodo maximiza a janela do driver utilizado
           Exemplo:
        maximiza()''' 
        self.driver.maximize_window()
    
    
    def preencher_tela(self):
        '''Este metodo preenche a tela inteira com a pagina
           Exemplo:
        preencher_tela()'''
        self.driver.fullscreen_window()
            
    def atualizar(self):
        '''Este metodo atualiza a pagina atual
           Exemplo:
        atualizar()'''
        self.driver.refresh()
        
    def voltar(self):
        '''Este metodo retorna a pagina anterior
           Exemplo:
        voltar()'''
        self.driver.back()
    
    def frente(self):
        '''Este metodo segue para a proxima pagina em sequencia
           Exemplo:
        frente()'''
        self.driver.forward()
    
    def limpar(self):
        '''Este metodo limpa o campo de um input de texto
           Exemplo:
        limpar()'''
        self.driver.clear()
        
    def get_titulo(self):
        '''Este metodo retorna o titulo atual da pagina
           Exemplo:
        get_titulo()'''
        return self.driver.title
    
    def get_html(self):
        return self.driver.page_source
    
    def get_navegador(self):
        '''Este metodo retorna o navegador que esta sendo usado no driver
           Exemplo:
        get_navegador()'''
        return self.driver.name
    
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
        
        id:    Web    <form id="loginForm"> = 'loginForm'
        
        name:    Web    <input name="username" type="text" /> = 'username'
        
        class:    Web     <p class="content">Site content goes here.</p> = 'content'
        
        xpath:    Web <html>                    =    '/html/body/form[1]' ou '//form[1]' ou '//form[@id='loginForm']'
                                     <body>
                                      <form id="loginForm">
                                      
        link:    Web        <a href="continue.html">Continue</a> = 'Continue'
        
        tag:    Web    <h1>Welcome</h1> = 'h1'
        
        css:    Web    <p class="content">Site content goes here.</p> = 'p.content'
        
        partial_link:    Web    <a href="continue.html">Continue</a> = 'Conti'
           
        '''  
        if(implicit!=None):  
            self.driver.implicitly_wait(implicit)
        if(tipo == 'id'):
            element=self.driver.find_element_by_id(elemento)
        elif(tipo == 'name'):
            element=self.driver.find_element_by_name(elemento) 
        elif(tipo == 'class'):            
            element=self.driver.find_element_by_class_name(elemento) 
        elif(tipo == 'xpath'):            
            element=self.driver.find_element_by_xpath(elemento) 
        elif(tipo == 'link'):            
            element=self.driver.find_element_by_link_text(elemento) 
        elif(tipo == 'tag'):            
            element=self.driver.find_element_by_tag_name(elemento) 
        elif(tipo == 'css'):            
            element=self.driver.find_element_by_css_selector(elemento) 
        elif(tipo == 'partial_link'):            
            element=self.driver.find_element_by_partial_link_text(elemento) 
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Web
                name:    Web
                class:    Web
                xpath:    Web
                link:    Web
                tag:    Web
                css:    Web
                partial_link:    Web
                andorid:    Mobile
                ios:    Mobile
                binding:    Web(Angular)
                model:    Web(Angular)
                
                """
            raise Elemento_erro(Erro)
        return element
      
    def elemento_list(self,elemento,tipo,indice_lista,implicit=None):
        '''Esta procura um elemento  dentro de uma lista de elementos com o mesmo parametro
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        indice_lista(obrigatorio):Indice de ordem do elemento na lista
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        elemento_list("id.user","id",0,10)
        elemento_list("class_user_login","class",3,1)
        elemento_list("login","name",2)
        
        lista de elementos:
        
        id:    Web    <form id="loginForm"> = 'loginForm'
        
        name:    Web    <input name="username" type="text" /> = 'username'
        
        class:    Web     <p class="content">Site content goes here.</p> = 'content'
        
        xpath:    Web <html>                    =    '/html/body/form[1]' ou '//form[1]' ou '//form[@id='loginForm']'
                                     <body>
                                      <form id="loginForm">
                                      
        link:    Web        <a href="continue.html">Continue</a> = 'Continue'
        
        tag:    Web    <h1>Welcome</h1> = 'h1'
        
        css:    Web    <p class="content">Site content goes here.</p> = 'p.content'
        
        partial_link:    Web    <a href="continue.html">Continue</a> = 'Conti'
       
        
        '''
        if(implicit!=None):  
            self.driver.implicitly_wait(implicit)
        elements=self.elementos_list(elemento, tipo, implicit)
        element=elements[indice_lista]
        return element
    
    def elementos_list(self,elemento,tipo,implicit=None):
        '''Esta procura todos os elementos de elementos com o mesmo parametro
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        elementos_list("id.user","id",10)
        elementos_list("class_user_login","class",1)
        elementos_list("login","name")
        
        lista de elementos:
        
        id:    Web    <form id="loginForm"> = 'loginForm'
        
        name:    Web    <input name="username" type="text" /> = 'username'
        
        class:    Web     <p class="content">Site content goes here.</p> = 'content'
        
        xpath:    Web <html>                    =    '/html/body/form[1]' ou '//form[1]' ou '//form[@id='loginForm']'
                                     <body>
                                      <form id="loginForm">
                                      
        link:    Web        <a href="continue.html">Continue</a> = 'Continue'
        
        tag:    Web    <h1>Welcome</h1> = 'h1'
        
        css:    Web    <p class="content">Site content goes here.</p> = 'p.content'
        
        partial_link:    Web    <a href="continue.html">Continue</a> = 'Conti'
        
         
        '''
        
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
        elif(tipo == 'link'):            
            elements=self.driver.find_elements_by_link_text(elemento)
        elif(tipo == 'tag'):            
            elements=self.driver.find_elements_by_tag_name(elemento)
        elif(tipo == 'text'):            
            elements=self.driver.find_elements_by_partial_link_text(elemento)
        elif(tipo == 'css'):            
            elements=self.driver.find_elements_by_css_selector(elemento)
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Web
                name:    Web
                class:    Web
                xpath:    Web
                link:    Web
                tag:    Web
                css:    Web
                partial_link:    Web
                """
            raise Elemento_erro(Erro)
        return elements
    
    def elemento_por_texto(self,elemento_base,tipo,texto_referencia,implicit=None):
        '''Este metodo retorna em um elemento, baseado no texto referencia 
        na qual temos 3 parametros
        
        elemento_base(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        texto_referencia(obrigatorio): escolhe qual elemento da lista, baseado no texto
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        
        
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <a href='http://algumacoisa.com.br'>texto valor</a>
                
                 elemento_por_texto("gsfi","class",'texto valor')
        '''
        elemento=None
        elements=self.elementos_list(elemento_base, tipo,implicit)
        for element in elements:
            if(element.text==texto_referencia):
                elemento=element
        return elemento
    
    
    def elemento_por_atributo(self,elemento_base,tipo,atributo_referencia,valor,implicit=None):
        '''Este metodo retorna em um elemento, baseado no atributto referencia 
        na qual temos 3 parametros
        
        elemento_base(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        texto_referencia(obrigatorio): escolhe qual elemento da lista, baseado no texto
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        
        
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <a href='http://algumacoisa.com.br'>texto valor</a>
                
                 elemento_por_texto("gsfi","class",'texto valor')
        '''
        if(implicit!=None):  
            self.driver.implicitly_wait(implicit)
        elemento=None
        elements=self.elementos_list(elemento_base, tipo)
        for element in elements:
            if(element.get_attribute(atributo_referencia)==valor):
                elemento=element
        return elemento
    
    def escreve(self,elemento,conteudo,tipo,implicit=None,tempo=None):
        '''Este metodo escreve em um elemento, na qual temos cinco parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        tempo:É o tempo que leva para escrever cada tecla.
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input class="gsfi" id="lst-ib" maxlength="2048" name="q" autocomplete="off" title="Pesquisar" >
                
                 escreve("gsfi","QUALQUER TEXTO","class",10,0.1)
        '''
        
        element=self.elemento(elemento,tipo,implicit) 
        if(tempo is not None):
            if(self.tipo=='web'):
                for char in conteudo:
                    element.send_keys(char) 
                    sleep(tempo)
        else:
            element.send_keys(conteudo)
            
        return element
    
    def clica_elemento_atributo(self,elemento_base,tipo,atributo_referencia,valor,implicit=None):
        self.elemento_por_atributo(elemento_base, tipo, atributo_referencia, valor,implicit).click()
        
    def escreve_por_texto(self,elemento_base,tipo,conteudo,texto_referencia,implicit=None):
        '''Este metodo escreve em um elemento, na qual temos cinco parametros
        
        elemento_base(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        texto_referencia(obrigatorio): escolhe qual elemento da lista, baseado no texto
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <a href='http://algumacoisa.com.br'>texto valor</a>
                
                 escreve_por_texto("gsfi","class",'Valor','texto valor')
        '''
       
        elemento=self.elemento_por_texto(elemento_base, tipo, texto_referencia,implicit)    
        elemento.send_keys(conteudo)
        return elemento
    
    def clica_por_text(self,elemento_base,tipo,texto_referencia):
        '''Este metodo escreve em um elemento, na qual temos cinco parametros
        
        elemento_base(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao.
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        texto_referencia(obrigatorio): escolhe qual elemento da lista, baseado no texto

        
        Exemplos:
        
            dado um trecho de HTML:
            
                <a href='http://algumacoisa.com.br'>texto valor</a>
                
                 clica_por_text("gsfi","class",'texto valor')
        '''
        elemento=self.elemento_por_texto(elemento_base, tipo, texto_referencia)
        elemento.click()
        return elemento
           
    def clica(self,elemento,tipo,implicit=None):
        '''Este metodo clica em um elemento, na qual temos tres parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input class="gsfi" id="lst-ib" maxlength="2048" name="q" autocomplete="off" title="Pesquisar" >
                
                clica("gsfi","class",10)
        '''
        
        element=self.elemento(elemento,tipo,implicit) 
        element.click()
        return element
             
    
    def pegar_texto(self,elemento,tipo,implicit=None):
        '''Este metodo retorna o texto de um elemento, na qual temos tres parametros
        
        retornara o texto que estiver no elemento
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        Exemplos:
        
            dado um trecho de HTML:
            
                <input class="gsfi" id="lst-ib" maxlength="2048" name="q" autocomplete="off" title="Pesquisar" >Textooo</input>
                
                valor=pegar_textto("lst-ib","id",10)
                print(valor)
                >>>Textooo
        '''
        element=self.elemento(elemento,tipo,implicit) 
        return element.text,element
                
    def escrever_elemento_lista(self,elemento,conteudo,tipo,indice_lista:int,implicit=None,tempo:int=None):
        '''Este metodo escreve em um elemento de uma lista de elementos com o mesmo tipo e elemento, na qual temos seis parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a busca na lista de elementos com a mesma descricao
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        indice_lista(obrigatorio): Qual dos itens que achamos queremos usar, este sempre retorna uma lista na ordem que foi achado 
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        tempo:É o tempo que leva para escrever cada tecla.
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input name="btn" type="submit" jsaction="sf.lck">
                <input name="btn" type="submit" jsaction="sf.chk">
                
                escrever_elemento_lista("input","QUAL QUER TEXTO","tag",2,10,0.1)
        '''
        element=self.elemento_list(elemento,tipo,indice_lista,implicit)
        element.send_keys(conteudo)     
            
    def clica_elemento_lista(self,elemento,tipo,indice_lista:int,implicit=None):
        '''Este metodo clica em um elemento de uma lista de elementos com o mesmo tipo e elemento. na qual temos quatro parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a busca na lista de elementos com a mesma descricao
        indice_lista(obrigatorio): Qual dos itens que achamos queremos usar, este sempre retorna uma lista na ordem que foi achado
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input name="btn" type="submit" jsaction="sf.lck">
                <input name="btn" type="submit" jsaction="sf.chk">
                
                clica_elemento_lista("input","tag",1,10)
        '''
        element=self.elemento_list(elemento,tipo,indice_lista,implicit)
        element.click()
        return element 
    
    def pegar_texto_list(self,elemento,tipo,indice_lista:int,implicit=None):
        '''Este metodo retorna o texto de um elemento de uma lista de elementos com o mesmo tipo e elemento. na qual temos quatro parametros
        
        retornara o texto que estiver no elemento
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        indice_lista(obrigatorio): Qual dos itens que achamos queremos usar, este sempre retorna uma lista na ordem que foi achado
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            dado um trecho de HTML:
            
                <input name="btn" type="submit" jsaction="sf.lck">
                <input name="btn" type="submit" jsaction="sf.chk">
                
                pegar_texto_list("input","tag",1,10)
        '''
        element=self.elementos_list(elemento,tipo,indice_lista,implicit)
        return element.text 