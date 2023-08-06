# -*- coding: utf-8 -*-

'''
Created on 26 de set de 2018

@author: koliveirab
'''
import argparse
from behave.__main__ import main
import threading
import ast
from Pyautomators import Dados
from .Error import Ambiente_erro
        
class Modelador_Funcional_Web():
    
    @staticmethod
    def Run_Pyautomators(dicionario_yaml,navegador):
        
        lista_de_execucao=["--capture",'--logcapture','-v','--no-junit','--capture-stderr']
        for item in dicionario_yaml:
            if(item=='tags'):
                for arg in dicionario_yaml[item]:
                    tag_string=str(",").join(dicionario_yaml[item])
                lista_de_execucao.append("--tags="+tag_string)
            if(item=='args'):
                for arg in dicionario_yaml[item]:
                    lista_de_execucao.append('-D'+str(arg)+'='+str(dicionario_yaml[item][arg]))
            if(item=='saida'):
                lista_de_execucao.append('--format=json.pretty')
                lista_de_execucao.append('-o='+str(navegador).upper()+dicionario_yaml[item])
            if(item=='navegador'):
                if(dicionario_yaml[item]=='Chrome'):
                    lista=[]
                    for options in dicionario_yaml[item]:
                        lista.append(options)
                    lista_de_execucao.append('-DchromeOptions='+str(lista))
                if(dicionario_yaml[item]=='Firefox'):
                    lista=[]
                    for options in dicionario_yaml[item]:
                        lista.append(options)
                    lista_de_execucao.append('-DfirefoxOptions='+str(lista))

        lista_de_execucao.append('-Dnavegador='+navegador)
        return lista_de_execucao
    
class Modelador_Funcional_Moble():
    
    @staticmethod
    def Run_Pyautomators(dicionario_yaml,Device):
        
        lista_de_execucao=["--capture",'--logcapture','-v','--no-junit','--capture-stderr']
        for item in dicionario_yaml:
            if(item=='tags'):
                for arg in dicionario_yaml[item]:
                    tag_string=str(",").join(dicionario_yaml[item])
                lista_de_execucao.append("--tags="+tag_string)
            if(item=='args'):
                for arg in dicionario_yaml[item]:
                    lista_de_execucao.append('-D'+str(arg)+'='+str(dicionario_yaml[item][arg]))
            if(item=='saida'):
                lista_de_execucao.append('--format=json.pretty')
                lista_de_execucao.append('-o='+str(Device).upper()+dicionario_yaml[item])
            if(item=='Device'):
                if(dicionario_yaml[item]=='Android'):
                    lista=[]
                    for options in dicionario_yaml[item]:
                        lista.append(options)
                    lista_de_execucao.append('-DAndroidOptions='+str(lista))
                if(dicionario_yaml[item]=='Ios'):
                    lista=[]
                    for options in dicionario_yaml[item]:
                        lista.append(options)
                    lista_de_execucao.append('-DIosOptions='+str(lista))

        lista_de_execucao.append('-Ddevice='+Device)
        return lista_de_execucao
    

class Thread_Run(threading.Thread):
    def __init__(self,Item,list_exec):
        threading.Thread.__init__(self)
        self.Item=Item
        self.list_exec=list_exec
    def run(self):  
        valor=None 
        if(self.list_exec['Teste']=='Web'):
            valor=Modelador_Funcional_Web.Run_Pyautomators(self.list_exec, self.Item) 
        elif(self.list_exec['Teste']=='Mobile'):
            valor=Modelador_Funcional_Moble.Run_Pyautomators(self.list_exec, self.Item) 
        main(valor)
        
def runner(dicionario_de_execucao):
    if(dicionario_de_execucao['TESTE']=='Web'):
        for Navegador in dicionario_de_execucao['navegadores']:
            Thread_Run(Navegador,dicionario_de_execucao).start()
    if(dicionario_de_execucao['TESTE']=='Mobile'):
        for device in dicionario_de_execucao['devices']:
            Thread_Run(device,dicionario_de_execucao).start()

def main(dicionario_de_execucao):
    runner(dicionario_de_execucao)
    
if('__main__'==__name__):

    ARG=argparse.ArgumentParser()
    ARG.add_argument("-P",'--path_yaml',required=True,help="Arquivo Yaml")
    ARG.add_argument("-I",'--indice',required=True,help="Indice de execucao")
    
    valores=dict(vars(ARG.parse_args()))
    
    dicionario_de_execucao=ast.literal_eval(valores["Dict_valor"])
    
    Folder=Dados.pegarConteudoYAML(dicionario_de_execucao['path_yaml'])
    indice=1
    executavel=None
    for Teste in Folder:
        if(indice==dicionario_de_execucao['indice']):
            executavel=Teste
            break
        indice+=1
    if executavel==None:
        Error='''
                Não Existe este Indice para a execução'''
        raise Ambiente_erro(Error)
    runner(dicionario_de_execucao)