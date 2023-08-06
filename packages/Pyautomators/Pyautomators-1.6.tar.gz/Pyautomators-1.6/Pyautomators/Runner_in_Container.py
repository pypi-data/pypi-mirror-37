# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''

import threading
import docker
from Pyautomators import Dados
from .Runner_Pyautomators import Error
class Escalavel_web(threading.Thread):
    def __init__(self,Image,volume,indice,path_yaml):
        '''Super Classe Thread'''
        #recebendo os metodos da classe pai como herança
        threading.Thread.__init__(self)
        '''Recebendo um agente docker'''
        #conectando ao docker local
        self.client=docker.from_env()
        '''Recebendo um atributo Imagem'''
        #guardando as variaveis de imagem, volume e o comando a ser enviado dentro do container
        self.Image=Image
        self.volume=volume
        self.indice=indice
        self.path_yaml=path_yaml
    def run(self):    
        '''Rodando o container ''' 
        #rodando o container com a imagem enviada enviando o volume e os comandos dentro do container e destruindo apos a execução  
        self.client.containers.run(image=self.Image,command="python3 -m Pyautomators.Runner_Pyautomators -P={} -I={}".format(self.path_yaml,self.indice),volumes=self.volume,remove=True)
        
class Runner_Container:
    
    def Runner_line(self,path_yaml,volume):
        #Iterando em todos os testes que devem ser executados
        Folder=Dados.pegarConteudoYAML(path_yaml)
        indice=0
        for container in Folder:
            indice+=1
            
            if(Folder[container]['TESTE']=='Web'):
                #a imagem deve ser ...
                Image="pyautomators"
            else:
                Error='''
                        Este teste nao é valido, os testes validos são
                        
                        Web'''
                raise 
            #executa a thread atual
            Escalavel_web(Image,volume,indice,path_yaml).start()