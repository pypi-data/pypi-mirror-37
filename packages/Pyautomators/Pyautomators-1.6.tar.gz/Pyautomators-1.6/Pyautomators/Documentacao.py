# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
import pyautogui
import json
import behave2cucumber
from .Ambiente import _tratar_path
import ast
''' Este modulo tem o intuito de trabalhar a geração de artefatos, 
trabalhando com a entrada dos dados para o teste'''

def printarTela(NomeArquivo):
    '''Esta função retira prints da tela e grava em um arquivo
    parametros:
    NomeArquivo(obrigatorio): Nome do arquivo 
    
    Exemplo:
    printarTela("valor.png")'''
    #ajustar a path e tirar um print com o nome passado
    nome=_tratar_path(NomeArquivo)
    #Tira o print
    pyautogui.screenshot(nome) 

def print_local(xi,yi,xf,yf,NomeArquivo):
    '''Esta função retira prints da tela apartir de coordenadas pré estabelecidas
    parametros:
    xi,yi,xf,yf(obrigatorio):Coordenadas iniciais e finais para enquadrar o print
    NomeArquivo(obrigatorio): Nome do arquivo 
    
    Exemplo:
    print_local(10,200,100,1000"valor.png")''' 
    #faz uma função lambida que retira a largura e a altura
    result= lambda a,b:b-a 
    xd=result(xi,xf)
    yd=result(yi,yf)
    #ajustar a path e tirar um print com o nome passado e as medidas iniciais     
    nome=_tratar_path(NomeArquivo)
    #Tira o print
    pyautogui.screenshot(nome,region=(xi,yi, xd, yd))
   
def tranforma_cucumber(NomeArquivo,novo=None):
    '''Esta função transforma o padrão de report json do Behave, em um padrão compativel com o Cucumber
    parametros:
    NomeArquivo(obrigatorio): Nome do arquivo 
    novo:Nome de um novo arquivo caso necessario gerar os dois, sendo o segundo o padrão json do Cucumber
    
    Exemplo:
    tranforma_cucumber("teste.json","teste2.json")
    tranforma_cucumber("teste.json")'''
    nome=_tratar_path(NomeArquivo)
    valor=""
    #Abertura do arquivo com os resultados
    with open(nome) as behave_json:
        #Transformando o padrão behave em cucumber
        cucumber_json = behave2cucumber.convert(json.load(behave_json))
        #Encontrando a duração do teste
        for element in cucumber_json:
            elemento=element["elements"]
            for lista in elemento:
                listaa=lista["steps"]
                for lis in listaa:
                    li=lis["result"]["duration"]
                    #Convertendo a quantidade de horas
                    lis["result"]["duration"]=int(li*1000000000)
        #Transformando de aspas  simples para aspas duplas.
        valor=ast.literal_eval(str(cucumber_json).replace("\'",'"""').replace("'",'"'))
    #Caso o nome do segundoo arquivo exita ele grava no segundo arquivo e mantei o primeiro intacto, se não a modificação e salva no primeiro
    if(novo is None):
        novo=nome
    #Abrindo o arquivo 
    arquivo = open(novo,'w')  
    #Carregando o json
    #conteudo=json.loads(valor)
    #Ajustando json
    conteudo=json.dumps(valor,indent=4)   
    #Salvando no arquivo       
    arquivo.write(conteudo)
    #Fechando o arquivo
    arquivo.close()
    return valor