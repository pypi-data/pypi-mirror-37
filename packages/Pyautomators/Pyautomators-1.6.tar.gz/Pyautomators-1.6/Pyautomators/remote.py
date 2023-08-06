# -*- coding: utf-8 -*-
'''
Created on 12 de set de 2018

@author: koliveirab
'''
import http.server
import socketserver
import socket
import ast
from .Runner_Pyautomators import Thread_Run
''' Esta modulo tem o intuito de trabalhar em conjunto comunica��o entre sistemas e gera��o de Threads, 
trabalhando com cloud, processos e sistemas provedores de servi�os de nuvem e docker'''
def servidor_http(endereco:str,porta:int):
    '''Esta fun��o tem como principio gerar um servidor http'''
    #criando um objeto servidor
    Handler = http.server.SimpleHTTPRequestHandler
    #criando o objeto para servidor socket tcp
    httpd = socketserver.TCPServer((endereco, porta), Handler)
    #subindo o servidor e rodando com while==true
    httpd.serve_forever()

class Runner_Client():
    def __init__(self,Server):
        #abrindo um objeto socket
        self.Client=socket.socket()
        #endereco do servidor e porta==9000
        host,port=Server, 9000
        #conectando a este endereço
        self.Client.connect((host,port))
        """Conectando ao servidor"""
        #aguardando uma resposta do servidor
        valor=self.Client.recv(1024).decode("utf8")
        #transformando o json que receber como string em um dicionario
        jsons=ast.literal_eval(valor)
        """ Aguardando resposta da conexao com o valor para rodar o teste"""
        #verificando o tipo do teste enviado
        if(jsons["tipo"]=="Funcional Web"):
            #criando threads de cada navegador
            for navegador in jsons['navegadores']:
                #iniciando cada thread de cada navegador
                Thread_Run(navegador,jsons).start()
        
        
class Controler_Remote_Runner():
    
    def __init__(self,Folder):
        #abrindo um objeto socket
        self.Server=socket.socket()
        #recebendo todos os os parametros
        self.parameter=Folder
        #pegando o tamanho de todos os testes para rodar
        self.Instancias=len(Folder) 
        """ Preparando """   
        def Preper(self):
            #criando o servidor com o endereço atual e a porta==9000
            self.Endereco=(socket.gethostbyname(socket.gethostname()),9000)
            self.Server.bind(self.Endereco)
            #abrindo o numero de usuarios simultaneos igual ao tamanho de testes que iram rodar
            self.Server.listen(self.Instancias)
            print('Server:{}\nQuanditade de acessiveis:{}'.format(self.Endereco,self.Instancias))
        Preper()
        
    def Runner(self):  
        #criando uma lista para receber informações de todos os servidores  
        lista=[]             
        def iniciar():
            #enquanto tiver reste para ser enviado ira rodar
            for paramete in self.parameter:
                #aguardando alguem se conectar
                c,addr =self.Server.accept()          
                print(addr)
                #adicionando o client na lista de registro
                lista.append(addr)
                print(paramete)
                #enviando o encode do json do que o client deve fazer
                c.send(str(self.parameter[paramete]).encode('utf_8'))
        iniciar()